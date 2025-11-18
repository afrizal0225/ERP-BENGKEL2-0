from django import forms
from .models import StasiunKerja, BOM, BOMDetail

class StasiunKerjaForm(forms.ModelForm):
    class Meta:
        model = StasiunKerja
        fields = '__all__'

class BOMForm(forms.ModelForm):
    class Meta:
        model = BOM
        fields = ['id_product', 'version']

class BOMDetailForm(forms.ModelForm):
    class Meta:
        model = BOMDetail
        fields = ['id_bom', 'id_product', 'nama_product', 'version', 'id_rawmaterial', 'nama_rawmaterial', 'id_stasiunkerja', 'nama_stasiunkerja', 'satuan', 'qty']

class BulkUploadForm(forms.Form):
    file = forms.FileField()