from django.contrib import admin
from .models import StasiunKerja, BOM, BOMDetail

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
