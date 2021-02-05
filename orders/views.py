from datetime import datetime, timedelta
DATE_FORMAT = '%Y-%m-%d'

from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView
from django import forms
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy

from orders.models import Order, ProductHistory, OrderItem
from coupons.models import Coupon
from products.models import Product, Attribute, Category
from stores.models import Store
from .forms import (
    QuantityForm, 
    CheckoutPaymentMethodsForm, 
    ShippingAddressSelectForm, 
    StaffOrderCreateForm,
    PaymentStoreSelectForm,
    # ProductCollectionForm,
    OrderEditForm,
)
from customers.forms import CustomerSignUpForm, CustomerFaceAddressCreateForm
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Sum          # to do advanced queries
from django.http import JsonResponse
from customers.models import User, Address
import json
from .utils import (
    get_order_items_cart_total,
    get_order_items,
    send_order_emails,
)

# REST API stuff
from rest_framework.parsers import JSONParser
from .serializers import ProductSerializer, ProductSearchSerializer, UpdateCartSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from indodana.models import Indodana
from coupons.models import Coupon

@login_required
@permission_required('orders.view_order', raise_exception=True)
def order_create_view(request):
    '''View is used only to serve the API for the staff to select the customer'''
    return render(request, 'order-create.html', {})


class OrderListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Order
    context_object_name = 'orders'
    permission_required = 'orders.view_order'
    template_name='order-list.html'
    paginate_by = 30

    # query set function to get the results of the search field 
    def get_queryset(self):

        query = self.request.GET.get('q')
        date_from = self.request.GET.get('from')
        date_until = self.request.GET.get('until')
        sort_by = self.request.GET.get('sort_by')

        ## sorting by
        if sort_by == 'cart_total_asc':
            sort_by = 'cart_total'
        elif sort_by == 'cart_total_desc':
            sort_by = '-cart_total'
        elif sort_by == 'date_asc':
            sort_by = 'dateCreated'
        elif sort_by == 'date_desc':
            sort_by = '-dateCreated'
        elif sort_by == 'status_asc':
            sort_by = 'status'
        elif sort_by == 'status_desc':
            sort_by = '-status'
        else:
            sort_by = '-dateCreated'

        orders = Order.objects.order_by(sort_by).exclude(
            status='Pending'
        ).annotate(
            cart_total = Sum('orderitem__price'),
            cart_total_with_discount = Sum('orderitem__discountedPrice')
        )

        if query: 
            for query_item in query.split(' '):

                orders_by_string = orders.filter(
                    Q(customer__user__first_name__icontains = query_item) | 
                    Q(customer__user__last_name__icontains = query_item) |
                    Q(customer__user__mobileNumber__icontains = query_item) |
                    Q(customer__user__phoneNumber__icontains = query_item)  |
                    Q(customer__user__email__icontains = query_item) |
                    Q(customer__customercar__licensePlate__icontains = query_item) |

                    Q(id__icontains = query_item) |                  # == invoice number
                    Q(store__name__icontains = query_item) |
                    Q(status__icontains = query_item) |
                    Q(orderChannel__icontains = query_item) 
                )

                if query_item.isdigit():
                    orders_cart_size = orders.filter(
                        Q(id = query_item) |
                        Q(cart_total = query_item) |            # if passing in the number check if that matches the total cart price
                        Q(cart_total_with_discount = query_item)
                    ) 
                    orders = orders_cart_size | orders_by_string
                
                else: orders = orders_by_string
                                            
        ## FILTERING BY ORDER DATE CREATED
        if date_from:
            datetime_obj = datetime.strptime(date_from, DATE_FORMAT)
            orders = orders.filter(dateCreated__gte=datetime_obj)
        
        if date_until:
            datetime_obj = datetime.strptime(date_until, DATE_FORMAT) + timedelta(days=1)
            orders = orders.filter(dateCreated__lte=datetime_obj)
 
        return orders.distinct()

class OrderDetailsView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'orders.view_order'

    def get(self, request, pk):

        order = Order.objects.get(pk=pk)

        if request.GET.get('print') == 'true':
            template_name='order-print.html'
        else:
            template_name='order-details.html'

        return render(request, template_name, {'order': order})

