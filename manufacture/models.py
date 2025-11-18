from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from product.models import Product, RawMaterial

class StasiunKerja(models.Model):
    id_stasiun_kerja = models.AutoField(primary_key=True)
    nama_stasiun_kerja = models.CharField(max_length=200)
    keterangan = models.TextField(blank=True)

    def __str__(self):
        return self.nama_stasiun_kerja

class BOM(models.Model):
    id_bom = models.CharField(max_length=50, primary_key=True)
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    version = models.CharField(max_length=50)

    def __str__(self):
        product_name = self.id_product.name if self.id_product else "No Product"
        return f"BOM {self.id_bom} - {product_name} - v{self.version}"

class BOMDetail(models.Model):
    id_bom = models.ForeignKey(BOM, on_delete=models.CASCADE)
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    nama_product = models.CharField(max_length=200, blank=True)
    version = models.CharField(max_length=50)
    id_rawmaterial = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    nama_rawmaterial = models.CharField(max_length=200, blank=True)
    id_stasiunkerja = models.ForeignKey(StasiunKerja, on_delete=models.CASCADE)
    nama_stasiunkerja = models.CharField(max_length=200, blank=True)
    satuan = models.CharField(max_length=50)
    qty = models.DecimalField(max_digits=10, decimal_places=2)
    harga_satuanrawmaterial = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    harga_totalrawmaterial = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.id_bom} - {self.id_product} - {self.id_rawmaterial}"

@receiver(pre_save, sender=BOMDetail)
def set_bomdetail_prices(sender, instance, **kwargs):
    if instance.id_rawmaterial:
        instance.harga_satuanrawmaterial = instance.id_rawmaterial.price
        instance.harga_totalrawmaterial = instance.id_rawmaterial.price * instance.qty
    class Meta:
        unique_together = ('id_bom', 'id_product', 'id_rawmaterial', 'version')
