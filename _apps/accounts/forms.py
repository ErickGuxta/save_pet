# ============================================================
# Imports
# ============================================================

# importando forms do Django e formulários prontos de autenticação
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

# importando model de perfil do tutor
from _apps.accounts.models import Usuario

User = get_user_model()


# ============================================================
# Cadastro público de usuário
# ============================================================

class PublicUserForm(UserCreationForm):
    # campos extras do User padrão que aparecem no cadastro
    first_name = forms.CharField(label="Nome", max_length=150)
    email = forms.EmailField(label="E-mail")

    class Meta:
        model = User
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
# Perfil do tutor
# ============================================================

class PerfilUsuarioForm(forms.Form):
    # campos do User
    nome = forms.CharField(max_length=150)
    email = forms.EmailField()

    # campos do perfil Usuario
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
        super().__init__(*args, **kwargs)

        if user is not None:
            # preenche o formulário com dados do User e do perfil Usuario
            perfil, _ = Usuario.objects.get_or_create(user=user)
            self.fields["nome"].initial = user.first_name
            self.fields["email"].initial = user.email
            self.fields["cpf"].initial = perfil.cpf
            self.fields["telefone"].initial = perfil.telefone
            self.fields["cep"].initial = perfil.cep
            self.fields["logradouro"].initial = perfil.logradouro
            self.fields["numero"].initial = perfil.numero
            self.fields["complemento"].initial = perfil.complemento
            self.fields["bairro"].initial = perfil.bairro
            self.fields["cidade"].initial = perfil.cidade
            self.fields["estado"].initial = perfil.estado

        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

