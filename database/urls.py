from django.urls import path
from  . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('visitor/', views.visitor, name='visitor'),
    path('edit_profile_page/', views.edit_profile_page, name='edit_profile_page'),
    path('signup/', views.signupPage, name='signup'),   
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),  
    
    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='database/password/password_change_done.html'), name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='database/password/password_change.html'), name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='database/password/password_reset_done.html'), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),    
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='database/password/password_reset_complete.html'),
     name='password_reset_complete'),
]