class OrderEditView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'orders.view_order'

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)

        if order.status in ['Cancelled', 'Refunded']:
            return redirect('order-details', pk=pk)

        context = {}
        context['form'] = OrderEditForm(instance=order)
        return render(request, 'order-edit.html', context)

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk) 
        orderEditForm = OrderEditForm(request.POST or None, instance = order)

        if not orderEditForm.is_valid():
            context = {}
            context['form'] = orderEditForm
            return redirect('order-details', pk=pk)
        else:
            order.save()

            ## placing items back to stock
            if order.status in ['Cancelled', 'Refunded']:
                for orderItem in order.orderitem_set.all():
                    productHistory = ProductHistory()
                    productHistory.adjust_stock_order(orderItem, order.status, returned=True)

                send_order_emails(order)

            return redirect('order-list')


class OrderItemEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = OrderItem
    permission_required = 'orders.view_order'
    template_name = 'orderitem-edit.html'
    # success_url = reverse_lazy(
    #     'order-edit', 
    #     kwargs={
    #         'pk': self.model.pk
    #     }
    # )
    fields = [
        'quantity',
        'discountedPrice',
    ]


### STAFF CREATING ORDERS FOR CUSTOMERS
@login_required
@permission_required('orders.view_order', raise_exception=True)
def select_customer(request):
    """
    API view to select or create a customer for the staff to craete an order for that customer.
    """

    data = json.loads(request.body)
    name = data['name']
    email = data['email']
    mobileNumber = data['mobileNumber']

    # create query by the search criteria
    users = User.objects.filter(isCustomer=True).values(
        'id', 
        'first_name', 
        'last_name', 
        'email',
        'mobileNumber'
    )
    
    if name != "":
        users = users.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
    
    if email != "":
        users = users.filter(email__icontains=email)

    if mobileNumber != "":
        users = users.filter(mobileNumber__icontains=mobileNumber)

    return JsonResponse({"users": list(users[:50])}) # limiting down to 50 results only

