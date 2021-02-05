from django.conf import settings
from django.urls import reverse
from allauth.account.adapter import DefaultAccountAdapter

class MyAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):

        print('request.user.isStaff', request.user.isStaff)

        if request.user.isCustomer:
            return reverse('customer-profile')
        else:
            return reverse('staff-profile')