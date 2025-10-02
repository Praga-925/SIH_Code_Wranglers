"""
Role-based decorators and mixins for LCA Tool
"""
from functools import wraps
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.response import Response
from rest_framework import mixins, viewsets


def role_required(*roles):
    """
    Decorator to require specific roles for function-based views.
    Usage: @role_required('admin', 'metallurgist')
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return JsonResponse({'error': 'Authentication required'}, status=401)
            
            if request.user.role not in roles:
                return JsonResponse({
                    'error': 'Insufficient permissions',
                    'required_roles': roles,
                    'user_role': request.user.role
                }, status=403)
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def minimum_role_required(minimum_role):
    """
    Decorator to require minimum role level.
    Usage: @minimum_role_required('metallurgist')
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return JsonResponse({'error': 'Authentication required'}, status=401)
            
            from .permissions import ROLE_HIERARCHY
            user_level = ROLE_HIERARCHY.get(request.user.role, 0)
            required_level = ROLE_HIERARCHY.get(minimum_role, 0)
            
            if user_level < required_level:
                return JsonResponse({
                    'error': 'Insufficient role level',
                    'minimum_role': minimum_role,
                    'user_role': request.user.role
                }, status=403)
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def admin_required(view_func):
    """
    Decorator to require admin role.
    Usage: @admin_required
    """
    return role_required('admin')(view_func)


def metallurgist_or_admin_required(view_func):
    """
    Decorator to require metallurgist or admin role.
    Usage: @metallurgist_or_admin_required
    """
    return role_required('metallurgist', 'admin')(view_func)


class RoleBasedViewMixin:
    """
    Mixin to add role-based access control to class-based views.
    """
    required_roles = None
    minimum_role = None
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, 
                          status=status.HTTP_401_UNAUTHORIZED)
        
        # Check required roles
        if self.required_roles and request.user.role not in self.required_roles:
            return Response({
                'error': 'Insufficient permissions',
                'required_roles': self.required_roles,
                'user_role': request.user.role
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Check minimum role
        if self.minimum_role:
            from .permissions import ROLE_HIERARCHY
            user_level = ROLE_HIERARCHY.get(request.user.role, 0)
            required_level = ROLE_HIERARCHY.get(self.minimum_role, 0)
            
            if user_level < required_level:
                return Response({
                    'error': 'Insufficient role level',
                    'minimum_role': self.minimum_role,
                    'user_role': request.user.role
                }, status=status.HTTP_403_FORBIDDEN)
        
        return super().dispatch(request, *args, **kwargs)


class AdminOnlyMixin(RoleBasedViewMixin):
    """
    Mixin to restrict access to admin users only.
    """
    required_roles = ['admin']


class MetallurgistOrAdminMixin(RoleBasedViewMixin):
    """
    Mixin to restrict access to metallurgist and admin users.
    """
    required_roles = ['metallurgist', 'admin']


class AuthenticatedUserMixin(RoleBasedViewMixin):
    """
    Mixin to allow all authenticated users.
    """
    required_roles = ['engineer', 'metallurgist', 'admin']


class RoleBasedModelViewSet(viewsets.ModelViewSet):
    """
    Custom ModelViewSet with role-based permissions for different actions.
    """
    role_permissions = {
        'list': ['engineer', 'metallurgist', 'admin'],
        'retrieve': ['engineer', 'metallurgist', 'admin'],
        'create': ['metallurgist', 'admin'],
        'update': ['metallurgist', 'admin'],
        'partial_update': ['metallurgist', 'admin'],
        'destroy': ['admin'],
    }
    
    def check_permissions(self, request):
        """
        Check if the user has permission for the current action.
        """
        super().check_permissions(request)
        
        if not request.user.is_authenticated:
            self.permission_denied(request, message='Authentication required')
        
        action = self.action or 'list'
        required_roles = self.role_permissions.get(action, ['admin'])
        
        if request.user.role not in required_roles:
            self.permission_denied(
                request, 
                message=f'Role {request.user.role} not allowed for action {action}'
            )


def log_permission_check(func):
    """
    Decorator to log permission checks for auditing.
    """
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        import logging
        logger = logging.getLogger('permissions')
        
        user = getattr(request, 'user', None)
        user_info = f"{user.username} ({user.role})" if user and user.is_authenticated else "Anonymous"
        
        logger.info(f"Permission check: {func.__name__} - User: {user_info} - Path: {request.path}")
        
        result = func(request, *args, **kwargs)
        
        if hasattr(result, 'status_code') and result.status_code == 403:
            logger.warning(f"Permission denied: {func.__name__} - User: {user_info}")
        
        return result
    return wrapper


class OwnershipMixin:
    """
    Mixin to enforce object ownership permissions.
    Users can only access their own objects, admin can access all.
    """
    ownership_field = 'created_by'  # Field that stores the owner
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        if not self.request.user.is_authenticated:
            return queryset.none()
        
        # Admin can see all objects
        if self.request.user.role == 'admin':
            return queryset
        
        # Users can only see their own objects
        filter_kwargs = {self.ownership_field: self.request.user}
        return queryset.filter(**filter_kwargs)
    
    def perform_create(self, serializer):
        """
        Set the owner when creating new objects.
        """
        serializer.save(**{self.ownership_field: self.request.user})


def api_role_required(*roles):
    """
    Decorator for DRF API views to require specific roles.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, request, *args, **kwargs):
            if not request.user.is_authenticated:
                return Response({'error': 'Authentication required'}, 
                              status=status.HTTP_401_UNAUTHORIZED)
            
            if request.user.role not in roles:
                return Response({
                    'error': 'Insufficient permissions',
                    'required_roles': roles,
                    'user_role': request.user.role
                }, status=status.HTTP_403_FORBIDDEN)
            
            return view_func(self, request, *args, **kwargs)
        return _wrapped_view
    return decorator