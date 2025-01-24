from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# class Candidate(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_createdby')

# class Interviewer(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_createdby')

# class HRManager(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_createdby')
# class Candidate(AbstractUser):
#     def __str__(self):
#         return self.username 

# from django.db import models


class CustomUser(AbstractUser):
    USER_TYPES = [
        ('candidate', 'Candidate'),
        ('interviewer', 'Interviewer'),
        ('manager', 'HRManager'),
    ]
    # Add any additional fields here
    type = models.CharField(max_length=15, choices=USER_TYPES, default='candidate')

    def __str__(self):
        return self.username 