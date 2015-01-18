#import rrdtool
#from ganglia.models import Resource,Metric,Host
import os
import jpype

def get_relate(res_list):
	if len(res_list) == 0:	#list is empty
		return 	
	if len(res_list[0].res_related) > 0:	#already reduced
		return 
	base_path = "/home/ganglia/django_proj/monitor/ganglia/metric/"
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
	
'''
generate images for metrics in the resource
'''
def res_img(metric_list):
	res_img_list = {}
	for metric in metric_list:
		hostname = str(metric.mtr_hostname)
		m_name = str(metric.metric_name)
		generate_img(hostname,m_name,'hour')
		generate_img(hostname,m_name,'day')
		generate_img(hostname,m_name,'week')
		generate_img(hostname,m_name,'month')
		metric_imgpath = ['ganglia/images/%s_hour.png' % m_name,
			'ganglia/images/%s_day.png' % m_name,
			'ganglia/images/%s_week.png'% m_name,
			'ganglia/images/%s_month.png' % m_name]	
		res_img_list[m_name] = metric_imgpath
	return res_img_list


def generate_img(host_name,metric_name,time):
	img_path = "/home/ganglia/django_proj/monitor/ganglia/static/ganglia/images/"
	rrd_path = "/var/lib/ganglia/rrds/my\ cluster/"+host_name+"/"+metric_name.lower()+".rrd"
	if time == "hour":
		rrdtool_graph(img_path+metric_name+'_hour.png',rrd_path,'end-1h','now',metric_name,'180')
	elif time == "day":
		rrdtool_graph(img_path+metric_name+'_day.png',rrd_path,'end-1d','now',metric_name,'4320')
	elif time == "week":
		rrdtool_graph(img_path+metric_name+'_week.png',rrd_path,'end-1w','now',metric_name,'30240')
	elif time == "month":
		rrdtool_graph(img_path+metric_name+'_month.png',rrd_path,'end-1m','now',metric_name,'129600')
	else:
		return 


def rrdtool_graph(i_path,r_path,start,end,mtric_name,step):	
	print r_path
	command = "rrdtool graph %s --end %s --start %s --width 250 --height 150 DEF:ds=%s:sum:AVERAGE:step=%s AREA:ds#0000FF:%s" % (i_path,end,start,r_path,step,mtric_name)
	os.system(command)



'''def rrdtool_graph(i_path,r_path,start,end,mtric_name,step):	
	rrdtool.graph(i_path,'--imgformat','PNG',
	'--width','250',
	'--height','150',
	'--start',start,
	'--end',end,
	'--vertical-label','sum',
	'--title',mtric_name,
	'DEF:ds=%s:sum:AVERAGE:step=%s' % (r_path,step),
	'AREA:ds#CC00FF:%s' % mtric_name
	)
'''


if __name__ == "__main__":
	generate_img("localhost","cpu_user","hour")
