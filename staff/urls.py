from django.urls import path
from .views import (
    listView, 
    StaffEditView, 
    StaffDeleteView, 
    staff_create_view, 
    staffProfile,
    staff_signup,
    staff_access_edit_view,
    staff_profile_edit_view,
)
from allauth.account.views import LoginView, LogoutView

urlpatterns = [
    path('', listView, name='staff-list'),
    path('create/', staff_create_view, name='staff-create'),
    path('<int:pk>/edit/', StaffEditView.as_view(), name='staff-edit'),
    path('<int:pk>/access/edit/', staff_access_edit_view, name='staff-access-edit'),
    path('<int:pk>/delete/', StaffDeleteView.as_view(), name='staff-delete'),

    # staff facing views
    path('signup/', staff_signup, name='staff-signup'),
    path('login/', LoginView.as_view(), name='staff-login'),
    path('logout/', LogoutView.as_view(), name='staff-logout'),
    path('profile/', staffProfile, name='staff-profile'),
    path('profile/edit/', staff_profile_edit_view, name='staff-profile-edit'),
]