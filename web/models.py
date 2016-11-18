#-*- coding:utf-8 -*-
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse
import django.utils.timezone

# Create your models here.
@python_2_unicode_compatible
class WebUser(models.Model):
    user_name = models.CharField('用户名', max_length=100)
    password = models.CharField('密码', max_length=100)
    email = models.EmailField('邮箱', max_length=100)
    addr = models.CharField('address', max_length=40)

    def __str__(self):
        return self.user_name

    def __unicode__(self):
        return self.user_name


@python_2_unicode_compatible
class Words(models.Model):
    txid = models.CharField('txid', max_length=40)
    # text = models.CharField('誓言', max_length=200)
    user_id = models.IntegerField()

    def __str__(self):
        return self.txid
