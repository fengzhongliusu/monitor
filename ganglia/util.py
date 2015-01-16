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
