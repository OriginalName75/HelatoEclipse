from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render

from BDD.models import Groupe, horaireProf


# Create your views here.
@login_required(login_url='/connexion')
@user_passes_test(lambda u: u.is_superuser)
def home(request):
        h=horaireProf.objects.all()   
        return render(request, 'GeneEDT/home.html', locals())   
    
    