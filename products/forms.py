# pylint: disable=missing-module-docstring,no-member,missing-class-docstring
# pylint: disable=line-too-long
from django import forms
from .widgets import CustomClearableFileInpit
from .models import Product, Category


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    image = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInpit)  # noqa: E501

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['category'].choices = friendly_names
        # pylint: disable=unused-variable
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
