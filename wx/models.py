from django.db import models

# Create your models here.
class wxUser(models.Model):
	# id = models.AutoField(primary_key = True)
	openID = models.CharField(max_length = 30)
	# name = models.CharField(max_length = 20)
	address = models.CharField(max_length = 40) # length - 34
	def __unicode__(self):
		return self.address

class wxContent(models.Model):
	user = models.ForeignKey(wxUser)
	txid = models.CharField(max_length = 70) # length - 64
	count = models.CharField(max_length = 3)
	# sub = models.CharField(max_length = 10)
	def __unicode__(self):
		return self.txid