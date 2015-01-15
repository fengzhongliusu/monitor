from django.shortcuts import render
from django.http import HttpResponse
from ganglia.models import Resource,Metric


# Create your views here.

def index(request):
	resource_list = Resource.objects.all()
	context = {'resource_list': resource_list}
	return render(request,'ganglia/index.html',context)

def detail(request,metric_id):
	return HttpResponse("This for detail info for Metric %s." % metric_id)

