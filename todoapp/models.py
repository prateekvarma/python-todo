from django.db import models
from django.contrib.auth.models import User

#Difference in blank & null -> Blank is used in textfield and chars, while null+blank is used for datetime

class Todo(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecomlpleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
