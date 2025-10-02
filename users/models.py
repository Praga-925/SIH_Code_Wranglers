from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom User model extending AbstractUser with role-based access
    """
    ROLE_CHOICES = [
        ('engineer', 'Engineer'),
        ('metallurgist', 'Metallurgist'),
        ('admin', 'Admin'),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='engineer',
        help_text='User role in the LCA system'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def is_engineer(self):
        return self.role == 'engineer'
    
    @property
    def is_metallurgist(self):
        return self.role == 'metallurgist'
    
    @property
    def is_admin_role(self):
        return self.role == 'admin'
