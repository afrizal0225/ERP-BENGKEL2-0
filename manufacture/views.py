from django.shortcuts import render, get_object_or_404, redirect
from .models import StasiunKerja, BOM, BOMDetail
from product.models import Product, RawMaterial
from .forms import StasiunKerjaForm, BOMForm, BOMDetailForm, BulkUploadForm
from django.contrib import messages
import openpyxl
from datetime import datetime
from openpyxl import Workbook
from django.http import HttpResponse

def stasiunkerja_list(request):
    stasiunkers = StasiunKerja.objects.all()
    return render(request, 'manufacture/stasiunkerja_list.html', {'stasiunkers': stasiunkers})

def stasiunkerja_create(request):
    if request.method == 'POST':
        form = StasiunKerjaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stasiun Kerja created successfully.')
            return redirect('stasiunkerja_list')
    else:
        form = StasiunKerjaForm()
    return render(request, 'manufacture/stasiunkerja_form.html', {'form': form, 'title': 'Create Stasiun Kerja'})

def stasiunkerja_update(request, pk):
    stasiunker = get_object_or_404(StasiunKerja, pk=pk)
    if request.method == 'POST':
        form = StasiunKerjaForm(request.POST, instance=stasiunker)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stasiun Kerja updated successfully.')
            return redirect('stasiunkerja_list')
    else:
        form = StasiunKerjaForm(instance=stasiunker)
    return render(request, 'manufacture/stasiunkerja_form.html', {'form': form, 'title': 'Update Stasiun Kerja'})

def stasiunkerja_delete(request, pk):
    stasiunker = get_object_or_404(StasiunKerja, pk=pk)
    if request.method == 'POST':
        stasiunker.delete()
        messages.success(request, 'Stasiun Kerja deleted successfully.')
        return redirect('stasiunkerja_list')
    return render(request, 'manufacture/stasiunkerja_confirm_delete.html', {'stasiunker': stasiunker})

def stasiunkerja_bulk_create(request):
    if request.method == 'POST':
        form = BulkUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            try:
                wb = openpyxl.load_workbook(file)
                sheet = wb.active
                created_count = 0
                for row in sheet.iter_rows(min_row=2, values_only=True):
                    if len(row) < 2:
                        continue
                    nama_stasiun_kerja, keterangan = row[:2]
                    try:
                        StasiunKerja.objects.create(
                            nama_stasiun_kerja=nama_stasiun_kerja,
                            keterangan=keterangan or '',
                        )
                        created_count += 1
                    except Exception as e:
                        messages.error(request, f"Error creating stasiun kerja {nama_stasiun_kerja}: {e}")
                messages.success(request, f'Bulk upload completed. {created_count} stasiun kerja created.')
            except Exception as e:
                messages.error(request, f"Error processing file: {e}")
            return redirect('stasiunkerja_list')
    else:
        form = BulkUploadForm()
    return render(request, 'manufacture/stasiunkerja_bulk_form.html', {'form': form, 'title': 'Bulk Upload Stasiun Kerja'})

def bom_list(request):
    boms = BOM.objects.all()
    return render(request, 'manufacture/bom_list.html', {'boms': boms})

def bom_create(request):
    if request.method == 'POST':
        form = BOMForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'BOM created successfully.')
            return redirect('bom_list')
    else:
        form = BOMForm()
    return render(request, 'manufacture/bom_form.html', {'form': form, 'title': 'Create BOM'})

def bom_update(request, pk):
    bom = get_object_or_404(BOM, pk=pk)
    details = BOMDetail.objects.filter(id_bom=bom)
    rawmaterials = RawMaterial.objects.all()
    stasiunkers = StasiunKerja.objects.all()
    return render(request, 'manufacture/bom_update.html', {
        'bom': bom,
        'details': details,
        'rawmaterials': rawmaterials,
        'stasiunkers': stasiunkers,
        'title': 'Update BOM Details'
    })

def bom_delete(request, pk):
    bom = get_object_or_404(BOM, pk=pk)
    if request.method == 'POST':
        bom.delete()
        messages.success(request, 'BOM deleted successfully.')
        return redirect('bom_list')
    return render(request, 'manufacture/bom_confirm_delete.html', {'bom': bom})

def bom_detail(request, pk):
    bom = get_object_or_404(BOM, pk=pk)
    details = BOMDetail.objects.filter(id_bom=bom)
    total_hpp = sum(detail.harga_totalrawmaterial for detail in details)
    return render(request, 'manufacture/bom_detail.html', {'bom': bom, 'details': details, 'total_hpp': total_hpp})

