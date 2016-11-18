from django.db import models

# Create your models here.
class User(models.Model):
	# id = models.AutoField(primary_key = True)
	openID = models.CharField(max_length = 30)
	# name = models.CharField(max_length = 20)
	address = models.CharField(max_length = 40) # length - 34
	def __str__(self):
		return self.address

class Content(models.Model):
	user = models.ForeignKey(User)
	txid = models.CharField(max_length = 70) # length - 64
	count = models.CharField(max_length = 3)
	# sub = models.CharField(max_length = 10)
	def __str__(self):
		return self.txid