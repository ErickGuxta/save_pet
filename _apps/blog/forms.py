from django import forms

from .models import ArtigoBlog, Categoria


class ArtigoBlogForm(forms.ModelForm):
    class Meta:
        model = ArtigoBlog
        fields = ["titulo", "categoria", "conteudo"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

        self.fields["categoria"].widget.attrs.update({"class": "form-select"})


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["nome", "descricao"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})
