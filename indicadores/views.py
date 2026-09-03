from django.shortcuts import render
from datosarray import periodo, personas
# Create your views here.
def dashboard(request):
    return render(request, 'indicadores/dashboard.html', {'periodo': periodo, 'personas': personas})