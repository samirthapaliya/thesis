# External Improt
from .models import Worker
from django.forms import ModelForm

class WorkerProfileForm(ModelForm):
    class Meta:
     model=Worker
     fields= '__all__'
    
class EditWorkerForm(ModelForm):
    class Meta:
        model = Worker
        fields = ["name","picture","phone"]