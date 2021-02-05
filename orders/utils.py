from django.core.mail import EmailMultiAlternatives
from config.settings import MANAGERS
# from .templates import invoice
from django.template.loader import render_to_string

from products.models import Product
from orders.models import OrderItem
from stores.models import Store
from pages.models import EmailContent


def get_order_items(cartProducts):
    orderItems = []
    if cartProducts:
        for productID, quantity in cartProducts.items():
            
            product = Product.objects.filter(id=productID).first()
            
            if product:
                if product.discount_price != product.price: discountedPrice = product.discount_price
                else: discountedPrice = None

                orderItem = OrderItem(
                    product = product,
                    quantity=quantity,
                    price = product.price,
                    discountedPrice = discountedPrice
                )
                orderItems.append(orderItem)

    return orderItems


def get_order_items_cart_total(order_items):
    cart_total = 0
    for item in order_items:
        
        if item.discountedPrice: price = item.discountedPrice
        else: price = item.price

        cart_total += (item.quantity * price)
    return cart_total


def get_stores_choices():
    stores = Store.objects.all()
    payment_stores_choices = []
    for store in stores:
        payment_stores_choices.append(
            (store.id, store.name)      # appending the stores as choices for store payemnt dropdown
        )
        
    return payment_stores_choices


BANK_CHOICES = [
    ('BCA', 'BCA'),
    ('Mandiri', 'Mandiri'),
]

def send_order_emails(order):

    try:
        emailContent = EmailContent.objects.get(name=order.status)  

        message = render_to_string(
            'email/invoice.txt', 
            {
                'order': order,
                'emailContent': emailContent.content
            }
        )

        html_message = render_to_string(
            'email/invoice.html', 
            {
                'order': order,
                'emailContent': emailContent.content
            }
        )

        email = EmailMultiAlternatives(
            emailContent.subject,
            message,
            None,
            [order.customer.user.email],
            # ['stan.kosyakov@gmail.com']     # BCC
        )
        email.attach_alternative(html_message, "text/html")
        email.send()
    
    except Exception as err:

        email = EmailMultiAlternatives(
            "Email error",
            f'An error happened when trying to send out the email. Please check if Email Content section \
                contains all email templates, as this is likely to cause this error.\nError message: "{err}"',
            None,
            MANAGERS
        ).send()
