from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator

from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Store
from products.models import Category

def stores(request):
    stores = Store.objects.all()
    context = {'stores':stores}
    context['categories'] = Category.objects.all()
    return render(request, 'stores.html', context)

@login_required
@permission_required('stores.view_store', raise_exception=True)
def stores_list(request):
    stores = Store.objects.all()
        
    paginator = Paginator(stores, 30)
    page_number = request.GET.get('page')
    stores = paginator.get_page(page_number)

    context = {'stores':stores}
    return render(request, 'stores-list.html', context)


class StoreCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Store
    permission_required = 'stores.view_store'
    fields = '__all__'
    success_url = reverse_lazy('stores-list')


class StoreUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Store
    permission_required = 'stores.view_store'
    fields = '__all__'
    success_url = reverse_lazy('stores-list')


class StoreDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Store
    permission_required = 'stores.view_store'
    fields = '__all__'
    success_url = reverse_lazy('stores-list')