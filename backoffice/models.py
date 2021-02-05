from django.db import models
from customers.models import User

class Dashboard(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.user.first_name

#? not in use yet unless wants to 
# class EmailContent(models.Model):
#     name = models.CharField(max_length=100)
#     content = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return self.name
