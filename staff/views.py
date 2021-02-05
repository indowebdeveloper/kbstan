from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db.models import Q

from customers.models import User
from .models import Staff
from .forms import StaffCreateForm, UserCreateForm, StaffPermissionsForm, StaffSignUpForm, StaffFaceEditForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import login

# Models import for permissions allocation
from backoffice.models import Dashboard
from cars.models import CarBrand
from coupons.models import Coupon
from customers.models import Customer
from orders.models import Order
from products.models import Product
from promotions.models import Promotion
from stores.models import Store
from pages.models import PageContent


@login_required
@permission_required('staff.view_staff', raise_exception=True)
def staff_create_view(request):
    if request.method == 'POST':

        user_form = UserCreateForm(request.POST)
        staff_form = StaffCreateForm(request.POST)

        if user_form.is_valid() and staff_form.is_valid():
            staff = staff_form.save(commit=False)
            user = user_form.save(commit=False)
            user.isStaff = True     
            staff.user = user
            user.save()
            staff.save()
            return redirect('staff-list')

    else:
        user_form = UserCreateForm()
        staff_form = StaffCreateForm()

    context = {}
    context['user_form'] = user_form
    context['staff_form'] = staff_form

    return render(request, 'staff-create.html', context)

@login_required
@permission_required('staff.view_staff', raise_exception=True)
def listView(request):
    staffList = User.objects.filter(isStaff=True)

    query = request.GET.get('q')
    if query: 
        for query_item in query.split(' '):

            staffList = staffList.filter(
                Q(first_name__icontains=query_item) | 
                Q(last_name__icontains=query_item) |
                Q(email__icontains=query_item) |
                Q(mobileNumber__icontains=query_item)
            ).order_by('-id').distinct()

    paginator = Paginator(staffList, 30)
    page_number = request.GET.get('page')
    staffList = paginator.get_page(page_number)
    return render(request, 'staff-list.html', {'staffList': staffList} )


class StaffEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = User
    permission_required = 'staff.view_staff'
    template_name = 'staff-edit.html'
    fields = ('first_name', 
                'last_name', 
                'email', 
                'mobileNumber'
            )
    success_url = reverse_lazy('staff-list')


@login_required
@permission_required('staff.view_staff', raise_exception=True)
def staff_access_edit_view(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == "GET":
        userPermissions = {
            'dashboard': user.has_perm('backoffice.view_dashboard'),
            'pagecontent': user.has_perm('pages.view_pagecontent'),
            'product': user.has_perm('products.view_product'),
            'carbrand': user.has_perm('cars.view_carbrand'),
            'coupon': user.has_perm('coupons.view_coupon'),
            'customer': user.has_perm('customers.view_customer'),
            'order': user.has_perm('orders.view_order'),
            'promotion': user.has_perm('promotions.view_promotion'),
            'staff': user.has_perm('staff.view_staff'),
            'store': user.has_perm('stores.view_store'),
        }
        staffPermissionsForm = StaffPermissionsForm(userPermissions)

    if request.method == "POST":
        staffPermissionsForm = StaffPermissionsForm(request.POST)
        if staffPermissionsForm.is_valid():

            user.user_permissions.clear()   # clear all the permissions and set new from form

            appModelsList = [
                Dashboard,
                PageContent,
                CarBrand,
                Coupon,
                Customer,
                Order,
                Product,
                Promotion,
                Staff,
                Store,
            ]

            # for each tracked model, check if the model has been passed as true in the form
            # then find that permission in the list and add this permission to users permissions
            for appModel in appModelsList:
                if staffPermissionsForm.cleaned_data.get(appModel._meta.model_name):
                    permission = Permission.objects.get(
                        codename__startswith = 'view_',
                        content_type = ContentType.objects.get_for_model(appModel)
                    )
                    user.user_permissions.add(permission)

            return redirect('staff-list') 

    return render(request, 'staff-access-edit.html', {'staffPermissionsForm': staffPermissionsForm, 'staffUser': user})


class StaffDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = User
    permission_required = 'staff.view_staff'
    context_object_name = 'staff'
    template_name='staff-delete.html'
    success_url = reverse_lazy('staff-list')

@login_required
def staffProfile(request):
    return render(request, 'staff-profile.html')

@login_required
def staff_profile_edit_view(request):

    if request.method == 'POST':
        contact_form = StaffFaceEditForm(request.POST, instance=request.user)

        if contact_form.is_valid:
            contact_form.save()
            return redirect('staff-profile')

    context = {}
    context['form'] = StaffFaceEditForm(instance=request.user)
    return render(request, 'staff-profile-edit.html', context)


def staff_signup(request):
    context = {}

    if request.method == 'GET':
        staffSignupForm = StaffSignUpForm()

    if request.method == 'POST':
        staffSignupForm = StaffSignUpForm(request.POST)

        if staffSignupForm.is_valid():
            staffUser = staffSignupForm.save(request)
            login(request, staffUser, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('staff-profile')

    context['staffSignupForm'] = staffSignupForm
    return render(request, 'staff-signup.html', context)
