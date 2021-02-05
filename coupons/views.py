from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q

from datetime import datetime
from .forms import *

from .models import Coupon

@login_required
@permission_required('coupons.view_coupon', raise_exception=True)
def coupon_create_view(request):
    if request.method == 'POST':

        coupon_form = CouponCreateForm(request.POST)

        if coupon_form.is_valid():

            coupon = coupon_form.save()

            return redirect('coupon-list')

    else:
        coupon_form = CouponCreateForm()

    context = {}
    context['coupon_form'] = coupon_form

    return render(request, 'coupon-create.html', context)


@login_required
@permission_required('coupons.view_coupon', raise_exception=True)
def coupon_edit_view(request, pk): 
    coupon = get_object_or_404(Coupon, id = pk) 
    form = CouponEditForm(request.POST or None, instance = coupon)
  
    if form.is_valid(): 
        form.save() 
        return redirect('coupon-list')
  
    context ={} 
    context["form"] = form 
  
    return render(request, 'coupon-edit.html', context) 

@login_required
@permission_required('coupons.view_coupon', raise_exception=True)
def coupon_list_view(request):

    # todo: adjust the filtering parameters accordingly to the model
    # query =  request.GET.get('q')
    # price_min =  request.GET.get('price_min')
    # price_max =  request.GET.get('price_max')
    # sizes =  request.GET.get('sizes')
    # brands =  request.GET.getlist('brands')
    # categories =  request.GET.getlist('categories')

    # products = Product.objects.filter()

    # if query:
    #     products = products.filter(name__icontains = query)

    # if price_min:
    #     products = products.filter(price__gte=price_min)

    # if price_max:
    #     products = products.filter(price__lte=price_max)

    # if brands:
    #     products = products.filter(productattribute__attribute__name__iexact='brand')
    #     products = products.filter(productattribute__values__in=brands)

    # if sizes:
    #     products = products.filter(productattribute__attribute__name__iexact='size')
    #     products = products.filter(productattribute__values__in=sizes)

    # if categories:
    #     products = products.filter(categories__name__in=categories).distinct()


    # ## get the attributes and categories
    # attributes = Attribute.objects.all()
    # productAttributes = ProductAttribute.objects.all()
    # categories = Category.objects.all()
    # carBrands = CarBrand.objects.all()

    # context['products'] = products
    # context['attributes'] = attributes
    # context['categories'] = categories
    # context['carBrands'] = carBrands
    
    include_query = request.GET.get('include')
    if include_query == 'expired':
        coupons = Coupon.objects.all()
    else:
        coupons = Coupon.objects.filter(
            Q(dateEnd__gte=datetime.today()) |
            Q(dateEnd=None)
        )

    paginator = Paginator(coupons, 30)
    page_number = request.GET.get('page')
    coupons = paginator.get_page(page_number)
    context = {}
    context['coupons'] = coupons

    return render(request, 'coupon-list.html', context)

#? detail view is depricated
# class CouponDetailsView(DetailView):
#     model = Product
#     template_name= 'product-details.html'


class CouponDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Coupon
    context_object_name = 'coupon'
    template_name='coupon-delete.html'
    permission_required = 'coupons.view_coupon'
    success_url = reverse_lazy('coupon-list')
