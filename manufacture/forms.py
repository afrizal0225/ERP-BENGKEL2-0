from django import forms
from .models import StasiunKerja, BOM, BOMDetail, ProductionOrder, ProductionOrderDetail, SuratPerintahKerja
from product.models import Product

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

class ProductionOrderForm(forms.ModelForm):
    class Meta:
        model = ProductionOrder
        fields = '__all__'
        widgets = {
            'tanggal_request': forms.DateInput(attrs={'type': 'date'}),
            'tanggal_selesai': forms.DateInput(attrs={'type': 'date'}),
        }

class ProductionOrderDetailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show products that have BOMs
        self.fields['id_product'].queryset = Product.objects.filter(bom__isnull=False).distinct()

    class Meta:
        model = ProductionOrderDetail
        fields = '__all__'

class SuratPerintahKerjaForm(forms.ModelForm):
    class Meta:
        model = SuratPerintahKerja
        fields = ['id_spk', 'id_po', 'tanggal_spk', 'keterangan']
        widgets = {
            'tanggal_spk': forms.DateInput(attrs={'type': 'date'}),
        }
