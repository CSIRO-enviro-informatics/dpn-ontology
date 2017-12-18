from rdflib import Graph
import pkg_resources

def get_dpn_ontology():
   g = Graph()
   dpnfn = "dpn.ttl"
   dpns = "dpn-services.ttl"
   dpnd = "dpn-dataset.ttl"

   g.parse(dpnfn, format='turtle' )
   g.parse(dpns, format='turtle' )
   g.parse(dpnd, format='turtle' )
   return g

def test_load_dpn_ontology():
   assert get_dpn_ontology()