@login_required
@permission_required('orders.view_order', raise_exception=True)
def order_create_cart_view(request, pk):
    """view for staff to create orders for customers"""

    customer_user = User.objects.get(pk=pk)

    order, orderIsCreated = Order.objects.get_or_create(
        customer=customer_user.customer,
        status='Pending'
    )

    orderItems = order.orderitem_set.all()
    coupon = Coupon()
    orderItems, couponMessage = coupon.apply_coupon(orderItems, request, customer_user=customer_user)
    cart_total = get_order_items_cart_total(orderItems)


    if request.method == 'GET':
        shippingAddressSelectForm = ShippingAddressSelectForm()
        checkoutPaymentMethodsForm = CheckoutPaymentMethodsForm()
        staffOrderCreateForm = StaffOrderCreateForm()
        del checkoutPaymentMethodsForm.fields['payment_method'].choices[-1]                     # deleting indodana as option in the list
        checkoutPaymentMethodsForm.fields['installment_period'].widget = forms.HiddenInput()  # disabling installment period, as it can be used only directly by the customer login
        paymentStoreSelectForm = PaymentStoreSelectForm()
        customerFaceAddressCreateForm = CustomerFaceAddressCreateForm()


    if request.method == 'POST':
        passCriteria = False

        # inserting the selected address option into the form, as they are loaded dynamically on the frontend
        shippingAddressSelectForm = ShippingAddressSelectForm(request.POST)
        customerFaceAddressCreateForm = CustomerFaceAddressCreateForm(request.POST)
        checkoutPaymentMethodsForm = CheckoutPaymentMethodsForm(request.POST)
        paymentStoreSelectForm = PaymentStoreSelectForm(request.POST)
        paymentStoreId = None
        product_collection_choice = request.POST.get('product_collection_choice')

        staffOrderCreateForm = StaffOrderCreateForm(request.POST)
        
        ## PRODUCT COLLECTION VIA SHIPPING:
        if product_collection_choice == 'shipping':

            addressSelectedID = request.POST.get('addressSelected')
            shippingAddressSelectForm.fields['addressSelected'].choices = [(addressSelectedID, addressSelectedID)]

            # SECTION OF EXISTING ADDRESS
            if shippingAddressSelectForm.is_valid() and shippingAddressSelectForm.cleaned_data['addressSelected'] != '-1':
                
                shippingAddress = Address.objects.get(
                    pk=shippingAddressSelectForm.cleaned_data['addressSelected']
                )
                passCriteria = True

            # SELECTION TO ENDER A NEW ADDRESS
            elif customerFaceAddressCreateForm.is_valid():
                shippingAddress = customerFaceAddressCreateForm.save(commit=False)
                passCriteria = True
            
        ## PRODUCT COLLECTION IN STORE:
        elif product_collection_choice == 'store-pickup' and paymentStoreSelectForm.is_valid():
            paymentStoreId = paymentStoreSelectForm.cleaned_data.get('paymentStore')
            passCriteria = True


        if passCriteria and \
            checkoutPaymentMethodsForm.is_valid() and \
            staffOrderCreateForm.is_valid():

            # Saving the address or payment store
            if paymentStoreId:
                order.store = Store.objects.get(id=paymentStoreId)
            else:
                shippingAddress.save()
                customer_user.customer.address_set.add(shippingAddress)
                order.shippingAddress = shippingAddress
                
            # setting payment option
            order.paymentOption = checkoutPaymentMethodsForm.cleaned_data.get('payment_method')

            # status setting:
            if order.paymentOption == 'Bank Transfer': order.status = 'Awaiting Bank Transfer'
            elif order.paymentOption == 'Payment in the store': order.status = 'Awaiting payment in store'
            elif order.paymentOption == 'Payment on delivery': order.status = 'Awaiting payment on delivery'
            elif order.paymentOption == 'Indodana': order.status = 'Awaiting Indodana payment'
            else: order.status = 'Unknown'

            order.orderChannel = staffOrderCreateForm.cleaned_data.get('orderChannel')
            order.shippingCost = staffOrderCreateForm.cleaned_data.get('shippingCost')
            order.notes = staffOrderCreateForm.cleaned_data.get('notes')
            order.staff = request.user
            customer_user.save()

            # managing stock
            for orderItem in orderItems:
                orderItem.save()
                productHistory = ProductHistory()
                productHistory.adjust_stock_order(orderItem, 'Purchase via backoffice')

            # processing the coupon
            if coupon.coupon:
                coupon.coupon.amountUsed += 1
                coupon.coupon.customersUsedCoupons.add(customer_user)
                coupon.coupon.save()
                order.coupon = coupon.coupon

            order.save()
                
            return redirect('order-details', pk=order.id)

    context = {}
    context['user'] = customer_user
    context['attributes'] = Attribute.objects.all()
    context['categories'] = Category.objects.all()
    context['ShippingAddressSelectForm'] = shippingAddressSelectForm
    context['CheckoutPaymentMethodsForm'] = checkoutPaymentMethodsForm
    context['PaymentStoreSelectForm'] = paymentStoreSelectForm
    context['StaffOrderCreateForm'] = staffOrderCreateForm
    context['CustomerFaceAddressCreateForm'] = customerFaceAddressCreateForm
    context['orderItems'] = orderItems
    context['couponMessage'] = couponMessage

    return render(request, 'order-create-cart.html', context)


