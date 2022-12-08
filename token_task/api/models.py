from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ID_TYPE_CHOICES = [
        ('phone', 'phone'),
        ('mail', 'mail'),
    ]
    
    phone_number = models.CharField(
        'Номер телефона пользователя',
        max_length=20,
        blank=True,
        help_text='Номер телефона в формате +79998887766')
    id_type = models.CharField(
        max_length=5,
        choices=ID_TYPE_CHOICES,
        default='mail',
        blank=True
    )
    
    REQUIRED_FIELDS = ['password']
    USERNAME_FIELD = 'username'
