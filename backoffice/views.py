from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.db.models import F  # used to do comparison queries of the same instance
from products.models import Product, ProductSearchQuery
from django.core.paginator import Paginator

@login_required
@permission_required('backoffice.view_dashboard', raise_exception=True)
def dashboard(request):
    productsLowInStock = Product.objects.filter(quantity__lt=F('stockThreshold'))

    paginator = Paginator(productsLowInStock, 30)
    page_number = request.GET.get('page')
    productsLowInStock = paginator.get_page(page_number)

    context = {}
    context['products_low_stock'] = productsLowInStock
    context['customerQueries'] = ProductSearchQuery.objects.all()[:50]

    return render(request, 'dashboard.html', context)
