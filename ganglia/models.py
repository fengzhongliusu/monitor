from django.db import models

# Create your models here.

class Resource(models.Model):
	res_hostname = models.CharField(max_length=200)
	res_name = models.CharField(max_length=200)
	res_type = models.CharField(max_length=200,default='hardware')
	def __unicode__(self):
		return self.res_name

class Metric(models.Model):
	resource = models.ForeignKey(Resource)
	metric_name = models.CharField(max_length=200)
	mtr_hostname = models.CharField(max_length=200)
	def __unicode__(self):
		return self.metric_name


	
	
