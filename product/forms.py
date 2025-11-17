from django import forms
from .models import Product, RawMaterial

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class RawMaterialForm(forms.ModelForm):
    class Meta:
        model = RawMaterial
        fields = '__all__'

class BulkUploadForm(forms.Form):
    file = forms.FileField()