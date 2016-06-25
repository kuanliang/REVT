from django.db import models
from django.contrib.auth.models import User

class TypeDB(models.Model):
	name = models.CharField(max_length=30)
	desc = models.TextField(null=True, blank=True)

	def __unicode__(self):
		return self.name
	class Meta:
		ordering = ['id']

class RefDB(models.Model):
	typedb = models.ForeignKey(TypeDB)
	name = models.CharField(max_length=30)
	desc = models.CharField(max_length=500, null=True, blank=True)

	def __unicode__(self):
		return self.name
	class Meta:
		ordering = ['id']

class Extraction(models.Model):
	name = models.CharField(max_length=30)
	desc = models.CharField(max_length=500, null=True, blank=True)

	def __unicode__(self):
		return self.name
	class Meta:
		ordering = ['id']

class Classifier(models.Model):
	name = models.CharField(max_length=30)
	desc = models.CharField(max_length=500, null=True, blank=True)

	def __unicode__(self):
		return self.name
	class Meta:
		ordering = ['id']

class HyperVariable(models.Model):
	typedb = models.ForeignKey(TypeDB)
	value = models.IntegerField()
	accuracy = models.DecimalField(default=0, max_digits=12, decimal_places=11)
	entropy = models.DecimalField(default=0, max_digits=12, decimal_places=11)
	
	def __unicode__(self):
		return u'%d :%10f' % (self.value, self.accuracy)
	class Meta:
		ordering = ['id']

class Primer(models.Model):
	typedb = models.ForeignKey(TypeDB)
	name = models.CharField(max_length=20)
	position_start = models.IntegerField(default=0)
	position_end = models.IntegerField(default=0)
	position_top = models.FloatField(default=0.4)
	desc = models.CharField(max_length=200, null=True, blank=True)
	
	def __unicode__(self):
		return u'%s (%d-%d)' % (self.name, self.position_start, self.position_end)
	class Meta:
		ordering = ['id']


class Vregion(models.Model):
	typedb = models.ForeignKey(TypeDB)
	name = models.CharField(max_length=10)
	position_start = models.IntegerField()
	position_end = models.IntegerField()
	position_top = models.FloatField(default=0.8)
	desc = models.CharField(max_length=200, null=True, blank=True)
	
	def __unicode__(self):
		return u'%s (%d-%d)' % (self.name, self.position_start, self.position_end)
	class Meta:
		ordering = ['id']


class Tax(models.Model):
	name = models.CharField(max_length=30)
	desc = models.TextField(blank=True, null=True)
	
	def __unicode__(self):
		return u'%s' % self.name
	class Meta:
		ordering = ['id']


class Experiment(models.Model):
	name = models.CharField(max_length=30)
	typedb = models.ForeignKey(TypeDB)
	users = models.ForeignKey(User)
	refdb = models.ForeignKey(RefDB)
	extraction = models.ForeignKey(Extraction)
	vregion = models.ForeignKey(Vregion, blank=True, null=True)
	primer = models.ForeignKey(Primer, blank=True, null=True)
	classifier = models.ForeignKey(Classifier)
	specific = models.BooleanField(default=0)
	start = models.IntegerField()
	end = models.IntegerField()
	bootstrap = models.DecimalField(default=0, max_digits=12, decimal_places=11)
	desc = models.TextField(blank=True, null=True)
	create_date = models.DateField(auto_now=False, auto_now_add=True)
	execute_date = models.DateField(blank=True, null=True)
	is_execute = models.BooleanField(default=0)

	def __unicode__(self):
		return u'%d.%s' % (self.id, self.name)

class Result(models.Model):
	exp_id = models.ForeignKey(Experiment)
	tax_id = models.ForeignKey(Tax)
	accuracy = models.DecimalField(default=0, max_digits=16, decimal_places=15)
	bootstrap = models.DecimalField(default=0, max_digits=16, decimal_places=15)
	remain = models.DecimalField(default=0, max_digits=16, decimal_places=15)

	def __unicode__(self):
		return u'%s %s %10f' % (self.exp_id, self.tax_id, self.accuracy)
	class Meta:
		ordering = ['id', 'exp_id', 'tax_id']

