from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model, authenticate, login as django_login, logout as django_logout
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import (
    RegisterSerializer,      # Specification-compliant
    UserSerializer,         # Specification-compliant
    UserRegistrationSerializer,  # Existing
    UserLoginSerializer,         # Existing
    UserProfileSerializer,       # Existing
    UserUpdateSerializer,        # Existing
    ChangePasswordSerializer     # Existing
)
from .permissions import (
    CanManageUsers,
    IsAdminRole,
    IsEngineerOrAbove
)
from .decorators import (
    api_role_required,
    AdminOnlyMixin,
    OwnershipMixin,
    log_permission_check
)

User = get_user_model()


# Specification-compliant views
class RegisterView(generics.CreateAPIView):
    """
    Register new user - matches specification
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Register a new user with role assignment",
        operation_summary="User Registration",
        tags=['Authentication'],
        request_body=RegisterSerializer,
        responses={
            201: openapi.Response(
                'User created successfully',
                RegisterSerializer,
                examples={
                    'application/json': {
                        'id': 1,
                        'username': 'newuser',
                        'email': 'user@example.com',
                        'role': 'engineer',
                        'first_name': 'John',
                        'last_name': 'Doe'
                    }
                }
            ),
            400: openapi.Response('Bad Request - Validation errors')
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    Get and update user profile
    Specification: Users can view and update their own profiles
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        """Return the current user's profile"""
        return self.request.user
    
    def get_permissions(self):
        """Allow profile updates only for profile owner or admin"""
        if self.request.method in ['PUT', 'PATCH']:
            return [IsAuthenticated(), (OwnershipMixin() | IsAdminRole())]
        return [IsAuthenticated()]
    
    @swagger_auto_schema(
        operation_description="Get current user's profile information",
        operation_summary="Get User Profile",
        tags=['User Profile'],
        responses={
            200: openapi.Response('User profile data', UserSerializer)
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Update current user's profile information",
        operation_summary="Update User Profile",
        tags=['User Profile'],
        request_body=UserSerializer,
        responses={
            200: openapi.Response('Profile updated successfully', UserSerializer)
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Partially update current user's profile",
        operation_summary="Partial Profile Update",
        tags=['User Profile'],
        request_body=UserSerializer,
        responses={
            200: openapi.Response('Profile updated successfully', UserSerializer)
        }
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class UserListView(AdminOnlyMixin, generics.ListAPIView):
    """
    List all users (admin only)
    Specification: Only admins can view all users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, CanManageUsers]
    
    def get_queryset(self):
        """Optional: Filter users by role if query parameter provided"""
        queryset = super().get_queryset()
        role = self.request.query_params.get('role', None)
        
        if role and role in ['engineer', 'metallurgist', 'admin']:
            queryset = queryset.filter(role=role)
            
        return queryset.order_by('-date_joined')
    
    @swagger_auto_schema(
        operation_description="List all users in the system. Only accessible by admin users.",
        operation_summary="List All Users (Admin Only)",
        tags=['User Management'],
        manual_parameters=[
            openapi.Parameter(
                'role',
                openapi.IN_QUERY,
                description="Filter users by role (engineer, metallurgist, admin)",
                type=openapi.TYPE_STRING,
                enum=['engineer', 'metallurgist', 'admin']
            )
        ],
        responses={
            200: openapi.Response('List of users', UserSerializer(many=True))
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UserManagementView(AdminOnlyMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Admin-only user management (get, update, delete specific user)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, CanManageUsers]
    lookup_field = 'id'
    
    @log_permission_check
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @log_permission_check
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
    @log_permission_check
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
    
    @log_permission_check
    def delete(self, request, *args, **kwargs):
        # Prevent admin from deleting themselves
        if self.get_object() == request.user:
            return Response(
                {'error': 'Cannot delete your own account'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().delete(request, *args, **kwargs)


# Existing views (for backward compatibility with simple session auth)
@api_view(['POST'])
@permission_classes([AllowAny])
@log_permission_check
def register(request):
    """
    User registration endpoint
    """
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # Simple response without JWT tokens
        user_data = UserProfileSerializer(user).data
        user_data['permissions'] = {
            'is_admin': user.is_admin_role,
            'is_metallurgist': user.is_metallurgist,
            'is_engineer': user.is_engineer,
            'role': user.role
        }
        
        return Response({
            'message': 'User created successfully',
            'user': user_data,
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
@log_permission_check
def login(request):
    """
    User login endpoint with simple session authentication
    """
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        
        # Use Django's built-in session authentication
        django_login(request, user)
        
        # Include role information for frontend
        user_data = UserProfileSerializer(user).data
        user_data['permissions'] = {
            'is_admin': user.is_admin_role,
            'is_metallurgist': user.is_metallurgist,
            'is_engineer': user.is_engineer,
            'role': user.role
        }
        
        return Response({
            'message': 'Login successful',
            'user': user_data,
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@log_permission_check
def logout(request):
    """
    User logout endpoint - simple session logout
    """
    try:
        django_logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': 'Invalid logout request'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveAPIView):
    """
    Get current user profile (legacy view for backward compatibility)
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    @log_permission_check
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UserUpdateView(generics.UpdateAPIView):
    """
    Update current user profile (legacy view for backward compatibility)
    """
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    @log_permission_check
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({
            'message': 'Profile updated successfully',
            'user': UserProfileSerializer(self.get_object()).data
        })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@log_permission_check
def change_password(request):
    """
    Change user password
    """
    serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({'message': 'Password changed successfully'})
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Legacy UserListView removed - using the role-based UserListView defined above


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@swagger_auto_schema(
    operation_description="""
    Test endpoint to verify authentication and role-based permissions.
    
    **How to use:**
    1. Login with POST /api/users/login-alt/ 
    2. Use session authentication to call this endpoint
    3. View your permissions and role information
    
    **Returns detailed permission information for your role:**
    - User profile data
    - Permission test results
    - Role-based capability matrix
    """,
    operation_summary="Test Auth & Permissions",
    tags=['Testing'],
    responses={
        200: openapi.Response(
            'Permission test results with user capabilities',
            examples={
                'application/json': {
                    "user": {
                        "id": 1,
                        "username": "admin_test",
                        "role": "admin",
                        "is_admin_role": True,
                        "is_metallurgist": True,
                        "is_engineer": True
                    },
                    "permissions": {
                        "can_manage_users": True,
                        "can_upload_datasets": True,
                        "can_manage_ai_models": True,
                        "can_view_reports": True,
                        "is_admin": True,
                        "is_engineer_or_above": True
                    }
                }
            }
        )
    }
)
def test_permissions(request):
    """
    Test endpoint to verify role-based permissions
    Returns user's role and permission capabilities
    """
    user = request.user
    
    # Test various permission checks
    from .permissions import (
        CanManageUsers, CanUploadDatasets, CanManageAIModels, 
        CanViewReports, IsAdminRole, IsEngineerOrAbove
    )
    
    permission_tests = {
        'can_manage_users': CanManageUsers().has_permission(request, None),
        'can_upload_datasets': CanUploadDatasets().has_permission(request, None),
        'can_manage_ai_models': CanManageAIModels().has_permission(request, None),
        'can_view_reports': CanViewReports().has_permission(request, None),
        'is_admin': IsAdminRole().has_permission(request, None),
        'is_engineer_or_above': IsEngineerOrAbove().has_permission(request, None),
    }
    
    return Response({
        'user': {
            'id': user.id,
            'username': user.username,
            'role': user.role,
            'is_admin_role': user.is_admin_role,
            'is_metallurgist': user.is_metallurgist,
            'is_engineer': user.is_engineer,
        },
        'permissions': permission_tests,
        'capabilities': {
            'admin': {
                'manage_users': user.role == 'admin',
                'upload_datasets': user.role == 'admin',
                'manage_ai_models': user.role == 'admin',
                'view_reports': user.role == 'admin',
                'run_lca': user.role == 'admin',
            },
            'metallurgist': {
                'manage_users': False,
                'upload_datasets': user.role in ['metallurgist', 'admin'],
                'manage_ai_models': user.role in ['metallurgist', 'admin'],
                'view_reports': user.role in ['metallurgist', 'admin'],
                'run_lca': user.role in ['metallurgist', 'admin'],
            },
            'engineer': {
                'manage_users': False,
                'upload_datasets': False,
                'manage_ai_models': False,
                'view_reports': user.role in ['engineer', 'metallurgist', 'admin'],
                'run_lca': user.role in ['engineer', 'metallurgist', 'admin'],
            }
        }
    })
