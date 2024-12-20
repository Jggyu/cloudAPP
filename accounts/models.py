from django.db import models

class User(models.Model):
    student_id = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)
    programming_language = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'users'