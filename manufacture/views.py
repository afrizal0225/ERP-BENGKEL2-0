from django.shortcuts import render, get_object_or_404, redirect
from .models import StasiunKerja, BOM, BOMDetail, ProductionOrder, ProductionOrderDetail, SuratPerintahKerja, SPKDetail, SPKOutput
from product.models import Product, RawMaterial
from .forms import StasiunKerjaForm, BOMForm, BOMDetailForm, BulkUploadForm, ProductionOrderForm, ProductionOrderDetailForm, SuratPerintahKerjaForm
from django.contrib import messages
import openpyxl
from datetime import datetime
from openpyxl import Workbook
from django.http import HttpResponse
from django.db.models import Sum

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

def productionorder_list(request):
    productionorders = ProductionOrder.objects.all()
    return render(request, 'manufacture/productionorder_list.html', {'productionorders': productionorders})


def productionorder_update(request, pk):
    productionorder = get_object_or_404(ProductionOrder, pk=pk)
    if request.method == 'POST':
        form = ProductionOrderForm(request.POST, instance=productionorder)
        if form.is_valid():
            form.save()
            messages.success(request, 'Production Order updated successfully.')
            return redirect('productionorder_list')
    else:
        form = ProductionOrderForm(instance=productionorder)
    return render(request, 'manufacture/productionorder_form.html', {'form': form, 'title': 'Update Production Order'})

def productionorder_delete(request, pk):
    productionorder = get_object_or_404(ProductionOrder, pk=pk)
    if request.method == 'POST':
        productionorder.delete()
        messages.success(request, 'Production Order deleted successfully.')
        return redirect('productionorder_list')
    return render(request, 'manufacture/productionorder_confirm_delete.html', {'productionorder': productionorder})

def productionorder_detail(request, pk):
    productionorder = get_object_or_404(ProductionOrder, pk=pk)
    details = ProductionOrderDetail.objects.filter(id_po=productionorder)
    return render(request, 'manufacture/productionorder_detail.html', {'productionorder': productionorder, 'details': details})

def productionorderdetail_create(request, po_pk):
    productionorder = get_object_or_404(ProductionOrder, pk=po_pk)
    if request.method == 'POST':
        form = ProductionOrderDetailForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['id_product']
            # Check if product has BOM
            if not BOM.objects.filter(id_product=product).exists():
                messages.error(request, f"Cannot create Production Order Detail: Product '{product.name}' (SKU: {product.sku}) does not have a BOM. Production Orders can only be created for products with existing BOMs.")
                return render(request, 'manufacture/productionorderdetail_form.html', {'form': form, 'productionorder': productionorder, 'title': 'Create Production Order Detail'})

            detail = form.save(commit=False)
            detail.id_po = productionorder
            detail.save()
            messages.success(request, 'Production Order Detail created successfully.')
            return redirect('productionorder_detail', pk=po_pk)
    else:
        form = ProductionOrderDetailForm()
    return render(request, 'manufacture/productionorderdetail_form.html', {'form': form, 'productionorder': productionorder, 'title': 'Create Production Order Detail'})

def productionorderdetail_update(request, pk):
    detail = get_object_or_404(ProductionOrderDetail, pk=pk)
    if request.method == 'POST':
        form = ProductionOrderDetailForm(request.POST, instance=detail)
        if form.is_valid():
            form.save()
            messages.success(request, 'Production Order Detail updated successfully.')
            return redirect('productionorder_detail', pk=detail.id_po.pk)
    else:
        form = ProductionOrderDetailForm(instance=detail)
    return render(request, 'manufacture/productionorderdetail_form.html', {'form': form, 'productionorder': detail.id_po, 'title': 'Update Production Order Detail'})

def productionorderdetail_delete(request, pk):
    detail = get_object_or_404(ProductionOrderDetail, pk=pk)
    po_pk = detail.id_po.pk
    if request.method == 'POST':
        detail.delete()
        messages.success(request, 'Production Order Detail deleted successfully.')
        return redirect('productionorder_detail', pk=po_pk)
    return render(request, 'manufacture/productionorderdetail_confirm_delete.html', {'detail': detail})

def productionorder_bulk_create(request):
    if request.method == 'POST':
        form = BulkUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            try:
                wb = openpyxl.load_workbook(file)
                sheet = wb.active
                created_count = 0
                for row in sheet.iter_rows(min_row=2, values_only=True):
                    if len(row) < 9:
                        continue
                    po_id, tanggal_request, tanggal_selesai, product_sku, nama_product, size, warna, qty_produksi, keterangan = row[:9]
                    try:
                        # Parse dates
                        if isinstance(tanggal_request, str):
                            tanggal_request = datetime.strptime(tanggal_request, '%Y-%m-%d').date()
                        if isinstance(tanggal_selesai, str):
                            tanggal_selesai = datetime.strptime(tanggal_selesai, '%Y-%m-%d').date()

                        product = Product.objects.get(sku=product_sku)

                        # Check if product has BOM
                        if not BOM.objects.filter(id_product=product).exists():
                            messages.error(request, f"Product with SKU {product_sku} does not have a BOM. Production Orders can only be created for products with existing BOMs.")
                            continue

                        po, po_created = ProductionOrder.objects.get_or_create(
                            id_po=po_id,
                            defaults={
                                'tanggal_request': tanggal_request,
                                'tanggal_selesai': tanggal_selesai
                            }
                        )
                        ProductionOrderDetail.objects.get_or_create(
                            id_po=po,
                            id_product=product,
                            defaults={
                                'nama_product': nama_product or '',
                                'size': size or '',
                                'warna': warna or '',
                                'qty_produksi': qty_produksi,
                                'keterangan': keterangan or '',
                            }
                        )
                        created_count += 1
                    except Product.DoesNotExist:
                        messages.error(request, f"Product with SKU {product_sku} not found")
                    except Exception as e:
                        messages.error(request, f"Error creating Production Order Detail: {e}")
                messages.success(request, f'Bulk upload completed. {created_count} Production Order Details created.')
            except Exception as e:
                messages.error(request, f"Error processing file: {e}")
            return redirect('productionorder_list')
    else:
        form = BulkUploadForm()
    return render(request, 'manufacture/productionorder_bulk_form.html', {'form': form, 'title': 'Bulk Upload Production Orders'})

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

