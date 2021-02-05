from django.shortcuts import render
from products.models import Product, Category, ProductAttribute
from django.urls import reverse_lazy
# from django.views.generic import DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required

from .models import ProductBrand, PageContent, EmailContent, ProductSection
from products.models import Attribute, Category
from promotions.models import Promotion
from django.core.paginator import Paginator
from .models import PageContent


### PUBLIC PAGES VIEWS ###
def about(request):

    context = {}
    context['categories'] = Category.objects.all()[:50]
    context['pageContent'] = PageContent.objects.get(name='About').content
    return render(request, 'about.html', context)
    
def terms_of_use(request):

    context = {}
    context['categories'] = Category.objects.all()[:50]
    context['pageContent'] = PageContent.objects.get(name='T&C').content
    return render(request, 'terms-of-use.html', context)
    
def privacy_policy(request):

    context = {}
    context['categories'] = Category.objects.all()[:50]
    context['pageContent'] = PageContent.objects.get(name='Privacy').content
    return render(request, 'privacy-policy.html', context)

def home(request):
    
    # PROMOTED PRODUCTS
    promotedProducts = Product.objects.filter(
        promotion__isActive=True
    )

    context = {}

    # Product attributes for product filtering
    context['product_attributes_width'] = ProductAttribute.objects.filter(attribute__name__iexact='tire width').values_list('values', flat=True).distinct()
    context['product_attributes_height'] = ProductAttribute.objects.filter(attribute__name__iexact='tire height').values_list('values', flat=True).distinct()
    context['product_attributes_diameter'] = ProductAttribute.objects.filter(attribute__name__iexact='tire diameter').values_list('values', flat=True).distinct()

    context['productBrands'] = ProductBrand.objects.all().order_by('rank')
    context['pageContents'] = PageContent.objects.all()

    context['featuredProducts'] = Product.objects.filter(isFeatured=True)[:50]
    context['promotedProducts'] = promotedProducts[:50]
    context['categories'] = Category.objects.all()[:50]
    context['promotions'] = Promotion.objects.filter(
        isActive=True,
        isFeatured=True
    )[:50]
    context['productSections'] = ProductSection.objects.filter(isActive=True).order_by('rank')[:50]

    return render(request, 'home.html', context)


### CONTENT MANAGEMENT VIEWS ################

class PageContentEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = PageContent
    permission_required = 'pages.view_pagecontent'
    template_name = 'pagecontent-edit.html'
    success_url = reverse_lazy('dashboard')
    fields = [
        # 'page',
        'content',
    ]


### PRODUCT BRAND VIEWS ###

@login_required
@permission_required('pages.view_pagecontent', raise_exception=True)
def product_brands_list_view(request):

    productBrands = ProductBrand.objects.all().order_by('rank')
    paginator = Paginator(productBrands, 30)
    page_number = request.GET.get('page')
    productBrands = paginator.get_page(page_number)

    context = {}
    context['productBrands'] = productBrands
    return render(request, 'productbrand-list.html', context)

class ProductBrandCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ProductBrand
    permission_required = 'pages.view_pagecontent'
    template_name = 'productbrand-create.html'
    success_url = reverse_lazy('productbrand-list')
    fields = [
        'name',
        'image',
        'rank',
    ]

class ProductBrandEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ProductBrand
    permission_required = 'pages.view_pagecontent'
    template_name = 'productbrand-edit.html'
    success_url = reverse_lazy('productbrand-list')
    fields = [
        'name',
        'image',
        'rank',
    ]

class ProductBrandDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ProductBrand
    permission_required = 'pages.view_pagecontent'
    context_object_name = 'service'
    template_name='productbrand-delete.html'
    success_url = reverse_lazy('productbrand-list')    
    

### PRODUCT SECTION VIEWS ###

class ProductSectionCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ProductSection
    permission_required = 'pages.view_pagecontent'
    context_object_name = 'productSection'
    template_name='productsection-create.html'
    success_url = reverse_lazy('productsection-list')
    fields = "__all__"

class ProductSectionEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ProductSection
    permission_required = 'pages.view_pagecontent'
    context_object_name = 'productSection'
    template_name='productsection-edit.html'
    success_url = reverse_lazy('productsection-list')
    fields = "__all__"

@login_required
@permission_required('pages.view_pagecontent', raise_exception=True)
def product_section_list_view(request):

    product_sections = ProductSection.objects.all().order_by('rank')

    paginator = Paginator(product_sections, 30)
    page_number = request.GET.get('page')
    product_sections = paginator.get_page(page_number)
    context = {}
    context['productSections'] = product_sections

    return render(request, 'productsection-list.html', context)

class ProductSectionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ProductSection
    permission_required = 'pages.view_pagecontent'
    context_object_name = 'productSection'
    template_name='productsection-delete.html'
    success_url = reverse_lazy('productsection-list')
    fields = "__all__"


### EMAIL VIEWS ###

@login_required
@permission_required('pages.view_pagecontent', raise_exception=True)
def email_content_list_view(request):
    emails = EmailContent.objects.all()
    paginator = Paginator(emails, 30)
    page_number = request.GET.get('page')
    emails = paginator.get_page(page_number)

    context = {}
    context['emailContents'] = emails
    return render(request, 'emailcontent-list.html', context)

class EmailContentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = EmailContent
    permission_required = 'pages.view_pagecontent'
    template_name = 'emailcontent-create.html'
    success_url = reverse_lazy('emailcontent-list')
    fields = [
        'name',
        'subject',
        'content',
    ]

class EmailContentEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = EmailContent
    permission_required = 'pages.view_pagecontent'
    template_name = 'emailcontent-edit.html'
    success_url = reverse_lazy('emailcontent-list')
    fields = [
        'subject',
        'content',
    ]

class EmailContentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = EmailContent
    permission_required = 'pages.view_pagecontent'
    context_object_name = 'service'
    template_name='emailcontent-delete.html'
    success_url = reverse_lazy('emailcontent-list')    