"""
Swagger decorators for JWT authentication
"""

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# JWT Bearer token parameter for Swagger documentation
jwt_header_param = openapi.Parameter(
    'Authorization',
    openapi.IN_HEADER,
    description="JWT Bearer token (format: 'Bearer <token>')",
    type=openapi.TYPE_STRING,
    required=True
)

# Common JWT responses
jwt_unauthorized_response = openapi.Response(
    'Unauthorized - Invalid or missing JWT token',
    examples={
        'application/json': {
            'detail': 'Given token not valid for any token type',
            'code': 'token_not_valid',
            'messages': [
                {
                    'token_class': 'AccessToken',
                    'token_type': 'access',
                    'message': 'Token is invalid or expired'
                }
            ]
        }
    }
)

jwt_forbidden_response = openapi.Response(
    'Forbidden - Insufficient permissions for this role',
    examples={
        'application/json': {
            'detail': 'You do not have permission to perform this action.'
        }
    }
)


def jwt_required_operation(**kwargs):
    """
    Decorator for operations that require JWT authentication
    """
    default_responses = {
        401: jwt_unauthorized_response,
        403: jwt_forbidden_response,
    }
    
    # Merge with custom responses if provided
    responses = kwargs.get('responses', {})
    responses.update(default_responses)
    kwargs['responses'] = responses
    
    # Add JWT header parameter
    manual_parameters = kwargs.get('manual_parameters', [])
    manual_parameters.append(jwt_header_param)
    kwargs['manual_parameters'] = manual_parameters
    
    return swagger_auto_schema(**kwargs)


def admin_only_operation(**kwargs):
    """
    Decorator for admin-only operations
    """
    if 'operation_description' not in kwargs:
        kwargs['operation_description'] = 'This operation requires admin role access.'
    
    kwargs['tags'] = kwargs.get('tags', []) + ['Admin Only']
    
    return jwt_required_operation(**kwargs)


def role_based_operation(required_roles=None, **kwargs):
    """
    Decorator for role-based operations
    
    Args:
        required_roles: List of roles that can access this operation
    """
    if required_roles:
        roles_str = ', '.join(required_roles)
        if 'operation_description' not in kwargs:
            kwargs['operation_description'] = f'This operation requires one of these roles: {roles_str}'
        
        kwargs['tags'] = kwargs.get('tags', []) + [f'Roles: {roles_str}']
    
    return jwt_required_operation(**kwargs)