from django import forms

#importar model de pets
from _apps.pets.models import Pet


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = [
            "nome",
            "especie",
            "raca",
            "sexo",
            "data_nascimento",
            "pelagem",
            "peso",
            "foto",
            "alergias",
            "doencas",
            "medicamentos",
            "observacoes",
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

        for field_name in ["especie", "sexo"]:
            self.fields[field_name].widget.attrs.update({"class": "form-select"})

        self.fields["data_nascimento"].input_formats = ["%d/%m/%Y", "%Y-%m-%d"]
        self.fields["data_nascimento"].error_messages["invalid"] = "Informe a data no formato dd/mm/aaaa."
        self.fields["data_nascimento"].widget = forms.DateInput(
            format="%d/%m/%Y",
            attrs={
                "class": "form-control date-br-input",
                "data-date-br": "true",
                "inputmode": "numeric",
                "maxlength": "10",
                "pattern": r"\d{2}/\d{2}/\d{4}",
                "placeholder": "dd/mm/aaaa",
                "autocomplete": "off",
            },
        )
