from __future__ import print_function
import sys
import rdflib
from rdflib import Graph, URIRef, BNode, Literal
from rdflib.namespace import RDF, RDFS
from rdflib.namespace import Namespace, NamespaceManager
from lxml import etree
import json
import hashlib

def eprint(*args, **kwargs):
   print(*args, file=sys.stderr, **kwargs)

def get_dpn_ontology():
    g = Graph()
    g.parse("http://purl.org/dpn")
    g.parse("http://purl.org/dpn/services")
    return g


#parses ISO xml file and extracts a list of services with minimal info about the service
def extract_service_info(isofile):
    tree = etree.parse(isofile)
    root= tree.xpath("//*")[0]
    default_ns = root.nsmap
    #res= tree.xpath("//*[local-name() ='SV_ServiceIdentification']")
    res = tree.xpath("//mdb:identificationInfo", namespaces=default_ns)

    serviceList = []

    '''
    for item in res:
       service = {}
       res = item.xpath("//srv:SV_ServiceIdentification/mri:citation/cit:CI_Citation/cit:title/gco:CharacterString/text()", namespaces=default_ns)
       service['title'] = res[0]
       res = item.xpath("//srv:SV_ServiceIdentification/srv:serviceType/gco:ScopedName/text()", namespaces=default_ns)
       service['type'] = res[0]
       res = item.xpath("//srv:SV_ServiceIdentification/srv:serviceTypeVersion/gco:CharacterString/text()", namespaces=default_ns)
       service['versionsList'] = res
       serviceList.append(service)
    '''
    res = tree.xpath("//mdb:distributionInfo/mrd:MD_Distribution", namespaces=default_ns)
    for item in res:
       service = {}
       res = item.xpath("//mrd:MD_Format/mrd:formatSpecificationCitation/cit:CI_Citation/cit:title/gco:CharacterString/text()", namespaces=default_ns)
       service['title'] = res
       res = item.xpath("//mrd:MD_Format/mrd:formatSpecificationCitation/cit:CI_Citation/cit:edition/gco:CharacterString/text()", namespaces=default_ns)
       service['version'] = res [0]
       res = item.xpath("//mrd:MD_Format/mrd:formatDistributor/mrd:MD_Distributor/mrd:distributorTransferOptions/mrd:MD_DigitalTransferOptions/mrd:onLine/cit:CI_OnlineResource/cit:linkage/gco:CharacterString/text()", namespaces=default_ns)
       service['url'] = res [0]
       res = item.xpath("//mrd:MD_Format/mrd:formatDistributor/mrd:MD_Distributor/mrd:distributorTransferOptions/mrd:MD_DigitalTransferOptions/mrd:onLine/cit:CI_OnlineResource/cit:name/gco:CharacterString/text()", namespaces=default_ns)
       service['name'] = res[0]
       res = item.xpath("//mrd:MD_Format/mrd:formatDistributor/mrd:MD_Distributor/mrd:distributorTransferOptions/mrd:MD_DigitalTransferOptions/mrd:onLine/cit:CI_OnlineResource/cit:protocol/gco:CharacterString/text()", namespaces=default_ns)
       service['type'] = res[0]
       serviceList.append(service)
    return serviceList

def get_dpn_service_instances(g):
    qres = g.query(
            """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
               PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
               PREFIX dpn: <http://purl.org/dpn#>
               SELECT ?s
               WHERE {
                  ?s rdfs:subClassOf dpn:Service
               }
            """)

    for row in qres:
       print("%s" % row)

def get_dpn_instance_graph(dpn_graph):
    nm = NamespaceManager(dpn_graph)
    #namespace_manager.bind('dpn', dpn, override=False)
    g = Graph(namespace_manager = nm)
    return g

def add_service_description(service, g, ns="http://example.org/dpn-example/"):
    DPN = Namespace("http://purl.org/dpn#")
    DPNS = Namespace("http://purl.org/dpn/services#")
    NS = Namespace(ns)

    # get unique identifier for service instance
    # TODO: Let user specify the identifier as a parameter
    id = abs(hash(service['name'])) % (10 ** 8)

    s = URIRef(ns + str(id))
    g.add( (s, RDF.type, DPN.Service) )
    g.add( (s, RDFS.label, Literal(service['name'])) )
    if service['type'] == "OGC:WFS":
       g.add( (s, DPN.implements, DPNS.WFS) )
    g.add( (s, DPN.endpoint, URIRef(service['url'])) )

    return g



def iso2dpn(isofile):
    serviceList = extract_service_info(isofile)
    #eprint(json.dumps(serviceList, indent=3))

    eprint("Loading DPN ontology...")
    dpn_g =  get_dpn_ontology()
    eprint("Creating DPN instance graph...")
    instance_g = get_dpn_instance_graph(dpn_g)
    for item in serviceList:
       eprint("Adding DPN service instance to graph... for '" + item['name'] + "'...")
       instance_g = add_service_description(item, instance_g)

    eprint("Emitting RDF to stdout...")
    eprint("--------")
    print( instance_g.serialize(format='n3').decode("utf-8")  )

def main():
    if(len(sys.argv) < 2):
       eprint("Usage: python " + sys.argv[0] + " [iso-19115 XML file]")
       exit(1)
    iso2dpn(sys.argv[1])


if __name__ == "__main__":
   main()