@api_view(('POST',))
def select_products(request):
    """
    API view for the staff to select products for customer's cart in a popup windown
    """
    if request.method == 'POST':
        productSearchSerializer = ProductSearchSerializer(data=request.data)
        if productSearchSerializer.is_valid():

            name = productSearchSerializer.data['name']
            attribute = productSearchSerializer.data['attribute']
            attributeValue = productSearchSerializer.data['attributeValue']
            brand = productSearchSerializer.data['brand']
            category = productSearchSerializer.data['category']

            products = Product.objects.all()

            serializer_context = {
                'request': (request),
            }

            if name != '':
                products = products.filter(name__icontains=name)
            if attribute != '':
                products = products.filter(productattribute__attribute__name=attribute)
                products = products.filter(productattribute__values__icontains=attributeValue)
            if brand != '':
                products = products.filter(productattribute__attribute__name='Brand')
                products = products.filter(productattribute__values__icontains=brand)
            if category != '':
                products = products.filter(categories__name__icontains=category)

            productSerializer = ProductSerializer(products, many=True, context={'request': serializer_context})

            return Response({
                'filters': productSearchSerializer.data,
                'products':productSerializer.data
                }, status=status.HTTP_202_ACCEPTED)

        return Response(productSearchSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


### CUSTOMER FACING VIEWS
def cart(request):
    cartProducts = request.session.get('products')
    
    orderItems = get_order_items(cartProducts)
       
    # if there is a promo code, update the cart with order items
    coupon = Coupon()
    orderItems, couponMessage = coupon.apply_coupon(orderItems, request)
    cart_total = get_order_items_cart_total(orderItems)

    context = {}
    context['orderItems'] = orderItems
    context['cart_total'] = cart_total
    context['couponMessage'] = couponMessage
    # context = {'order': order}
    context['categories'] = Category.objects.all()[:50]

    return render(request, 'cart.html', context)


def checkout(request):
    context = {}

    cartProducts = request.session.get('products')
    orderItems = get_order_items(cartProducts)
    coupon = Coupon()
    orderItems, couponMessage = coupon.apply_coupon(orderItems, request)
    cart_total = get_order_items_cart_total(orderItems)

    context['categories'] = Category.objects.all()[:50]
    context['orderItems'] = orderItems
    context['cart_total'] = cart_total
    context['couponMessage'] = couponMessage

    ### GET REQUEST #############
    if request.method == 'GET':
        ## FORMS
        context['CustomerSignUpForm'] = CustomerSignUpForm()
        # context['ProductCollectionForm'] = ProductCollectionForm()
        context['PaymentStoreSelectForm'] = PaymentStoreSelectForm()
        context['ShippingAddressSelectForm'] = ShippingAddressSelectForm()
        context['CustomerFaceAddressCreateForm'] = CustomerFaceAddressCreateForm()
        context['CheckoutPaymentMethodsForm'] = CheckoutPaymentMethodsForm()
    
    ### POST REQUEST #############
    if request.method == 'POST':
        passCriteria = False

        # productCollectionForm = ProductCollectionForm(request.POST)
        shippingAddressSelectForm = ShippingAddressSelectForm(request.POST)
        customerSignUpForm = CustomerSignUpForm(request.POST)
        customerFaceAddressCreateForm = CustomerFaceAddressCreateForm(request.POST)
        checkoutPaymentMethodsForm = CheckoutPaymentMethodsForm(request.POST)
        paymentStoreSelectForm = PaymentStoreSelectForm(request.POST)
        paymentStoreId = None
        product_collection_choice = request.POST.get('product_collection_choice')

        ## FOR LOGIN USERS
        if request.user.is_authenticated:
            user = request.user

            # inserting the selected address option into the form, as they are loaded dynamically on the frontend
            addressSelectedID = request.POST.get('addressSelected')
            shippingAddressSelectForm.fields['addressSelected'].choices = [(addressSelectedID, addressSelectedID)]


            # PRODUCT COLLECTION VIA SHIPPING:
            if product_collection_choice == 'shipping':

                # user selects an existing address
                if shippingAddressSelectForm.is_valid() and shippingAddressSelectForm.cleaned_data['addressSelected'] != '-1':
                    
                    shippingAddress = Address.objects.get(
                        pk=shippingAddressSelectForm.cleaned_data['addressSelected']
                    )
                    passCriteria = True

                # User selects a new address
                elif customerFaceAddressCreateForm.is_valid():
                    shippingAddress = customerFaceAddressCreateForm.save(commit=False)
                    passCriteria = True
                
            # PRODUCT COLLECTION IN STORE:
            elif product_collection_choice == 'store-pickup' and paymentStoreSelectForm.is_valid():
                paymentStoreId = paymentStoreSelectForm.cleaned_data.get('paymentStore')
                passCriteria = True

        ## IF NOT LOGGEDIN: CHECK IF ADDRESS FORM  OR COLLECTION STORE IS CORRECT
        elif customerSignUpForm.is_valid():
            if product_collection_choice == 'shipping' and customerFaceAddressCreateForm.is_valid():
                shippingAddress = customerFaceAddressCreateForm.save(commit=False)
                passCriteria = True
            elif product_collection_choice == 'store-pickup' and paymentStoreSelectForm.is_valid():
                paymentStoreId = paymentStoreSelectForm.cleaned_data.get('paymentStore')
                passCriteria = True

        ## IF NOT LOGGEDIN: CHECK IF PAYMENT STORE IS SELECTED
        if passCriteria:
            if checkoutPaymentMethodsForm.is_valid():

                # create new user if the user is not authenticated
                if not request.user.is_authenticated: user = customerSignUpForm.save(request)

                ## Reuse Indodana order if exists, else create new
                order, order_created = Order.objects.get_or_create(
                    customer = user.customer,
                    paymentOption = 'Indodana',
                    status = 'Awaiting Indodana payment',
                    defaults = {
                        'customer': user.customer,
                        'orderChannel': 'Website',
                        'coupon': coupon.coupon,
                    }
                )
                # remove all order items from the order in case the customer has manipulated the cart
                if not order_created:
                    order.orderitem_set.clear()

                # Saving the address or payment store
                if paymentStoreId:
                    order.store = Store.objects.get(id=paymentStoreId)
                else:
                    shippingAddress.save()
                    order.shippingAddress = shippingAddress
                    user.customer.address_set.add(shippingAddress)
                    user.save()

                order.paymentOption = checkoutPaymentMethodsForm.cleaned_data.get('payment_method')
                if checkoutPaymentMethodsForm.cleaned_data.get('installment_period'):
                    order.installmentPeriod = checkoutPaymentMethodsForm.cleaned_data.get('installment_period')

                if checkoutPaymentMethodsForm.cleaned_data.get('payment_store'):
                    order.installmentPeriod = checkoutPaymentMethodsForm.cleaned_data.get('payment_store')

                # status setting:
                if order.paymentOption == 'Bank Transfer': order.status = 'Awaiting Bank Transfer'
                elif order.paymentOption == 'Payment in the store': order.status = 'Awaiting payment in store'
                elif order.paymentOption == 'Payment on delivery': order.status = 'Awaiting payment on delivery'
                elif order.paymentOption == 'Indodana': order.status = 'Awaiting Indodana payment'
                else: order.status = 'Unknown'

                order.save()

                for orderItem in orderItems:
                    orderItem.save()
                    order.orderitem_set.add(orderItem)
                

                ### REGULAR ORDER PROCESSING ###
                if not order.paymentOption == 'Indodana':

                    for orderItem in orderItems:
                        productHistory = ProductHistory()
                        productHistory.adjust_stock_order(orderItem, 'Website Purchase')

                    # updating the coupon code stats
                    if coupon.coupon:
                        coupon.coupon.amountUsed += 1
                        coupon.coupon.customersUsedCoupons.add(user)
                        coupon.coupon.save()

                    # delete the products from the cart
                    if request.session.get('products'): del request.session['products']   
                    # todo delete coupon code from session

                    # login the customer if the customer is not logged in already
                    if not request.user.is_authenticated: login(request, user, backend='django.contrib.auth.backends.ModelBackend')

                    send_order_emails(order)
                    return render(request, 'order-completed.html', context)

                ## INDODANA REQUEST SENDING ##
                else:
                    indodana = Indodana(order)
                    indodana.send_transaction_request()
                    #! save transaction code!!
                    print('RESP DATA', indodana.resp_data)   # todo delete this line
                    
                    if indodana.is_valid():
                        return redirect(indodana.redirect_url)
                    else:
                        context['indodata_error_message'] = indodana.error_message


        context['ShippingAddressSelectForm'] = shippingAddressSelectForm
        context['CustomerSignUpForm'] = customerSignUpForm
        context['CustomerFaceAddressCreateForm'] = customerFaceAddressCreateForm
        context['CheckoutPaymentMethodsForm'] = checkoutPaymentMethodsForm
    
    return render(request, 'checkout.html', context)


def transaction_approval_view(request):

    print('REQUEST INDO HEADER', request.headers)
    print('REQUEST INDO BODY', request.text)

    response = {
        'status': 'OK',
        'message': 'Confirmation received' 
    }

    return JsonResponse(response)

def customer_enquiry(request, slug):

        product = Product.objects.get(slug=slug)
        context = {}

        if request.method == 'GET':
            context['message'] = 'Please select how many products you wish to have.'
            quantityForm = QuantityForm()

            if request.user.is_authenticated and request.user.customer:
                customer = request.user.customer

            else:
                context['customerCreateForm'] = CustomerSignUpForm()


        elif request.method == 'POST':
            quantityForm = QuantityForm(request.POST)

            if request.user.is_authenticated and request.user.customer:
                customer = request.user.customer

            else:
                customerCreateForm = CustomerSignUpForm(request.POST)
                context['customerCreateForm'] = customerCreateForm

                if customerCreateForm.is_valid():
                    user = customerCreateForm.save(request)
                    customer = user.customer
                
                else: customer = None

            if customer:
                if quantityForm.is_valid():

                    order, orderIsCreated = Order.objects.get_or_create(
                        orderChannel='Website',
                        customer=customer,
                        status = 'Enquiry',
                    )
                    
                    # creating product item for the order
                    orderItem, orderItemIsCreated = OrderItem.objects.get_or_create(
                        order = order,
                        product = product,
                        quantity=quantityForm.cleaned_data['quantity'],
                        price = product.price,
                        discountedPrice = product.discount_price,
                    )
                    # log in the user
                    if not request.user.is_authenticated: login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    
                    context['message'] = 'Thank you for your enquiry, we will get back to you as soon as possible.'
                    context['enquirySubmittedSuccessfully'] = True

        context['product'] = product
        context['quantityForm'] = quantityForm

        context['categories'] = Category.objects.all()[:50] # passing the categories for the footer
        return render(request, 'customer-enquiry.html', context)


@api_view(('POST',))
def update_cart(request):
    if request.method == 'POST':

        # processing the cart in cookies wheter the customer is loggedin or not
        productID = request.data.get('productId')
        quantity = request.data.get('quantity')

        #* commented out the real stock quantity to avoid survillance
        # product = Product.objects.get(id=productID)
        # if quantity > product.quantity: quantity = product.quantity
        # if quantity > 20: quantity = 20


        # CASE 1: STAFF ADDING PRODUCTS FOR CUSTOMER - HANDLED VIA PENDING ORDER
        if request.user.is_authenticated and request.user.id != request.data.get('userId'):

            user = User.objects.get(id=request.data.get('userId'))
            product = Product.objects.get(id=request.data.get('productId'))

            order, orderCreated = Order.objects.get_or_create(
                customer=user.customer,
                status = 'Pending',
            )
            order.staff = request.user
            order.save()

            orderItem, orderItemCreated = OrderItem.objects.get_or_create(
                order=order,
                product = product,
                defaults = {
                    'price': product.price,
                    'discountedPrice': product.discount_price
                }
            )
            orderItem.price = product.price
            discountedPrice = product.discount_price

            if orderItemCreated: orderItem.quantity = quantity
            else: orderItem.quantity += quantity

            if orderItem.quantity > 50: orderItem.quantity = 50

            orderItem.save()

            if orderItem.quantity <= 0 or quantity == 0: 
                numProducts = 0
                orderItem.delete()
            else:
                numProducts = orderItem.quantity

            numUniqueProducts = order.orderitem_set.all().count()

        ## CASE 2: CUSTOMER ADDING PRODUCTS TO OWN CART - HANDLED VIA SESSION COOKIES
        else:
            # set products attribute in sesssion if customer doesnt have yet
            if not request.session.get('products'): request.session['products'] = {}

            if not request.session.get('products').get(f'{productID}'):
                request.session.get('products')[f'{productID}'] = quantity
                orderItemCreated = True
            else: 
                request.session.get('products')[f'{productID}'] += quantity
                orderItemCreated = False

            numProducts = request.session.get('products')[f'{productID}']

            if quantity == 0 or numProducts <= 0: 
                del request.session['products'][f'{productID}']   # delete the product from the list if quantity is less or eq zero
            request.session.modified = True

            if numProducts > 50: numProducts = 50

            numUniqueProducts = len(request.session.get('products'))

            discountedPrice = None    # is not being used on the CF side, therefore none

        return Response({
            'numUniqueProducts': numUniqueProducts,
            'numProducts': numProducts,
            'productId': productID,
            'quantity': quantity,
            'discountedPrice': discountedPrice,
            'newProduct': orderItemCreated,
            }, status=status.HTTP_202_ACCEPTED)

    return Response(updateCartData.errors, status=status.HTTP_400_BAD_REQUEST)

@login_required
def customer_orders(request):
    """customer facing view of customer's orders history"""
    orders = Order.objects.filter(customer=request.user.customer)
    context = {'orders': orders}
    context['categories'] = Category.objects.all()
    return render(request, 'customer-orders.html', context)
