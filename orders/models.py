from django.db import models

from customers.models import Customer, Address
from staff.models import Staff
from stores.models import Store
from products.models import Product
from services.models import Service
from customers.models import User
from django.urls import reverse
from coupons.models import Coupon


ORDER_CHANNEL_CHOICES = (
    ('WhatsApp', 'WhatsApp'),
    ('Phone Call', 'Phone Call'),
    ('Email', 'Email'),
    ('Instagram', 'Instagram'),
    ('Facebook', 'Facebook'),
    ('Marketplace', 'Marketplace'),
    ('Chat Box', 'Chat Box'),
    ('Website', 'Website'),
)

PAYMENT_CHOICES = (
    ('Bank Transfer', 'Bank Transfer'),
    ('Payment in the store', 'Payment in the store'),
    # ('Payment on delivery', 'Payment on delivery'),
    ('Indodana', 'Indodana'),
)

INSTALLMENT_CHOICES = [
    ('1', '1 month'),
    ('3', '3 months'),
    ('6', '6 months'),
    ('12', '12 months'),
]

class Order(models.Model):

    status_choices = (
        ('Enquiry', 'Enquiry'),     # enquiry before order
        ('Pending', 'Pending'),     # order pending
        ('Awaiting Bank Transfer', 'Awaiting Bank Transfer'),
        ('Awaiting payment in store', 'Awaiting payment in store'),
        ('Awaiting payment on delivery', 'Awaiting payment on delivery'),
        ('Awaiting Indodana payment', 'Awaiting Indodana payment'),
        ('Reserved', 'Reserved'),
        ('Paid on website', 'Paid on website'),
        ('Paid in store', 'Paid in store'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Refund in process', 'Refund in process'),
        ('Refunded', 'Refunded'),
    )


    dateCreated = models.DateTimeField(auto_now_add=True)
    dateEdited = models.DateTimeField(auto_now=True)   
    
    orderChannel = models.CharField(choices=ORDER_CHANNEL_CHOICES, max_length=20, default='WhatsApp', verbose_name='Order channel')
    store = models.ForeignKey(Store, blank=True, null=True, on_delete=models.SET_NULL)  
    paymentOption = models.CharField(choices=PAYMENT_CHOICES, max_length=30, verbose_name='Payment option', blank=True, null=True)
    installmentPeriod = models.CharField(choices=INSTALLMENT_CHOICES, max_length=30, verbose_name='Indodana installment period', blank=True, null=True)
    shippingCost = models.PositiveIntegerField(blank=True, null=True, verbose_name='Shipping cost')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    staff = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True) 
    status = models.CharField(max_length=30, choices=status_choices)
    coupon = models.ForeignKey(Coupon, blank=True, null=True, on_delete=models.SET_NULL)
    notes = models.TextField(blank=True, null=True)
    shippingAddress = models.ForeignKey(Address, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return str(self.dateCreated)
    
    def get_absolute_url(self):
        return reverse('order-details', kwargs={'pk': self.pk})
 
    @property
    def get_cart_total(self):
        orderItems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderItems])
        return total


class OrderItem(models.Model):
    dateCreated = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0, blank=True, null=True) 
    price = models.PositiveIntegerField()
    discountedPrice = models.PositiveIntegerField(blank=True, null=True)
    profit = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.dateCreated)

    def get_absolute_url(self):
        return reverse('order-details', kwargs={'pk': self.order.pk})

    @property
    def get_total(self):
        if self.discountedPrice: price = self.discountedPrice
        else: price = self.product.price
        total = price * self.quantity
        return total


class ServiceItem(models.Model):
    dateCreated = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, blank=True, null=True)

    timeSlotsChoices = [
        ('morning', 'morning (7am - 10am)'),
        ('afternoon', 'afternoon (1am - 6pm)'),
        ('evening', 'evening (7pm - 9pm)')
    ]

    appointmentDate = models.DateField(verbose_name='Appointment Date')
    appontmentTimeSlot = models.CharField(max_length=10, choices=timeSlotsChoices, verbose_name='Appointment time slot')

    isFinished = models.BooleanField(default=False)

    def __str__(self):
        return str(self.service)


class ProductHistory(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='history')

    adjustmentType = models.CharField(max_length=50)

    quantity = models.IntegerField()
    newQuantity = models.PositiveIntegerField()
    purchasePrice = models.PositiveIntegerField(blank=True, null=True)
    purchasePriceTotal = models.PositiveIntegerField(blank=True, null=True)
    sellingPrice = models.PositiveIntegerField(blank=True, null=True)

    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    comment = models.CharField(max_length=100, blank=True, null=True)


    def __str__(self):
        return self.adjustmentType

    def adjust_stock_order(self, orderItem, adjustmentType, returned=False):
        # order, order.customer, orderitem

        self.product = orderItem.product
        self.adjustmentType = adjustmentType

        self.quantity = orderItem.quantity

        if returned == True: self.product.quantity = self.product.quantity + orderItem.quantity
        else: self.product.quantity = self.product.quantity - orderItem.quantity

        if orderItem.discountedPrice: self.sellingPrice = orderItem.discountedPrice
        else: self.sellingPrice = orderItem.price

        self.newQuantity = self.product.quantity

        self.order = orderItem.order
        self.user = orderItem.order.customer.user

        self.product.save()
        self.save()

