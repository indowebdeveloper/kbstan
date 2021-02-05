from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q          # to do advanced queries
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from orders.models import Order
from .models import Customer, User, Address
from .forms import CustomerSignUpForm, CustomerCreateForm, CustomerAddressCreateForm, CustomerCarCreateForm, CustomerFaceContactEditForm, CustomerFaceAddressCreateForm
from products.models import Category
from cars.models import CustomerCar


class FooterCategoriesMixin:

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['categories'] = Category.objects.all()
        return context


@login_required
@permission_required('customers.view_customer', raise_exception=True)
def customer_create_view(request):
    if request.method == 'POST':

        customer_form = CustomerCreateForm(request.POST)
        address_form = CustomerAddressCreateForm(request.POST)
        car_form = CustomerCarCreateForm(request.POST)

        if customer_form.is_valid() and address_form.is_valid() and car_form.is_valid():
            address = address_form.save(commit=False)
            car = car_form.save(commit=False)
            user = customer_form.save(commit=False)
            user.isCustomer = True
            user.save()
            
            customer = Customer(user=user)
            
            customer.save()
            address.customer = customer
            address.save()
            car.customer = customer
            car.save()

            next_arg = request.GET.get('redirect')
            if next_arg:

                return redirect('order-create-cart', pk=user.pk)

            return redirect('customer-details', pk=user.pk)

    else:
        customer_form = CustomerCreateForm()
        address_form = CustomerAddressCreateForm()
        car_form = CustomerCarCreateForm()

    context = {}
    context['customer_form'] = customer_form
    context['address_form'] = address_form
    context['car_form'] = car_form

    return render(request, 'customer-create.html', context)


class CustomerEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = User
    permission_required = 'customers.view_customer'
    template_name = 'customer-edit.html'
    success_url = reverse_lazy('customer-list')
    fields = [
            'first_name',
            'last_name',
            'email',
            # 'phoneNumber',
            'mobileNumber',
            ]


class CustomerAddressCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Address
    permission_required = 'customers.view_customer'
    template_name = 'customer-address-create.html'
    success_url = reverse_lazy('customer-list')
    fields = [
        'type',
        'state',
        'zipCode',
        'city',
        'street',
        'houseNumber',
        'shippingCost',    
    ]

    def dispatch(self, request, *args, **kwargs):
        """
        dispatching customer's id before saving the address
        """
        self.customer = get_object_or_404(Customer, pk=kwargs['customer_pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # adding the customer tp the address
        form.instance.customer = self.customer
        return super().form_valid(form)


class CustomerAddressEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Address
    permission_required = 'customers.view_customer'
    template_name = 'customer-address-edit.html'
    success_url = reverse_lazy('customer-list')
    fields = [
        'type',
        'state',
        'zipCode',
        'city',
        'street',
        'houseNumber',
        'shippingCost',
    ]


class CustomerAddressDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Address
    permission_required = 'customers.view_customer'
    context_object_name = 'customerAddress'
    template_name = 'customer-address-delete.html'
    success_url = reverse_lazy('customer-list')


### CUSTOMER CAR SECTION ###

class CustomerCarCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = CustomerCar
    permission_required = 'customers.view_customer'
    template_name = 'customer-car-create.html'
    success_url = reverse_lazy('customer-list')
    fields = [
        'carBrand',
        'carModel',
        'licensePlate',  
    ]

    def dispatch(self, request, *args, **kwargs):
        """
        dispatching customer's id before saving the address
        """
        self.customer = get_object_or_404(Customer, pk=kwargs['customer_pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # adding the customer tp the address
        form.instance.customer = self.customer

        return super().form_valid(form)


class CustomerCarEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = CustomerCar
    permission_required = 'customers.view_customer'
    template_name = 'customer-car-edit.html'
    success_url = reverse_lazy('customer-list')
    fields = [
        'carBrand',
        'carModel',
        'licensePlate',
    ]


class CustomerCarDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = CustomerCar
    permission_required = 'customers.view_customer'
    context_object_name = 'customerCar'
    template_name = 'customer-car-delete.html'
    success_url = reverse_lazy('customer-list')


@login_required
@permission_required('customers.view_customer', raise_exception=True)
def customer_details_view(request, pk):
    customer = get_object_or_404(User, pk=pk)
    orders = Order.objects.filter(customer__user__pk=pk)
    return render(request, 'customer-details.html', {'customer': customer, 'orders': orders})


class CustomerListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    permission_required = 'customers.view_customer'
    context_object_name = 'customers'
    template_name='customer-list.html'
    paginate_by = 30 #pagination

    # query set function to get the results of the search field 
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            for query_item in query.split(' '):

                return self.model.objects.filter(
                    Q(first_name__icontains = query_item) | 
                    Q(last_name__icontains = query_item) |
                    Q(mobileNumber__icontains = query_item) |
                    Q(phoneNumber__icontains = query_item)  |
                    Q(email__icontains = query_item) |
                    Q(customer__customercar__licensePlate__icontains = query_item),
                    isCustomer=True
                ).distinct()

        else:
            return self.model.objects.all().order_by('-date_joined')


### Customer facing views ###

class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm 
    template_name = 'customer-signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'customer'
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        user = form.save()
        # login(self.request, user)
        return redirect('customer-profile') 

@login_required
def customerProfile(request):
    user = request.user
    context = {'user':user}
    context['categories'] = Category.objects.all()
    return render(request, 'customer-profile.html', context)

@login_required
def customer_facing_profile_edit_view(request):

    if request.method == 'POST':
        contact_form = CustomerFaceContactEditForm(request.POST, instance=request.user)

        if contact_form.is_valid:
            contact_form.save()
            return redirect('customer-profile')

    context = {}
    context['contact_form'] = CustomerFaceContactEditForm(instance=request.user)
    context['categories'] = Category.objects.all()
    return render(request, 'customer-profile-edit.html', context)


class CustomerFacingAddressCreateView(FooterCategoriesMixin, LoginRequiredMixin, CreateView):
    model = Address
    template_name = 'customer-facing-address-create.html'
    success_url = reverse_lazy('customer-profile')
    fields = [
        'type',
        'state',
        'zipCode',
        'city',
        'street',
        'houseNumber',
        # 'shippingCost',    
    ]

    def dispatch(self, request, *args, **kwargs):
        """
        dispatching customer's id before saving the address
        """
        self.customer = get_object_or_404(Customer, pk=kwargs['customer_pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # adding the customer tp the address
        form.instance.customer = self.customer
        return super().form_valid(form)


class CustomerFacingAddressEditView(FooterCategoriesMixin, LoginRequiredMixin, UpdateView):
    model = Address
    template_name = 'customer-facing-address-edit.html'
    success_url = reverse_lazy('customer-profile')
    fields = [
        'type',
        'state',
        'zipCode',
        'city',
        'street',
        'houseNumber',
        # 'shippingCost',
    ]


class CustomerFacingAddressDeleteView(FooterCategoriesMixin, LoginRequiredMixin, DeleteView):
    model = Address
    context_object_name = 'customerAddress'
    template_name = 'customer-facing-address-delete.html'
    success_url = reverse_lazy('customer-profile')


class CustomerFacingCarCreateView(FooterCategoriesMixin, LoginRequiredMixin, CreateView):
    model = CustomerCar
    # permission_required = 'customers.view_customer'
    template_name = 'customer-facing-car-create.html'
    success_url = reverse_lazy('customer-profile')
    fields = [
        'carBrand',
        'carModel',
        'licensePlate',  
    ]

    def dispatch(self, request, *args, **kwargs):
        """
        dispatching customer's id before saving the address
        """
        self.customer = get_object_or_404(Customer, pk=kwargs['customer_pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # adding the customer tp the address
        form.instance.customer = self.customer

        return super().form_valid(form)


class CustomerFacingCarEditView(FooterCategoriesMixin, LoginRequiredMixin, UpdateView):
    model = CustomerCar
    # permission_required = 'customers.view_customer'
    template_name = 'customer-facing-car-edit.html'
    success_url = reverse_lazy('customer-profile')
    fields = [
        'carBrand',
        'carModel',
        'licensePlate',
    ]


class CustomerFacingCarDeleteView(FooterCategoriesMixin, LoginRequiredMixin, DeleteView):
    model = CustomerCar
    # permission_required = 'customers.view_customer'
    context_object_name = 'customerCar'
    template_name = 'customer-facing-car-delete.html'
    success_url = reverse_lazy('customer-profile')