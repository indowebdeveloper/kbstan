from django.db import models
from django.urls import reverse
from django.core.serializers.json import DjangoJSONEncoder  # required for datetime serialization to pass in the the requests to indodana

from datetime import datetime, timedelta
from requests import post, get
import hashlib, hmac, time, math, json

class Indodana:

    def __init__(self, order):
        '''Takes in the order and constructs the payload to be sent to Indodana for confirmation'''

        self.order = order
        self.construct_payload()

    def get_transaction_details(self):
        self.transaction_details = {
            "merchantOrderId": self.order.id,
            "amount": self.order.get_cart_total, 
            "items": []
        }

        for order_item in self.order.orderitem_set.all():

            order_item_temp = {
                "id": str(order_item.product.id),
                "name": order_item.product.name,
                "url": reverse('product', args=[order_item.product.slug]),
                "imageUrl": order_item.product.featured_image.url,
                "type": 'Product',      # self.order_item.product.categories
                "quantity": order_item.quantity,
                "parentType": "SELLER", 
                "parentId": "000001"    
            }

            if order_item.discountedPrice: 
                order_item_temp['price'] = order_item.discountedPrice
            else:
                order_item_temp['price'] = order_item.price

            self.transaction_details['items'].append(order_item_temp)
        
        return self.transaction_details

    def get_customer_details(self):
        user = self.order.customer.user
        self.customer_details = {
            "firstName": user.first_name,
            "lastName": user.last_name,
            "email": user.email,
            "phone": user.mobileNumber
        }
        return self.customer_details

    def get_seller(self):
        self.seller = {
            "id": "000001",
            "name": "KIOSBAN",
            "url": "https://www.kiosban.com",
            "sellerIdNumber": "000001",
            "email": "contact@kiosban.com",
            "address": {
                "firstName": "Merchant",
                "lastName": "Seller",
                "address": "Kelapa Gading",
                "city": "Jakarta Utara",
                "postalCode": "11240",
                "phone": "081812345678",
                "countryCode": "ID"
            }
        }
        return self.seller

    def get_shipping_address(self):
        self.shipping_address = {
            "firstName": self.customer_details['firstName'],
            "lastName": self.customer_details['lastName'],
            "address": str(self.order.shippingAddress.street + ' ' + self.order.shippingAddress.houseNumber),
            "city": self.order.shippingAddress.city,
            "postalCode": str(self.order.shippingAddress.zipCode),
            "phone": self.customer_details['phone'],
            "countryCode": "ID"
        }
        return self.shipping_address

    def construct_payload(self):
        '''Main method to construct the payload that will be send to Indodana for purchase confirmation'''
        expiry_date = datetime.today() + timedelta(days=1)
        expiry_date = expiry_date.astimezone().replace(microsecond=0).isoformat()

        self.payload = {
            'transactionDetails': self.get_transaction_details(),
            'customerDetails': self.get_customer_details(),
            'sellers': [self.get_seller()],
            'billingAddress': self.get_shipping_address(),
            'shippingAddress': self.get_shipping_address(),
            "paymentType": str(self.order.installmentPeriod + '_months'),
            "approvedNotificationUrl": 'http://127.0.0.1:8000/orders/checkout/',
            "cancellationRedirectUrl": 'http://127.0.0.1:8000/orders/checkout/',
            "backToStoreUrl": 'http://127.0.0.1:8000/orders/checkout/',
            # "approvedNotificationUrl": reverse('product', args=(self.order_item.product.slug)),
            # "cancellationRedirectUrl": reverse('product', args=(self.order_item.product.slug)),
            # "backToStoreUrl": reverse('product', args=(self.order_item.product.slug)),
            "expirationAt": expiry_date
        }

    def is_valid(self):
        '''Checks if the response from Indodana is valid and returns True or False'''
        self.resp_status = self.resp_data.get('status')
        self.redirect_url = self.resp_data.get('redirectUrl')

        if self.resp_status == 'OK': 
            return True
        else: 
            self.error_message = f'Something went wrong. Error: {self.resp_data.get("error")["message"]}. \nPlease try again or contact our team for support.'
            return False

    def send_transaction_request(self):
        '''Generates the auth key and sends the request to Indodata to do the transaction'''

        def generate_authorization_key():
            api_key = '098f75158d034f3'
            api_secret = '2df2b5f3ee5142c785b82cbddf1eaba7'
            nonce = math.floor(time.time())

            string = api_key + ':' + str(nonce)
            signature = hmac.new(bytes(api_secret , 'latin-1'), msg = bytes(string , 'latin-1'), digestmod = hashlib.sha256).hexdigest()

            return f'Bearer {api_key}:{nonce}:{signature}'


        ### EXECUTION ###

        resp = post(
            'https://sandbox01-api.indodana.com/chermes/merchant/v1/checkout_url', 
            headers = {'Authorization': generate_authorization_key()}, 
            json = self.payload
        )

        self.resp_data = json.loads(resp.text)
        # print('self.payload', self.payload)
        # print('resp_data', resp_data)
        # return resp_data