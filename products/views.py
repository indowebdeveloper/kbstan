from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator

from products.models import (
    Attribute, 
    Category, 
    Product, 
    ProductImage,
    ProductAttribute,
    ProductSearchQuery
)
from cars.models import CarBrand
from orders.models import ProductHistory

from .forms import ProductAdjustStock

from django.db.models import Sum    # used to calculate the cogs 

from .forms import ProductFullForm, ProductAttributeCreateForm

import json
from django.http import JsonResponse

from django.db.models import Q, Min, Max

@login_required
@permission_required('products.view_product', raise_exception=True)
def product_create_view(request):
    if request.method == 'POST':

        product_form = ProductFullForm(request.POST or None, request.FILES or None)
        files = request.FILES.getlist('gallery_images')
        product_attribute_form = ProductAttributeCreateForm(request.POST)

        if product_form.is_valid() and product_attribute_form.is_valid():

            # collect the attributes and values passed from the form 
            attributeIDs = request.POST.getlist('attribute')
            values = request.POST.getlist('values')
            # product_attribute = product_attribute_form.save() #* depricated, replaced with the list of attributes

            product = product_form.save()

            #? got depricated as we will be using featured image as stand alone from the product model
            # add featured image to the gallery
            # ProductImage.objects.create(
            #         image=product.featured_image,
            #         product=product
            #     )

            # adding other gallary images to the gallary
            for image in files:
                ProductImage.objects.create(
                    image=image,
                    product=product
                )

            # SAVING ATTRIBUTES OF THE PRODUCT
            if attributeIDs[0]:
                print('attributeIDs', attributeIDs)
                for num in range(len(attributeIDs)):
                    product_attribute = ProductAttribute()
                    product_attribute.product = product

                    attribute = Attribute.objects.get(id=attributeIDs[num])
                    product_attribute.attribute = attribute
                    product_attribute.values = values[num]
                    product_attribute.save() 
            
            # SAVE PRODUCT CREATED HISTORY ENTRY
            productHistory = ProductHistory(
                product = product,
                adjustmentType = 'Product created',
                quantity = product.quantity,
                newQuantity = product.quantity,
                purchasePrice = product.purchasePrice,
                purchasePriceTotal = product.purchasePrice * product.quantity,    #? this is an old field that has been
                user = request.user
            ).save()

            return redirect('product-details', slug=product.slug)

    else:
        product_form = ProductFullForm()
        product_attribute_form = ProductAttributeCreateForm()

    context = {}
    context['product_form'] = product_form
    context['product_attribute_form'] = product_attribute_form

    return render(request, 'product-create.html', context)


class ProductEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    permission_required = 'products.view_product'
    template_name = 'product-edit.html'
    fields = [
        'name',
        'categories',
        'price',
        'bottomPrice',
        # 'purchasePrice', 
        'description',
        'isFeatured',
        'isVisible',
        'purchaseOnlyViaEnquiry',
        # 'quantity',  
        'stockThreshold',
        # 'latestPurchasingPrice'
        'seoMetaTags',
        'relatedCarBrand',
        'featured_image',
    ]


