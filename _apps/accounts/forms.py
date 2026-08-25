# ============================================================
# Imports
# ============================================================

# importando forms do Django e formulários prontos de autenticação
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from _apps.accounts.models import Dono


# ============================================================
# Cadastro público de dono
# ============================================================

class PublicUserForm(UserCreationForm):
    # campos extras do User padrão que aparecem no cadastro
    first_name = forms.CharField(label="Nome", max_length=150)
    email = forms.EmailField(label="E-mail")

    class Meta:
        model = Dono
        fields = [
            "username",
            "first_name",
            "email",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # adiciona bootstrap nos campos do formulário
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


# ============================================================
# Login
# ============================================================

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # adiciona bootstrap nos campos do formulário de login
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


# ============================================================
# Dados do tutor
# ============================================================

class PerfilDonoForm(forms.Form):
    # campos do User
    nome = forms.CharField(max_length=150)
    email = forms.EmailField()

    # campos cadastrais do Dono
    cpf = forms.CharField(label="CPF", max_length=14, required=False)
    telefone = forms.CharField(max_length=20, required=False)
    cep = forms.CharField(label="CEP", max_length=9, required=False)
    logradouro = forms.CharField(max_length=150, required=False)
    numero = forms.CharField(max_length=20, required=False)
    complemento = forms.CharField(max_length=100, required=False)
    bairro = forms.CharField(max_length=100, required=False)
    cidade = forms.CharField(max_length=100, required=False)
    estado = forms.CharField(max_length=2, required=False)

    def __init__(self, *args, **kwargs):
        # o user é enviado pela view para carregar os dados já cadastrados
        user = kwargs.pop("user", None)
        dono = kwargs.pop("dono", None)
        super().__init__(*args, **kwargs)

        if user is not None:
            self.fields["nome"].initial = user.first_name
            self.fields["email"].initial = user.email

        if dono is not None:
            self.fields["cpf"].initial = dono.cpf
            self.fields["telefone"].initial = dono.telefone
            self.fields["cep"].initial = dono.cep
            self.fields["logradouro"].initial = dono.logradouro
            self.fields["numero"].initial = dono.numero
            self.fields["complemento"].initial = dono.complemento
            self.fields["bairro"].initial = dono.bairro
            self.fields["cidade"].initial = dono.cidade
            self.fields["estado"].initial = dono.estado

        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})
