from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import LoginForm, RegisterForm, CreatePostForm, CommentForm, FormDadosGerais, ContactForm
from flask_gravatar import Gravatar
from class_email import Class_email


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)
gravatar = Gravatar(app, size=100, rating='g', default='retro', force_default=False, force_lower=False, use_ssl=False, base_url=None)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


##CONFIGURE TABLE
class User(UserMixin, db.Model):

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    # posts = relationship("BlogPost", back_populates="author")
    comments = relationship("Comment", back_populates="comment_author")


# class BlogPost(db.Model):
#     __tablename__ = "blog_posts"
#     id = db.Column(db.Integer, primary_key=True)
#     author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
#     author = relationship("User", back_populates="posts")
#     title = db.Column(db.String(250), unique=True, nullable=False)
#     subtitle = db.Column(db.String(250), nullable=False)
#     date = db.Column(db.String(250), nullable=False)
#     body = db.Column(db.Text, nullable=False)
#     img_url = db.Column(db.String(250), nullable=False)
#     comments = relationship("Comment", back_populates="parent_post")


class Comment(db.Model):

    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("blog_posts.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # parent_post = relationship("BlogPost", back_populates="comments")
    comment_author = relationship("User", back_populates="comments")
    text = db.Column(db.Text, nullable=False)

class Menu(db.Model):

    __tablename__ = "TbOne"
    id = db.Column(db.Integer, primary_key=True)
    RefPartner = db.Column(db.String, unique=True, nullable=False)
    Cliente = db.Column(db.String)
    Origem = db.Column(db.String)
    Destino = db.Column(db.String)
    Incoterm = db.Column(db.String)
    RefCliente = db.Column(db.String)
    Moeda = db.Column(db.String)
    modal = db.Column(db.String)
    VlTotal = db.Column(db.Float)
    Merc = db.Column(db.String)
    Vol = db.Column(db.String)
    M3 = db.Column(db.Float)
    Pb = db.Column(db.Float)
    Pl = db.Column(db.Float)
    Re = db.Column(db.String)
    Sd = db.Column(db.String)
    Status = db.Column(db.String)
    Obs = db.Column(db.String)
    bl = db.Column(db.String)
    nrBl = db.Column(db.String)
    navio = db.Column(db.String)
    vg = db.Column(db.String)
    via = db.Column(db.String)
    eta = db.Column(db.String)
    DLDraft = db.Column(db.String)
    DLCarga = db.Column(db.String)
    ttime = db.Column(db.String)
    dtBL = db.Column(db.String)
    Importador = db.Column(db.String)
    dcts = db.Column(db.String)
    Operador = db.Column(db.String)
    Booking = db.Column(db.String)
    TipoFrt = db.Column(db.String)
    Saida = db.Column(db.String)
    # abert = db.Column(db.String)
    fech = db.Column(db.String)
    dtEnvDcts = db.Column(db.String)
    lclFcl = db.Column(db.String)

db.create_all()


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def get_all_posts():

    posts =Menu.query.all()
    return render_template("index.html", all_posts=posts, current_user=current_user)


@app.route('/register', methods=["GET", "POST"])
def register():

    form = RegisterForm()

    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            print(User.query.filter_by(email=form.email.data).first())
            #User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("get_all_posts"))

    return render_template("register.html", form=form, current_user=current_user)


@app.route('/login', methods=["GET", "POST"])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        # Email doesn't exist or password incorrect.
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('get_all_posts'))
    return render_template("login.html", form=form, current_user=current_user)


@app.route('/logout')
def logout():

    logout_user()
    return redirect(url_for('get_all_posts'))

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------


