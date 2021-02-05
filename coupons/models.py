from django.db import models
from datetime import datetime, date
from customers.models import User
from products.models import Product
from django.db.models import Q
from django.core.validators import MaxValueValidator, MinValueValidator
# from django.contrib.postgres.fields import CITextField

class Coupon(models.Model):
    timestampCreated = models.DateTimeField(auto_now_add=True)

    code = models.CharField(max_length=100, unique=True)
    # code = models.CITextField(unique=True)      # case insensitive char field     # replace field above with this one in prod to implement case insensitivity of coupons
    description = models.TextField(blank=True, null=True)
    isActive = models.BooleanField(default=True, verbose_name='Coupon is active')

    amountLimit = models.PositiveIntegerField(blank=True, null=True, verbose_name='Coupon amount limit')
    amountUsed = models.PositiveIntegerField(default=0, verbose_name='Number of times the coupon has been used')
    # amountLeft = models.PositiveIntegerField(verbose_name='Coupons left') #? field replaced by the property field below
    # amountPerCustomer = models.PositiveIntegerField(default=1, verbose_name='Number of coupons per customer')
    limitOnePerCustomer = models.BooleanField(default=True, verbose_name='Coupon is limited to 1 time use per customer')

    discountTypes = [
        ("percent", "percent"),
        ("amount", "amount")
    ]

    discountType = models.CharField(max_length=20, choices=discountTypes, default='percent', verbose_name='Discount type')
    discountAmount = models.PositiveIntegerField(
        verbose_name='Discount amount',
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ])

    dateStart = models.DateField(default=datetime.now, verbose_name='Start date')    #* reference: https://simpleisbetterthancomplex.com/tutorial/2019/01/03/how-to-use-date-picker-with-django.html
    dateEnd = models.DateField(blank=True, null=True, verbose_name='End date')

    categories = models.ManyToManyField(to='products.Category', blank=True)
    products = models.ManyToManyField(to='products.Product', blank=True)

    # conditionTypes = [
    #     ('cart size', 'Minimum cart size'),
    #     ('number of products', 'Minimum number of products')
    # ]

    # conditionType = models.CharField(max_length=20, choices=conditionTypes, verbose_name='Condition type', blank=True, null=True)
    conditionAmount = models.PositiveIntegerField(blank=True, null=True, verbose_name='Minimum cart spending')

    customersUsedCoupons = models.ManyToManyField(User, blank=True)


    def __str__(self):
        return self.code

    @property
    def amountLeft(self):
        if self.amountLimit: return self.amountLimit - self.amountUsed
        # else: return -1     # -1 is the code for unlimited    #? will not be used for now


    def apply_coupon(self, orderItems, request, customer_user=None):

        self.coupon = None  # init coupon to avoid attribute missing in views utilization

        def date_in_range(start, end, x):
            if end:
                return start <= x <= end
            else:
                return start <= x

        if not orderItems: return orderItems, ''    # if orderItems is empty, just skip

        # COUPON EXISTS IN DB CHECK
        promoCode = request.GET.get('promocode')            # first check in get request
        if promoCode: promoCode = promoCode.strip()         # strip in cases of spaces in the code
        
        if promoCode == None: promoCode = request.session.get('promocode')  # next check in cookies
        else: request.session['promocode'] = promoCode  # update the cookie promocode
        if not promoCode: return orderItems, ''     # return same as usual as there is no entry

        self.coupon = Coupon.objects.filter(
            code__iexact=promoCode,
            isActive=True
        ).last()

        if not self.coupon:  
            message = f'Coupon "{promoCode}" does not exist, please check if coupon is correct.'
            if promoCode == request.session.get('promocode'): del request.session['promocode']
            self.coupon = None
            return orderItems, message


        # DATE VALIDITY CHECK
        if not date_in_range(self.coupon.dateStart, self.coupon.dateEnd, date.today()):
            message = 'This coupon code is not valid yet or has already expired.'
            return orderItems, message

        # MAX AMOUNT USED CHECK
        if self.coupon.amountLimit and self.coupon.amountUsed >= self.coupon.amountLimit:
            message = 'This coupon has been used the maximum number of times.'
            return orderItems, message

        # USER ALREADY USED CHECK
        if customer_user:
            if self.coupon.limitOnePerCustomer and request.user.is_authenticated and customer_user in self.coupon.customersUsedCoupons.all():
                message = 'This customer has already used this coupon.'
                return orderItems, message
        else:
            if self.coupon.limitOnePerCustomer and request.user.is_authenticated and request.user in self.coupon.customersUsedCoupons.all():
                message = 'You have already used this coupon.'
                return orderItems, message

        # MIN AMOUNT SPENT CHECK
        cartTotal = 0
        for orderIteam in orderItems:
            itemTotal = orderIteam.quantity * orderIteam.product.price
            cartTotal += itemTotal

        if self.coupon.conditionAmount and cartTotal <= self.coupon.conditionAmount:
            message = f'Minimum spendeture for this coupon is Rp {self.coupon.conditionAmount}.'
            return orderItems, message

        coupon_has_products_restriction = self.coupon.categories.exists() | self.coupon.products.exists()

        if coupon_has_products_restriction:
            # get all the product IDs that this coupon affects
            promotedProductsIDs = Product.objects.filter(
                Q(coupon=self.coupon) | 
                Q(categories__in=self.coupon.categories.all()),
            ).values_list('id', flat=True)
        
        orderItemsNew = []
        couponApplied = False
        for orderItem in orderItems:
            if not coupon_has_products_restriction or orderItem.product.id in promotedProductsIDs:
                couponApplied = True

                if self.coupon.discountType == 'percent':   
                    if self.coupon.discountAmount > 100: self.coupon.discountAmount = 100     # threshold not to give discount over 100%
                    
                    orderItem.discountedPrice = round(orderItem.product.price * (1-self.coupon.discountAmount/100))

                elif self.coupon.discountType == 'amount':
                    orderItem.discountedPrice = orderItem.product.price - self.coupon.discountAmount
                    
                    if orderItem.discountedPrice < 0: orderItem.discountedPrice = 0

                # attaching profit to orderItem
                orderItem.profit = (orderItem.discountedPrice - orderItem.product.purchasePrice) * orderItem.quantity

            else:
                orderItem.profit = (orderItem.price - orderItem.product.purchasePrice) * orderItem.quantity

            orderItemsNew.append(orderItem)

        if not couponApplied:
            message = f'Coupon "{promoCode}" is not applicable to any of the products.'
        else:
            message = f'You are using coupon: {promoCode}.'

        return orderItemsNew, message