def bom_bulk_create(request):
    if request.method == 'POST':
        form = BulkUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            try:
                wb = openpyxl.load_workbook(file)
                sheet = wb.active
                created_count = 0
                for row in sheet.iter_rows(min_row=2, values_only=True):
                    if len(row) < 10:
                        continue
                    bom_id, product_sku, nama_product, version, rawmaterial_sku, nama_rawmaterial, stasiunkerja_id, nama_stasiunkerja, satuan, qty = row[:10]
                    try:
                        product = Product.objects.get(sku=product_sku)
                        bom, bom_created = BOM.objects.get_or_create(
                            id_bom=bom_id,
                            defaults={'id_product': product, 'version': version}
                        )
                        rawmaterial = RawMaterial.objects.get(sku=rawmaterial_sku)
                        stasiunkerja = StasiunKerja.objects.get(id_stasiun_kerja=stasiunkerja_id)
                        BOMDetail.objects.get_or_create(
                            id_bom=bom,
                            id_product=product,
                            version=version,
                            id_rawmaterial=rawmaterial,
                            defaults={
                                'nama_product': nama_product or '',
                                'nama_rawmaterial': nama_rawmaterial or '',
                                'id_stasiunkerja': stasiunkerja,
                                'nama_stasiunkerja': nama_stasiunkerja or '',
                                'satuan': satuan,
                                'qty': qty,
                                'harga_satuanrawmaterial': rawmaterial.price,
                                'harga_totalrawmaterial': rawmaterial.price * qty,
                            }
                        )
                        created_count += 1
                    except Product.DoesNotExist:
                        messages.error(request, f"Product with SKU {product_sku} not found")
                    except RawMaterial.DoesNotExist:
                        messages.error(request, f"Raw Material with SKU {rawmaterial_sku} not found")
                    except StasiunKerja.DoesNotExist:
                        messages.error(request, f"Stasiun Kerja with ID {stasiunkerja_id} not found")
                    except Exception as e:
                        messages.error(request, f"Error creating BOM Detail: {e}")
                messages.success(request, f'Bulk upload completed. {created_count} BOM Details created.')
            except Exception as e:
                messages.error(request, f"Error processing file: {e}")
            return redirect('bom_list')
    else:
        form = BulkUploadForm()
    return render(request, 'manufacture/bom_bulk_form.html', {'form': form, 'title': 'Bulk Upload BOM Details'})

def download_stasiunkerja_template(request):
    wb = Workbook()
def bomdetail_update(request, pk):
    bomdetail = get_object_or_404(BOMDetail, pk=pk)
    if request.method == 'POST':
        form = BOMDetailForm(request.POST, instance=bomdetail)
        if form.is_valid():
            form.save()
            messages.success(request, 'BOM Detail updated successfully.')
            return redirect('bom_update', pk=bomdetail.id_bom.pk)
    else:
        form = BOMDetailForm(instance=bomdetail)
    return render(request, 'manufacture/bomdetail_form.html', {'form': form, 'title': 'Update BOM Detail'})

def bomdetail_delete(request, pk):
    bomdetail = get_object_or_404(BOMDetail, pk=pk)
    bom_pk = bomdetail.id_bom.pk
    if request.method == 'POST':
        bomdetail.delete()
        messages.success(request, 'BOM Detail deleted successfully.')
        return redirect('bom_update', pk=bom_pk)
    return render(request, 'manufacture/bomdetail_confirm_delete.html', {'bomdetail': bomdetail})

    ws = wb.active
    ws.title = "Stasiun Kerja"
    headers = ['Nama Stasiun Kerja', 'Keterangan']
    ws.append(headers)
    # Sample row
    ws.append(['Assembly Line 1', 'Main assembly station'])
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=stasiunkerja_template.xlsx'
    wb.save(response)
    return response

def download_bom_template(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "BOM"
    headers = ['BOM ID', 'Product SKU', 'Nama Product', 'Version', 'Raw Material SKU', 'Nama Raw Material', 'Stasiun Kerja ID', 'Nama Stasiun Kerja', 'Satuan', 'Qty']
    ws.append(headers)
    # Sample row
    ws.append(['BOM001', 'PROD001', 'Sample Product', '1.0', 'RAW001', 'Sample Raw Material', '1', 'Sample Stasiun Kerja', 'pcs', '10.5'])

    # Sheet for existing products
    ws_products = wb.create_sheet("Products_Exist")
    ws_products.append(['Product SKU', 'Nama Product'])
    for product in Product.objects.all():
        ws_products.append([product.sku, product.name])

    # Sheet for existing raw materials
    ws_rawmaterials = wb.create_sheet("RawMaterials_Exist")
    ws_rawmaterials.append(['Raw Material SKU', 'Nama Raw Material','Category'])
    for rawmaterial in RawMaterial.objects.all():
        ws_rawmaterials.append([rawmaterial.sku, rawmaterial.name, rawmaterial.category])
    # Sheet for existing stasiun kerja
    ws_stasiun = wb.create_sheet("StasiunKerja_Exist")
    ws_stasiun.append(['Stasiun Kerja ID', 'Nama Stasiun Kerja'])
    for stasiun in StasiunKerja.objects.all():
        ws_stasiun.append([stasiun.id_stasiun_kerja, stasiun.nama_stasiun_kerja])


    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=bom_template.xlsx'
    wb.save(response)
    return response