@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    form = FormDadosGerais()
    if not current_user.is_authenticated:
        flash("You need to login or register to comment.")
        return redirect(url_for("login"))
    emb = Menu.query.get(post_id)
    if form.submit1.data:
    # if form.submit1.data and form.validate_on_submit():

        emb.RefPartner  =    form.RefPartner.data
        emb.Cliente     =    form.Cliente.data
        emb.RefCliente  =    form.RefCliente.data
        emb.Origem      =    form.Origem.data
        emb.Destino     =    form.Destino.data
        emb.modal       =    form.modal.data
        emb.Incoterm    =    form.Incoterm.data
        emb.Moeda       =    form.Moeda.data
        emb.VlTotal     =    form.VlTotal.data
        emb.Merc        =    form.Merc.data
        emb.Vol         =    form.Vol.data
        emb.M3          =   form.M3.data
        emb.Pb          =   form.Pb.data
        emb.Pl          =   form.Pl.data
        emb.Re          =   form.Re.data
        emb.Sd          =   form.Sd.data
        emb.Status      =   form.Status.data
        emb.Obs         =   form.Obs.data
        emb.bl          =   form.bl.data
        emb.nrBl        =   form.nrBl.data
        emb.navio       =   form.navio.data
        emb.vg          =   form.vg.data
        emb.via         =   form.via.data
        emb.eta         =   form.eta.data
        emb.DLDraft     =   form.DLDraft.data
        emb.DLCarga     =   form.DLCarga.data
        emb.ttime       =   form.ttime.data
        emb.dtBL        =   form.dtBL.data
        emb.Importador  =   form.Importador.data
        emb.dcts        =   form.dcts.data
        emb.Operador    =   form.Operador.data
        emb.Booking     =   form.Booking.data
        emb.TipoFrt     =   form.TipoFrt.data
        emb.Saida       =   form.Saida.data
        # emb.abert     =   form.abert.data
        emb.fech        =   form.fech.data
        emb.dtEnvDcts   =   form.dtEnvDcts.data
        emb.lclFcl      =   form.lclFcl.data
        db.session.commit()

# EDITA OS DADOS -------------------------------

    form.RefPartner.data    =   emb.RefPartner
    form.Cliente.data       =   emb.Cliente
    form.RefCliente.data    =   emb.RefCliente
    form.Origem.data        =   emb.Origem
    form.Destino.data       =  emb.Destino
    form.modal.data         =  emb.modal
    form.Incoterm.data      =  emb.Incoterm
    form.Moeda.data         =  emb.Moeda
    form.VlTotal.data       =  emb.VlTotal
    form.Merc.data          =  emb.Merc
    form.Vol.data           =  emb.Vol
    form.M3.data            =  emb.M3
    form.Pb.data            =  emb.Pb
    form.Pl.data            =  emb.Pl
    form.Re.data            =  emb.Re
    form.Sd.data            =  emb.Sd
    form.Status.data        =  emb.Status
    form.Obs.data           =  emb.Obs
    form.bl.data            =  emb.bl
    form.nrBl.data          =  emb.nrBl
    form.navio.data         =  emb.navio
    form.vg.data            =  emb.vg
    form.via.data           =  emb.via
    form.eta.data           =  emb.eta
    form.DLDraft.data       =  emb.DLDraft
    form.DLCarga.data       =  emb.DLCarga
    form.ttime.data         =  emb.ttime
    form.dtBL.data          =  emb.dtBL
    form.Importador.data    =  emb.Importador
    form.dcts.data          =  emb.dcts
    form.Operador.data      =  emb.Operador
    form.Booking.data       =  emb.Booking
    form.TipoFrt.data       =  emb.TipoFrt
    form.Saida.data         =  emb.Saida
    # form.abert.data       =  emb.abert
    form.fech.data          =  emb.fech
    form.dtEnvDcts.data     =  emb.dtEnvDcts
    form.lclFcl.data        =  emb.lclFcl
    return render_template("post.html", post=emb,  form=form,  current_user=current_user)
# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

@app.route("/about")
def about():

    return render_template("about.html", current_user=current_user)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.submitEnviar.data:

        e_mail = Class_email()
        e_mail.send_email(to=form.email.data, subj="Teste e-mail", msg= f'{form.Message.data}  \n \n \n  {form.name.data}')

    return render_template("contact.html", form=form, current_user=current_user)




@app.route("/new-post", methods=["GET", "POST"])
# @admin_only
def add_new_post():

    form = CreatePostForm()
    if form.validate_on_submit():
        new_post =Menu(
            RefPartner=form.RefPartner.data,
            Cliente=form.Cliente.data,
            RefCliente=form.RefCliente.data,
            Origem=form.Origem.data,
            Destino=form.Destino.data,
            modal=form.modal.data
                )

            # date=date.today().strftime("%B %d, %Y")

        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))

    return render_template("make-post.html", form=form, current_user=current_user)




@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):

    post =Menu.query.get(post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=current_user,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))

    return render_template("make-post.html", form=edit_form, is_edit=True, current_user=current_user)


@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):

    post_to_delete =Menu.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=5000)


# ------------------------------------------------------------------------------------------------------


# @app.route("/contact", methods=["GET", "POST"])
# def send_email():
#     formsend =  ContactForm()
#
#     if formsend.submit.data:
#         print("send e-mail")

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------
