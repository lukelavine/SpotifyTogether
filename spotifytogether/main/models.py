from django.db import models

# Create your models here.

class User(models.Model):
	user_id = models.CharField(max_length=64, primary_key=True)
	display_name = models.CharField(max_length=128)
	clf1 = models.BinaryField()
	clf2 = models.BinaryField()
	clf3 = models.BinaryField()
	clf4 = models.BinaryField()