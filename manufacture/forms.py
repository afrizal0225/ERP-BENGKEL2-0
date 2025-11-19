from django import forms
from .models import StasiunKerja, BOM, BOMDetail, ProductionOrder, ProductionOrderDetail, SuratPerintahKerja, ProductionProgress
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

class AllocationForm(forms.Form):
    po_detail_id = forms.IntegerField(widget=forms.HiddenInput)
    allocated_qty = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0)

class SuratPerintahKerjaForm(forms.ModelForm):
    class Meta:
        model = SuratPerintahKerja
        fields = ['id_spk', 'id_po', 'tanggal_spk', 'keterangan']
        widgets = {
            'tanggal_spk': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter POs that have details with remaining > 0
        from .models import ProductionOrderDetail
        po_with_remaining = ProductionOrderDetail.objects.filter(qty_remaining__gt=0).values_list('id_po', flat=True).distinct()
        self.fields['id_po'].queryset = self.fields['id_po'].queryset.filter(id_po__in=po_with_remaining)

class ProductionProgressForm(forms.ModelForm):
    class Meta:
        model = ProductionProgress
        fields = ['id_spk', 'id_stasiunkerja', 'id_product', 'tanggal_mulai', 'tanggal_selesai', 'qty_selesai']
        widgets = {
            'tanggal_mulai': forms.DateInput(attrs={'type': 'date'}),
            'tanggal_selesai': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter SPKs that are approved
        self.fields['id_spk'].queryset = self.fields['id_spk'].queryset.filter(status='Approved')
        # For update, filter products based on instance SPK
        if self.instance.pk:
            from .models import SPKOutput
            products = SPKOutput.objects.filter(id_spk=self.instance.id_spk).values_list('id_product', flat=True)
            self.fields['id_product'].queryset = self.fields['id_product'].queryset.filter(pk__in=products)
