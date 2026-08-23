from django import forms

from apps.pets.models import Pet
from apps.vaccines.models import Vaccine


class VaccineForm(forms.ModelForm):
    class Meta:
        model = Vaccine
        fields = [
            "nome",
            "lote",
            "data_aplicacao",
            "data_reforco",
            "veterinario",
            "clinica",
            "observacoes",
            "pet",
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user is not None:
            self.fields["pet"].queryset = Pet.objects.filter(usuario=user)

        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

        self.fields["pet"].widget.attrs.update({"class": "form-select"})

        for field_name in ["data_aplicacao", "data_reforco"]:
            self.fields[field_name].input_formats = ["%d/%m/%Y", "%Y-%m-%d"]
            self.fields[field_name].error_messages["invalid"] = "Informe a data no formato dd/mm/aaaa."
            self.fields[field_name].widget = forms.DateInput(
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