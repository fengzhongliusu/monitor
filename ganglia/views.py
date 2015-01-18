from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from ganglia.models import Resource,Metric,Host
import jpype
import json
from ganglia.util import get_relate,str_to_list,res_img


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

	#generate graph for every metric
	path_list = res_img(metric_list)
	
	mtc_list = []
	for metric in metric_list:
		mtc= {}
		mtc["mtc_name"] = metric.metric_name
		mtc['img_path'] = path_list[metric.metric_name]
		mtc_list.append(mtc)

	rel_namelist = str_to_list(res.res_related)
	rel_list = []
	for rel_name in rel_namelist:
		"""attention after filter you get a list"""
		rel_fil = Resource.objects.filter(res_name=rel_name.strip(),res_hostname=res.res_hostname)
		if not len(rel_fil)==0:
			rel_list.append(rel_fil[0])
	return render(request,"ganglia/detail.html",{'resource':res,'metric_list':mtc_list,'relate_list':rel_list})


