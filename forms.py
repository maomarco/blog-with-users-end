from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, DecimalField
from wtforms.validators import DataRequired, URL, NumberRange
from wtforms.widgets import html5 as h5widgets
from flask_ckeditor import CKEditorField


##WTForm
class CreatePostForm(FlaskForm):

    RefPartner = StringField("Nossa Ref:", validators=[DataRequired()])
    Cliente = StringField("Cliente", validators=[DataRequired()])
    RefCliente = StringField("Ref Cliente", validators=[DataRequired()])
    Origem = StringField("Origem")
    Destino = StringField("Destino")
    modal = SelectField("Modal", choices=["","MARITIMO", "AEREO", "RODOVIARIO"])
    submit = SubmitField("Abrir novo processo")


class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")

#     ----------------------------------------------------------
#     ----------------------------------------------------------
class ContactForm(FlaskForm):
    name = StringField("Name", id="Name",validators=[DataRequired()])
    email = StringField("Email", id="Email", validators=[DataRequired()])
    phone = StringField("Phone", id="Phone", validators=[DataRequired()])
    Message = StringField("Message", id="Message", validators=[DataRequired()])
    submitEnviar = SubmitField("Enviar", id="submitEnviar")
#     ----------------------------------------------------------
#     ----------------------------------------------------------

class FormDadosGerais(FlaskForm):
    # id = StringField("id")
    RefPartner = StringField("Nossa Ref:", validators=[DataRequired()])
    Cliente = StringField("Cliente", validators=[DataRequired()])
    RefCliente = StringField("Ref Cliente", validators=[DataRequired()])
    Origem = StringField("Origem")
    Destino = StringField("Destino")
    modal = SelectField("Modal", choices=["","MARITIMO", "AEREO", "RODOVIARIO"])
    Incoterm = SelectField("Incoterm", choices=["","FOB", "CFR", "CIF", "CPT", "CIP", "FAS"])
    Moeda = SelectField("Moeda", choices=["", "USD", "EUR", "JPN"])
    VlTotal = DecimalField("Valor Total", validators = [NumberRange(min=0, max=999999, message= "bbb")])
    Merc = StringField("Mercadoria")
    Vol = StringField("Volume")
    # validators = [NumberRange(0, 1E+20)])
    M3 = DecimalField("M3", default=None )
    Pb = DecimalField("Peso Bruto", default=None)
    Pl = DecimalField("Peso Liquido", default=None)
    Re = StringField("DUE")
    Sd = StringField("RE / DDE")
    Status = StringField("Status")
    Obs = CKEditorField("Obs")
    bl = StringField("ETD (BL Date)")
    nrBl = StringField("Nr do Bl")
    navio = StringField("Navio")
    vg = StringField("Viagem")
    via = StringField("Via")
    eta = StringField("ETA")
    DLDraft = StringField("DL Draft")
    DLCarga = StringField("DL Carga")
    ttime = StringField("Transit Time")
    dtBL = StringField("data do BL")
    Importador = StringField("Importador")
    dcts = StringField("Envio Dcts")
    Operador = StringField("Operador")
    Booking = StringField("Booking")
    TipoFrt = StringField("Tipo do Frt")
    Saida = StringField("ETD")
    # abert = StringField("abert")
    fech = StringField("Fech do Processo")
    dtEnvDcts = StringField("Data Envio  Dcts")
    lclFcl = StringField("LCL / FCL")
    # submit = SubmitField("Salvar")
    submit1 = SubmitField("Salvar", id="DadosGerais")




        #
        # def validate(self):
        #     res = super(FormDadosGerais, self).validate()
        #         def validate(self):
        #         # if isinstance(self.VlTotal, float):
        #



class LoginForm(FlaskForm):

    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")


class CommentForm(FlaskForm):

    comment_text = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Submit Comment")
