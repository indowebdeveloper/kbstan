from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator

from .models import Service
from products.models import Attribute, Category


@login_required
@permission_required('services.view_service', raise_exception=True)
def service_list_view(request):

    services = Service.objects.all()

    paginator = Paginator(services, 30)
    page_number = request.GET.get('page')
    services = paginator.get_page(page_number)

    context = {}
    context['services'] = services
    context['attributes'] = Attribute.objects.all()
    context['categories'] = Category.objects.all()
    return render(request, 'service-list.html', context)


class ServiceCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Service
    permission_required = 'services.view_service'
    template_name = 'service-create.html'
    success_url = reverse_lazy('service-list')
    fields = [
        'name',
        'description',
        'price',
        'seoMetaTags',
        'isVisible',
        'relatedCategories',
        'relatedProducts',
    ]


class ServiceEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Service
    permission_required = 'services.view_service'
    template_name = 'service-edit.html'
    fields = [
        'name',
        'description',
        'price',

        'seoMetaTags',
        'isVisible',
        'relatedCategories',
        'relatedProducts',
    ]

class ServiceDetailsView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Service
    permission_required = 'services.view_service'
    template_name= 'service-details.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['categories'] = Category.objects.all()
        return context

class ServiceDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Service
    permission_required = 'services.view_service'
    context_object_name = 'service'
    template_name='service-delete.html'
    success_url = reverse_lazy('service-list')