from FuXi.SPARQL.BackwardChainingStore import TopDownSPARQLEntailingStore
from FuXi.Horn.HornRules import HornFromN3
from rdflib.Graph import Graph
from rdflib import Namespace
from pprint import pprint

'''
function for reasoning the related res of the spefified resource
'''
def reason_func(resource_name):
    famNs = Namespace('file:///home/cshuo/Documents/test/metric.n3#')
    nsMapping = {'mtc' : famNs}
    rules = HornFromN3('metric_rule.n3')
    factGraph = Graph().parse('metric.n3',format='n3')
    factGraph.bind('mtc',famNs)
    dPreds = [famNs.relateTo]

    topDownStore=TopDownSPARQLEntailingStore(factGraph.store,factGraph,idb=rules,derivedPredicates = dPreds,nsBindings=nsMapping)
    targetGraph = Graph(topDownStore)
    targetGraph.bind('ex',famNs)
    #get list of the related resource 
    r_list = list(targetGraph.query('SELECT ?RELATETO { mtc:%s mtc:relateTo ?RELATETO}' % resource_name,initNs=nsMapping))
    
    res_list = []
    for res in r_list:
        res_list.append(str(res).split("#")[1]);
    return res_list


if __name__ == "__main__":
    print reason_func("Cpu")

    