def download_productionorder_template(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Production Order"
    headers = ['PO ID', 'Tanggal Request', 'Tanggal Selesai', 'Product SKU', 'Nama Product', 'Size', 'Warna', 'Qty Produksi', 'Keterangan']
    ws.append(headers)
    # Sample row
    ws.append(['PO001', '2024-01-15', '2024-01-20', 'PROD001', 'Sample Product', 'M', 'Red', '100', 'Urgent order'])

    # Sheet for existing products that have BOMs
    ws_products = wb.create_sheet("Products_Exist")
    ws_products.append(['Product SKU', 'Nama Product', 'Size', 'Colour', 'BOM Version'])
    # Only include products that have BOMs
    products_with_bom = Product.objects.filter(bom__isnull=False).distinct()
    for product in products_with_bom:
        # Get the latest BOM version for this product
        latest_bom = BOM.objects.filter(id_product=product).order_by('-version').first()
        bom_version = latest_bom.version if latest_bom else ''
        ws_products.append([product.sku, product.name, product.size, product.colour, bom_version])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=productionorder_template.xlsx'
    wb.save(response)
    return response

def spk_list(request):
    spks = SuratPerintahKerja.objects.all()
    return render(request, 'manufacture/spk_list.html', {'spks': spks})

def spk_create(request):
    if request.method == 'POST':
        form = SuratPerintahKerjaForm(request.POST)
        if form.is_valid():
            spk = form.save()
            # Generate SPK details and outputs
            generate_spk_details(spk)
            messages.success(request, 'SPK created successfully with generated details.')
            return redirect('spk_detail', pk=spk.pk)
    else:
        form = SuratPerintahKerjaForm()
    return render(request, 'manufacture/spk_form.html', {'form': form, 'title': 'Create SPK'})

def spk_detail(request, pk):
    spk = get_object_or_404(SuratPerintahKerja, pk=pk)
    details = SPKDetail.objects.filter(id_spk=spk)
    outputs = SPKOutput.objects.filter(id_spk=spk)
    return render(request, 'manufacture/spk_detail.html', {'spk': spk, 'details': details, 'outputs': outputs})

def spk_delete(request, pk):
    spk = get_object_or_404(SuratPerintahKerja, pk=pk)
    if request.method == 'POST':
        spk.delete()
        messages.success(request, 'SPK deleted successfully.')
        return redirect('spk_list')
    return render(request, 'manufacture/spk_confirm_delete.html', {'spk': spk})

def generate_spk_details(spk):
    po = spk.id_po
    po_details = ProductionOrderDetail.objects.filter(id_po=po)

    # Dictionary to accumulate raw material needs per station
    raw_material_needs = {}
    # Set to collect unique stations per product
    stations_per_product = {}

    for po_detail in po_details:
        product = po_detail.id_product
        qty_produksi = po_detail.qty_produksi

        # Get BOM for the product
        bom = BOM.objects.filter(id_product=product).first()
        if not bom:
            continue

        bom_details = BOMDetail.objects.filter(id_bom=bom)

        for bom_detail in bom_details:
            station = bom_detail.id_stasiunkerja
            rawmaterial = bom_detail.id_rawmaterial
            qty_needed = bom_detail.qty * qty_produksi

            key = (station.id_stasiun_kerja, rawmaterial.sku)
            if key not in raw_material_needs:
                raw_material_needs[key] = {
                    'station': station,
                    'rawmaterial': rawmaterial,
                    'qty': 0,
                    'satuan': bom_detail.satuan
                }
            raw_material_needs[key]['qty'] += qty_needed

            # Collect unique stations for this product
            if product.sku not in stations_per_product:
                stations_per_product[product.sku] = {'product': product, 'qty_produksi': qty_produksi, 'stations': set()}
            stations_per_product[product.sku]['stations'].add(station)

    # Create SPKDetail instances
    for key, data in raw_material_needs.items():
        SPKDetail.objects.create(
            id_spk=spk,
            id_stasiunkerja=data['station'],
            nama_stasiunkerja=data['station'].nama_stasiun_kerja,
            id_rawmaterial=data['rawmaterial'],
            nama_rawmaterial=data['rawmaterial'].name,
            qty_kebutuhan=data['qty'],
            satuan=data['satuan']
        )

    # Create SPKOutput instances - each station produces the full qty_produksi for the product
    for product_data in stations_per_product.values():
        product = product_data['product']
        qty_produksi = product_data['qty_produksi']
        for station in product_data['stations']:
            SPKOutput.objects.create(
                id_spk=spk,
                id_stasiunkerja=station,
                nama_stasiunkerja=station.nama_stasiun_kerja,
                id_product=product,
                nama_product=product.name,
                qty_output=qty_produksi
            )
