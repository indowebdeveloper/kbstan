from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator

import json

from .models import CarBrand, CarType

@login_required
@permission_required('cars.view_carbrand', raise_exception=True)
def cars(request):
    car_brands = CarBrand.objects.all()

    paginator = Paginator(car_brands, 30)
    page_number = request.GET.get('page')
    car_brands = paginator.get_page(page_number)

    return render(request, 'cars.html', {'car_brands': car_brands})

@login_required
@permission_required('cars.view_carbrand', raise_exception=True)
def carBrandCreate(request):
    newData = json.loads(request.body)
    brandName = newData['brandName']
    carBrand, isCreated = CarBrand.objects.get_or_create(brand=brandName)

    if isCreated:
        return JsonResponse({'brandName': carBrand.brand,
                                'brandID': carBrand.id,
                                'status': 'Car brand created'})
    else:
        return JsonResponse({'status': 'Car brand already exists'})

@login_required
@permission_required('cars.view_carbrand', raise_exception=True)
def carModelCreate(request):
    newData = json.loads(request.body)
    modelName = newData['modelName']
    brandID = newData['brandID']
    modelBuildYear = newData['modelBuildYear']
    modelDetails = newData['modelDetails']
    carModel, isCreated = CarType.objects.get_or_create(type=modelName, 
                                                        defaults={
                                                            'type': modelName,
                                                            'buildYear': modelBuildYear,
                                                            'details': modelDetails
                                                        }) 
    if isCreated:
        carModel.carBrand = CarBrand.objects.get(id=brandID)
        carModel.save()
        return JsonResponse({'modelName': carModel.type,
                                'modelID': carModel.id,
                                'modelBuildYear': carModel.buildYear,
                                'modelDetails': carModel.details,
                                'status': 'Car model created'})
    else:
        return JsonResponse({'status': 'Car model already exists'})

@login_required
@permission_required('cars.view_carbrand', raise_exception=True)
def carBrandUpdate(request):
    newData = json.loads(request.body)
    brandID = newData['brandID']
    brandNewName = newData['brandName']
    carBrand = CarBrand.objects.get(id=brandID)
    carBrand.brand = brandNewName
    carBrand.save()

    return JsonResponse({'brandName': carBrand.brand,
                            'brandID': carBrand.id,
                            'status': 'Car brand updated'})

@login_required
@permission_required('cars.view_carbrand', raise_exception=True)
def carModelUpdate(request):
    newData = json.loads(request.body)
    modelID = newData['modelID']
    modelName = newData['modelName']
    modelBuildYear = newData['modelBuildYear']
    modelDetails = newData['modelDetails']
    
    carModel = CarType.objects.get(id=modelID)
    carModel.type = modelName
    carModel.buildYear = modelBuildYear
    carModel.details = modelDetails
    carModel.save()

    return JsonResponse({'modelName': carModel.type,
                            'modelID': carModel.id,
                            'modelBuildYear': carModel.buildYear,
                            'modelDetails': carModel.details,
                            'status': 'Car model updated'})

@login_required
@permission_required('cars.view_carbrand', raise_exception=True)
def carBrandDelete(request):
    newData = json.loads(request.body)
    brandID = newData['brandID']
    carBrand = CarBrand.objects.get(id=brandID)
    carBrand.delete()

    return JsonResponse({'brandID': carBrand.id,
                            'status': 'Car brand has been deleted'})

@login_required
@permission_required('cars.view_carbrand', raise_exception=True)
def carModelDelete(request):
    newData = json.loads(request.body)
    modelID = newData['modelID']
    carModel = CarType.objects.get(id=modelID)
    carModel.delete()

    return JsonResponse({'modelID': carModel.id,
                            'status': 'Car model has been deleted'})