### ATTRIBUTES VIEWS
class ProductAttributeCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ProductAttribute
    permission_required = 'products.view_product'
    context_object_name = 'productAttribute'
    template_name = 'product-attribute-create.html'
    success_url = reverse_lazy('product-list')
    fields = [
        'attribute',
        'values',
    ]

    def dispatch(self, request, *args, **kwargs):
        """
        dispatching products's id before saving the attribute
        """
        self.product = get_object_or_404(Product, pk=kwargs['product_pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # adding the productattribute tp the address
        form.instance.product = self.product
        return super().form_valid(form)


class ProductAttributeEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ProductAttribute
    permission_required = 'products.view_product'
    context_object_name = 'productAttribute'
    template_name = 'product-attribute-edit.html'
    success_url = reverse_lazy('product-list')
    fields = [
        'attribute',
        'values',
    ]


class ProductAttributeDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ProductAttribute
    permission_required = 'products.view_product'
    context_object_name = 'productAttribute'
    template_name = 'product-attribute-delete.html'
    success_url = reverse_lazy('product-list')


# todo delte the function below once going into prod, as it got replaced by class based view above
# def product_edit_view(request, slug): 
#     product = get_object_or_404(Product, slug = slug) 
#     # todo add a method to edit all the attributes of that product as well:
#     # productAttribute = get_object_or_404(ProductAttribute, id = id) 
#     form = ProductEditForm(request.POST or None, instance = product)
  
#     if form.is_valid(): 
#         form.save() 
#         return redirect('product-details', slug=product.slug)
  
#     context ={} 
#     context["form"] = form 
  
#     return render(request, 'product-edit.html', context) 

@login_required
@permission_required('products.view_product', raise_exception=True)
def product_list_view(request):

    products = query_products(request)

    paginator = Paginator(products, 30)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    context = {}
    context['products'] = products
    context['attributes'] = Attribute.objects.all()
    context['categories'] = Category.objects.all()
    context['carBrands'] = ProductAttribute.objects.filter(attribute__name__iexact='brand').values_list('values', flat=True)
    return render(request, 'product-list.html', context)


class ProductDetailsView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Product
    permission_required = 'products.view_product'
    template_name= 'product-details.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['categories'] = Category.objects.all()
        context['featuredProducts'] = Product.objects.filter(isFeatured=True)[:10]
        return context

class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    permission_required = 'products.view_product'
    context_object_name = 'product'
    template_name='product-delete.html'
    success_url = reverse_lazy('product-list')

@login_required
@permission_required('products.view_product', raise_exception=True)
def adjust_stock(request, slug):

    product = get_object_or_404(Product, slug=slug) 

    if request.method == 'POST':
        form = ProductAdjustStock(request.POST)

        if form.is_valid():
            productHistory = ProductHistory()
            productHistory.product = product
            productHistory.adjustmentType = form.cleaned_data['adjustmentType']
            productHistory.quantity = form.cleaned_data['amount']
            productHistory.purchasePrice = form.cleaned_data['purchasePrice']
            productHistory.user = request.user
            productHistory.comment = form.cleaned_data['comment']

            if productHistory.purchasePrice and productHistory.quantity:
                productHistory.purchasePriceTotal = productHistory.purchasePrice * productHistory.quantity

            productHistory.addSubtract = form.cleaned_data['addSubtract']
            # calculate and set new quantity
            if productHistory.addSubtract == 'Subtract':
                productHistory.quantity = -productHistory.quantity
            #todo implement validation if stock is higher than amount that is to be subtracted
            productHistory.newQuantity = product.quantity + productHistory.quantity
            product.quantity = productHistory.newQuantity

            ### Calculating COGS ###
            if productHistory.adjustmentType == 'Stock Purchasing':
                amountSum = ProductHistory.objects.filter(Q(product=product) & (Q(adjustmentType='Stock Purchasing') | Q(adjustmentType='Product created'))).aggregate(Sum('quantity'))
                purchasePriceSum = ProductHistory.objects.filter(Q(product=product) & (Q(adjustmentType='Stock Purchasing') | Q(adjustmentType='Product created'))).aggregate(Sum('purchasePriceTotal'))

                totalSum = amountSum['quantity__sum'] + productHistory.quantity
                purchasePriceSum = purchasePriceSum['purchasePriceTotal__sum'] + productHistory.purchasePriceTotal
                
                product.cogs = purchasePriceSum / totalSum
                product.purchasePrice = productHistory.purchasePrice    # updating the latest purchasing price 

            # save both product and productHistory
            productHistory.save()
            product.save()

            return redirect('product-details', slug=product.slug)
    
    else:
        form = ProductAdjustStock()

    return render(request, 'product-adjust-stock.html', {'form': form})

@login_required
@permission_required('products.view_product', raise_exception=True)
def attributes(request):
    query = request.GET.get('q')
    if query:
        attributes = Attribute.objects.filter(name__icontains = query)
    else:
        attributes = Attribute.objects.all()

    paginator = Paginator(attributes, 30)
    page_number = request.GET.get('page')
    attributes = paginator.get_page(page_number)

    return render(request, 'attributes.html', {'attributes': attributes}) 

@login_required
@permission_required('products.view_product', raise_exception=True)
def attributesCreate(request):
    newData = json.loads(request.body)
    attributeName = newData['attributeName']
    attribute, isCreated = Attribute.objects.get_or_create(name=attributeName)

    if isCreated:
        return JsonResponse({'attributeName': attribute.name,
                                'attributeID': attribute.id,
                                'status': 'SUCCESS'})
    else:
        return JsonResponse({'status': 'Attribute already exists'})

@login_required
@permission_required('products.view_product', raise_exception=True)
def attributesUpdate(request):
    newData = json.loads(request.body)
    attributeName = newData['attributeName']
    attributeID = newData['attributeID']

    try:
        attribute = Attribute.objects.get(id=attributeID)
        attribute.name = attributeName
        attribute.save()

        return JsonResponse({'attributeName': attribute.name,
                                'attributeID': attribute.id,
                                'status': 'SUCCESS'})

    except Exception as err:
        return JsonResponse(
            {
                'attributeName': attribute.name,
                'attributeID': attribute.id,
                'status': 'ERROR',
                'message': 'Item already exists'
            }
        )


@login_required
@permission_required('products.view_product', raise_exception=True)
def attributesDelete(request):
    newData = json.loads(request.body)
    attributeID = newData['attributeID']
    attribute = Attribute.objects.get(id=attributeID)
    attribute.delete()

    return JsonResponse({'attributeID': attribute.id,
                            'status': 'SUCCESS'})

## CATEGORIES ##
@login_required
@permission_required('products.view_product', raise_exception=True)
def categories(request):
    query = request.GET.get('q')
    if query:
        categories = Category.objects.filter(name__icontains = query)
    else:
        categories = Category.objects.all()

    paginator = Paginator(categories, 30)
    page_number = request.GET.get('page')
    categories = paginator.get_page(page_number)
    
    return render(request, 'categories.html', {'categories': categories})

@login_required
@permission_required('products.view_product', raise_exception=True)
def categoriesCreate(request):
    newData = json.loads(request.body)
    categoryName = newData['categoryName']
    category, isCreated = Category.objects.get_or_create(name=categoryName)

    if isCreated:
        return JsonResponse({'categoryName': category.name,
                                'categoryID': category.id,
                                'status': 'SUCCESS'})
    else:
        return JsonResponse({'status': 'Category already exists'})

@login_required
@permission_required('products.view_product', raise_exception=True)
def categoriesUpdate(request):
    newData = json.loads(request.body)
    categoryName = newData['categoryName']
    categoryID = newData['categoryID']

    try:
        category = Category.objects.get(id=categoryID)
        category.name = categoryName
        category.save()

        return JsonResponse({'categoryName': category.name,
                                'categoryID': category.id,
                                'status': 'SUCCESS'})
    except Exception as err:
        return JsonResponse({'categoryName': category.name,
                                'categoryID': category.id,
                                'status': 'ERROR',
                                'message': 'Iteam already exists'
                                })


@login_required
@permission_required('products.view_product', raise_exception=True)
def categoriesDelete(request):
    newData = json.loads(request.body)
    categoryID = newData['categoryID']
    category = Category.objects.get(id=categoryID)
    category.delete()

    return JsonResponse({'categoryID': category.id,
                            'status': 'SUCCESS'})


### Customers Products views ###
class CustomerProductDetailsView(DetailView):
    model = Product
    template_name='product.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the categories
        context['categories'] = Category.objects.all()[:50]
        return context


def customer_products_list_view(request):

    products = query_products(request)

    paginator = Paginator(products, 24)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    ## get the attributes and categories
    attributes = Attribute.objects.all()
    productAttributes = ProductAttribute.objects.all()
    categories = Category.objects.all()

    context = {}

    # Product attributes for product filtering
    context['product_attributes_width'] = ProductAttribute.objects.filter(attribute__name__iexact='tire width').values_list('values', flat=True).distinct()
    context['product_attributes_height'] = ProductAttribute.objects.filter(attribute__name__iexact='tire height').values_list('values', flat=True).distinct()
    context['product_attributes_diameter'] = ProductAttribute.objects.filter(attribute__name__iexact='tire diameter').values_list('values', flat=True).distinct()

    context['products'] = products
    context['attributes'] = attributes
    context['categories'] = categories
    context['carBrands'] = ProductAttribute.objects.filter(attribute__name__iexact='brand').values_list('values', flat=True)

    # getting the min and max prices of the all the products to display in the front end price range
    priceMin = Product.objects.filter().values_list('name').annotate(Min('price')).order_by('price').first()
    priceMax = Product.objects.filter().values_list('name').annotate(Max('price')).order_by('-price').first()
    if priceMin and priceMax:
        context['priceMin'] = priceMin[1]
        context['priceMax'] = priceMax[1]
    else:
        context['priceMin'] = 0
        context['priceMax'] = 0


    
    return render(request, 'products.html', context)


def query_products(request):

    query =  request.GET.get('q')
    price_min =  request.GET.get('price_min')
    price_max =  request.GET.get('price_max')
    sizes =  request.GET.get('sizes')
    brands =  request.GET.getlist('brands')
    categories =  request.GET.getlist('categories')
    promotionID = request.GET.get('promotion')
    tire_width = request.GET.get('tire_width')
    tire_height = request.GET.get('tire_height')
    tire_diameter = request.GET.get('tire_diameter')
    sort_by = request.GET.get('sort_by')

    # init query
    products = Product.objects.filter(isVisible=True)

    ## sorting by
    if sort_by == 'price_low_high':
        products = products.order_by('price')
    elif sort_by == 'price_high_low':
        products = products.order_by('-price')
    else:
        products = products.order_by('-dateCreated')

    ## parameters
    if query:

        query_items = query.split(' ')

        for query_item in query_items:
            products = products.filter(
                Q(name__icontains = query_item) |
                Q(id__icontains = query_item) |
                Q(productattribute__values__icontains = query_item)
            )

    if brands:
        products = products.filter(productattribute__attribute__name__iexact='brand')
        products = products.filter(productattribute__values__in=brands)

    if sizes:
        products = products.filter(productattribute__attribute__name__iexact='size')
        products = products.filter(productattribute__values__in=sizes)

    if categories:
        products = products.filter(categories__name__in=categories)

    if promotionID:
        if promotionID == 'all':
            promCategories = Category.objects.filter(promotion__gt=0)
            products = products.filter(
                Q(categories__in=promCategories) |
                Q(promotion__gt=0)
            )
    
        else:
            promCategories = Category.objects.filter(promotion__id=promotionID)
            products = products.filter(
                Q(categories__in=promCategories) |
                Q(promotion=promotionID)
            )
    
    if tire_width:
        products = products.filter(
            productattribute__attribute__name__iexact='tire width',
            productattribute__values=tire_width,
        )

    if tire_height:
        products = products.filter(
            productattribute__attribute__name__iexact='tire height',
            productattribute__values=tire_height,
        )
    if tire_diameter:
        products = products.filter(
            productattribute__attribute__name__iexact='tire diameter',
            productattribute__values=tire_diameter,
        )

    products = products.distinct()  # needs to be distinct since onwards the query will be translated to objects

    # post processing the products by prices
    if price_min:
        products = [product for product in products if product.discount_price and product.discount_price > int(price_min)]

    if price_max:
        products = [product for product in products if product.discount_price and product.discount_price < int(price_max)]

    ## SAVING CUSTOMERS SEARCH QUERIES ##
    queryData = {}
    queryData['keywords'] = query
    queryData['price_min'] = price_min
    queryData['price_max'] = price_max
    queryData['sizes'] = sizes
    queryData['brands'] = brands
    queryData['categories'] = categories
    queryData['promotionID'] = promotionID

    # check if any of the filter parameters is being used to save the search query
    filterParameterUsed = False
    for key in queryData.keys():
        if queryData[key]: filterParameterUsed=True
        
    if filterParameterUsed:     
        productSearchQuery = ProductSearchQuery.objects.create(
            queryData=queryData
        )
        if request.user.is_authenticated: 
            productSearchQuery.user=request.user
            productSearchQuery.save()

    return products