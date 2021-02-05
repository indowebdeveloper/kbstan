from datetime import datetime

from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.db.models import Q

from .forms import *

from .models import Promotion
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

@login_required
@permission_required('promotions.view_promotion', raise_exception=True)
def promotion_create_view(request):
    if request.method == 'POST':

        promotion_form = PromotionCreateForm(request.POST, request.FILES)

        if promotion_form.is_valid():

            promotion = promotion_form.save()

            return redirect('promotion-list')

    else:
        promotion_form = PromotionCreateForm()

    context = {}
    context['promotion_form'] = promotion_form

    return render(request, 'promotion-create.html', context)

@login_required
@permission_required('promotions.view_promotion', raise_exception=True)
def promotion_edit_view(request, pk): 

    promotion = get_object_or_404(Promotion, id = pk) 
    form = PromotionEditForm(request.POST or None, request.FILES or None, instance = promotion)
  
    if form.is_valid(): 
        form.save() 
        return redirect('promotion-list')
  
    context ={} 
    context["form"] = form 
  
    return render(request, 'promotion-edit.html', context) 

@login_required
@permission_required('promotions.view_promotion', raise_exception=True)
def promotion_list_view(request):

    include_query = request.GET.get('include')
    if include_query == 'expired':
        promotions = Promotion.objects.all()
    else:
        promotions = Promotion.objects.filter(
            Q(dateEnd__gt=datetime.today()) |
            Q(dateEnd=None)
        )

    paginator = Paginator(promotions, 30)
    page_number = request.GET.get('page')
    promotions = paginator.get_page(page_number)
    context = {}
    context['promotions'] = promotions

    return render(request, 'promotion-list.html', context)


class PromotionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Promotion
    permission_required = 'promotions.view_promotion'
    context_object_name = 'promotion'
    template_name='promotion-delete.html'
    success_url = reverse_lazy('promotion-list')
