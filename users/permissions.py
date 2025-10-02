"""
Custom permission classes for role-based access control in LCA Tool
"""
from rest_framework import permissions


class IsAdminRole(permissions.BasePermission):
    """
    Permission to only allow admin role users to access the view.
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role == 'admin'
        )


class IsMetallurgistOrAdmin(permissions.BasePermission):
    """
    Permission to allow metallurgist and admin roles to access the view.
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role in ['metallurgist', 'admin']
        )


class IsEngineerOrAbove(permissions.BasePermission):
    """
    Permission to allow engineer, metallurgist, and admin roles to access the view.
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role in ['engineer', 'metallurgist', 'admin']
        )


class CanUploadDatasets(permissions.BasePermission):
    """
    Permission to upload datasets - only admin and metallurgist can upload.
    """
    def has_permission(self, request, view):
        # Read access for all authenticated users
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Write access only for admin and metallurgist
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role in ['metallurgist', 'admin']
        )


class CanRunLCA(permissions.BasePermission):
    """
    Permission to run LCA analysis - all roles can run LCA.
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role in ['engineer', 'metallurgist', 'admin']
        )


class CanManageAIModels(permissions.BasePermission):
    """
    Permission to manage AI models - only admin and metallurgist.
    """
    def has_permission(self, request, view):
        # Read access for all authenticated users
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Write/Delete access only for admin and metallurgist
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role in ['metallurgist', 'admin']
        )


class CanViewReports(permissions.BasePermission):
    """
    Permission to view reports - all roles can view their own reports.
    Admin can view all reports.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Admin can access all reports
        if request.user.role == 'admin':
            return True
        
        # Users can only access their own reports
        return obj.created_by == request.user


class CanManageUsers(permissions.BasePermission):
    """
    Permission to manage users - only admin can create/modify/delete users.
    """
    def has_permission(self, request, view):
        # All authenticated users can view user list and their own profile
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Only admin can create/modify/delete users
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role == 'admin'
        )


class RoleBasedPermission(permissions.BasePermission):
    """
    Generic role-based permission class.
    Usage: Set required_roles in the view.
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        
        # Get required roles from the view
        required_roles = getattr(view, 'required_roles', [])
        if not required_roles:
            return True  # No specific role requirement
        
        return request.user.role in required_roles


# Role hierarchy for easy permission checking
ROLE_HIERARCHY = {
    'admin': 3,
    'metallurgist': 2, 
    'engineer': 1
}


class MinimumRolePermission(permissions.BasePermission):
    """
    Permission based on minimum role level.
    Usage: Set minimum_role in the view.
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        
        minimum_role = getattr(view, 'minimum_role', 'engineer')
        user_role_level = ROLE_HIERARCHY.get(request.user.role, 0)
        required_role_level = ROLE_HIERARCHY.get(minimum_role, 0)
        
        return user_role_level >= required_role_level