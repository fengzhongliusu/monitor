from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from ganglia.models import Resource,Metric,Host
import jpype
import json


# Create your views here.
def index(request):
	host_list = Host.objects.all()
	resource_list = Resource.objects.all()
	get_relate(resource_list)
	context = {'resource_list': resource_list,'host_list':host_list}
	return render(request,'ganglia/index.html',context)

def detail(request,resource_id):
	res = get_object_or_404(Resource,pk=resource_id)
	metric_list = Metric.objects.filter(resource=res)
	rel_list = str_to_list(res.res_related)
	return render(request,"ganglia/detail.html",{'resource':res,'metric_list':metric_list,'relate_list':rel_list})


def get_relate(res_list):
	if len(res_list) == 0:	#list is empty
		return 	
	if len(res_list[0].res_related) > 0:	#already reduced
		return 
	base_path = "/home/ganglia/django_proj/monitor/ganglia/"
	jar_path = base_path + "metric.jar"
	ttl_path = base_path + "metric.ttl"
	rules_path = base_path + "metric.rules"
	if jpype.isJVMStarted():
		print "jvm already running!!!"
	else:
		jpype.startJVM(jpype.getDefaultJVMPath(),"-ea","-Djava.class.path=%s" % jar_path)
        Reason = jpype.JClass("MetricRS")
	reason = Reason(ttl_path,rules_path)
	for res in res_list:
		relate = reason.getRelate(res.res_name);
		res.res_related = str(relate)	
		res.save()
	jpype.shutdownJVM()


def str_to_list(s):
	if len(s) == 2:
	   list_str = [];
	else:	   
	   trip_str = s[1:-1]
	   list_str = trip_str.split(",")
	return list_str
