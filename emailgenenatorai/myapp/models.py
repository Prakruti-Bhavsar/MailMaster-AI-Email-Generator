from django.db import models
from django.contrib.auth.hashers import make_password

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=255, unique=True, primary_key=True)  # Adding email field
    password = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        if not self.pk:  # Only hash password on first save (insert), not on updates
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
