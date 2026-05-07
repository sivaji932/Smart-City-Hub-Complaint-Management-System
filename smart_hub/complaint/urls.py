from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),


    path('citizen-dashboard/', views.citizen_dashboard, name='citizen_dashboard'),
    path('citizen/delete/<int:complaint_id>/', views.delete_complaint, name='delete_complaint'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/edit/<int:complaint_id>/', views.edit_complaint, name='edit_complaint'),
]
