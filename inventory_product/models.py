from django.db import models
from product.models import Product

class PenerimaanBarang(models.Model):
    id_penerimaan = models.CharField(max_length=100, primary_key=True)
    id_supplier = models.CharField(max_length=100)
    tanggal_terima = models.DateField()
    keterangan = models.TextField(blank=True)

    def __str__(self):
        return self.id_penerimaan

    @property
    def total_quantity(self):
        return self.penerimaanbarangdetail_set.aggregate(total=models.Sum('quantity'))['total'] or 0

class PenerimaanBarangDetail(models.Model):
    id_penerimaan = models.ForeignKey(PenerimaanBarang, on_delete=models.CASCADE)
    tanggal_terima = models.DateField()
    Supplier = models.CharField(max_length=200)
    BRAND = models.CharField(max_length=100)
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    Nama_product = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    satuan = models.CharField(max_length=50)
    harga_satuan = models.DecimalField(max_digits=10, decimal_places=2)
    harga_total = models.DecimalField(max_digits=10, decimal_places=2)
    kategori = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.id_penerimaan} - {self.Nama_product}"

class KeluarBarang(models.Model):
    id_keluar = models.CharField(max_length=100, primary_key=True)
    tanggal_keluar = models.DateField()
    keterangan = models.TextField(blank=True)

    def __str__(self):
        return self.id_keluar

    @property
    def total_quantity(self):
        return self.keluarbarangdetail_set.aggregate(total=models.Sum('quantity'))['total'] or 0

class KeluarBarangDetail(models.Model):
    id_keluar = models.ForeignKey(KeluarBarang, on_delete=models.CASCADE)
    tanggal_keluar = models.DateField()
    BRAND = models.CharField(max_length=100)
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    Nama_product = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    harga_satuan = models.DecimalField(max_digits=10, decimal_places=2)
    harga_total = models.DecimalField(max_digits=10, decimal_places=2)
    kategori = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.id_keluar} - {self.Nama_product}"

class InventoryProduct(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)

    @property
    def current_stock(self):
        total_in = PenerimaanBarangDetail.objects.filter(id_product=self.product).aggregate(total=models.Sum('quantity'))['total'] or 0
        total_out = KeluarBarangDetail.objects.filter(id_product=self.product).aggregate(total=models.Sum('quantity'))['total'] or 0
        return total_in - total_out

    def __str__(self):
        return f"Inventory for {self.product.name}"

# Raw Material Models
class PenerimaanRawMaterial(models.Model):
    id_penerimaan = models.CharField(max_length=100, primary_key=True)
    id_supplier = models.CharField(max_length=100)
    tanggal_terima = models.DateField()
    keterangan = models.TextField(blank=True)

    def __str__(self):
        return self.id_penerimaan

    @property
    def total_quantity(self):
        return self.penerimaanrawmaterialdetail_set.aggregate(total=models.Sum('quantity'))['total'] or 0

class PenerimaanRawMaterialDetail(models.Model):
    id_penerimaan = models.ForeignKey(PenerimaanRawMaterial, on_delete=models.CASCADE)
    tanggal_terima = models.DateField()
    Supplier = models.CharField(max_length=200)
    BRAND = models.CharField(max_length=100)
    id_rawmaterial = models.ForeignKey('product.RawMaterial', on_delete=models.CASCADE)
    Nama_rawmaterial = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    satuan = models.CharField(max_length=50)
    harga_satuan = models.DecimalField(max_digits=10, decimal_places=2)
    harga_total = models.DecimalField(max_digits=10, decimal_places=2)
    kategori = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.id_penerimaan} - {self.Nama_rawmaterial}"

class KeluarRawMaterial(models.Model):
    id_keluar = models.CharField(max_length=100, primary_key=True)
    tanggal_keluar = models.DateField()
    keterangan = models.TextField(blank=True)

    def __str__(self):
        return self.id_keluar

    @property
    def total_quantity(self):
        return self.keluarrawmaterialdetail_set.aggregate(total=models.Sum('quantity'))['total'] or 0

class KeluarRawMaterialDetail(models.Model):
    id_keluar = models.ForeignKey(KeluarRawMaterial, on_delete=models.CASCADE)
    tanggal_keluar = models.DateField()
    BRAND = models.CharField(max_length=100)
    id_rawmaterial = models.ForeignKey('product.RawMaterial', on_delete=models.CASCADE)
    Nama_rawmaterial = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    harga_satuan = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    harga_total = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    kategori = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        self.harga_satuan = self.id_rawmaterial.price
        self.harga_total = self.quantity * self.harga_satuan
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id_keluar} - {self.Nama_rawmaterial}"

class InventoryRawMaterial(models.Model):
    rawmaterial = models.OneToOneField('product.RawMaterial', on_delete=models.CASCADE)

    @property
    def current_stock(self):
        total_in = PenerimaanRawMaterialDetail.objects.filter(id_rawmaterial=self.rawmaterial).aggregate(total=models.Sum('quantity'))['total'] or 0
        total_out = KeluarRawMaterialDetail.objects.filter(id_rawmaterial=self.rawmaterial).aggregate(total=models.Sum('quantity'))['total'] or 0
        return total_in - total_out

    def __str__(self):
        return f"Inventory for {self.rawmaterial.name}"
