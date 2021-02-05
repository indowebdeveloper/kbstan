from django.contrib import admin
from .models import ProductBrand, PageContent, EmailContent

admin.site.register(EmailContent)
admin.site.register(ProductBrand)
admin.site.register(PageContent)
