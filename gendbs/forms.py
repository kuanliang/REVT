from django.forms import ModelForm
from gensite.gendbs.models import *

class ExpForm(ModelForm):
	class Meta:
		model = Experiment
		
