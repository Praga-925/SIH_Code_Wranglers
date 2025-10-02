from django.urls import path
from . import views

app_name = 'users_api'

urlpatterns = [
    # Basic authentication endpoints
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    
    # Admin-only user management
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/<int:id>/', views.UserManagementView.as_view(), name='user_management'),
    
    # Permission testing endpoint
    path('test-permissions/', views.test_permissions, name='test_permissions'),
    
    # Additional endpoints (backward compatibility)
    path('register-alt/', views.register, name='register_alt'),
    path('login-alt/', views.login, name='login_alt'),
    path('logout/', views.logout, name='logout'),
    path('profile/update/', views.UserUpdateView.as_view(), name='profile_update'),
    path('change-password/', views.change_password, name='change_password'),
]