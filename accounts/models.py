from django.db import models


class CustomUser(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150 )
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    phone = models.IntegerField(blank=False)

    class Meta:
        db_table = "custom_user"
