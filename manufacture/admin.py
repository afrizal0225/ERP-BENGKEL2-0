from django.contrib import admin
from .models import StasiunKerja, BOM, BOMDetail, ProductionOrder, ProductionOrderDetail, SuratPerintahKerja, SPKDetail, SPKOutput

@admin.register(StasiunKerja)
class StasiunKerjaAdmin(admin.ModelAdmin):
    list_display = ('id_stasiun_kerja', 'nama_stasiun_kerja', 'keterangan')
    search_fields = ('nama_stasiun_kerja',)

@admin.register(BOM)
class BOMAdmin(admin.ModelAdmin):
    list_display = ('id_bom', 'id_product', 'version')
    search_fields = ('id_product__name', 'version')

@admin.register(BOMDetail)
class BOMDetailAdmin(admin.ModelAdmin):
    list_display = ('id_bom', 'id_product', 'nama_product', 'version', 'id_rawmaterial', 'nama_rawmaterial', 'id_stasiunkerja', 'nama_stasiunkerja', 'satuan', 'qty', 'harga_satuanrawmaterial', 'harga_totalrawmaterial')
    list_filter = ('id_bom', 'id_product', 'id_stasiunkerja')
    search_fields = ('nama_product', 'nama_rawmaterial', 'nama_stasiunkerja')
    readonly_fields = ('harga_satuanrawmaterial', 'harga_totalrawmaterial')

@admin.register(ProductionOrder)
class ProductionOrderAdmin(admin.ModelAdmin):
    list_display = ('id_po', 'tanggal_request', 'tanggal_selesai')
    search_fields = ('id_po',)
    list_filter = ('tanggal_request', 'tanggal_selesai')

@admin.register(ProductionOrderDetail)
class ProductionOrderDetailAdmin(admin.ModelAdmin):
    list_display = ('id_po', 'id_product', 'nama_product', 'size', 'warna', 'qty_produksi', 'keterangan')
    list_filter = ('id_po', 'id_product', 'size', 'warna')
    search_fields = ('nama_product', 'keterangan')

@admin.register(SuratPerintahKerja)
class SuratPerintahKerjaAdmin(admin.ModelAdmin):
    list_display = ('id_spk', 'id_po', 'tanggal_spk', 'status', 'keterangan')
    list_filter = ('status', 'tanggal_spk')
    search_fields = ('id_spk', 'id_po__id_po')

@admin.register(SPKDetail)
class SPKDetailAdmin(admin.ModelAdmin):
    list_display = ('id_spk', 'nama_stasiunkerja', 'nama_rawmaterial', 'qty_kebutuhan', 'satuan')
    list_filter = ('id_spk', 'id_stasiunkerja')
    search_fields = ('nama_stasiunkerja', 'nama_rawmaterial')

@admin.register(SPKOutput)
class SPKOutputAdmin(admin.ModelAdmin):
    list_display = ('id_spk', 'nama_stasiunkerja', 'nama_product', 'qty_output')
    list_filter = ('id_spk', 'id_stasiunkerja')
    search_fields = ('nama_stasiunkerja', 'nama_product')
