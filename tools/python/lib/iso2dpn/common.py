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
def extract_service_info_byfile(isofile):
    tree = etree.parse(isofile)
    return extract_service_info(tree)

def extract_service_info_bystring(isostr):
    tree = etree.fromstring(isostr)
    return extract_service_info(tree)

def get_iso19115_3_namespaces():
    return {
            "mdb" : "http://standards.iso.org/iso/19115/-3/mdb/1.0" , 
            "xsi" : "http://www.w3.org/2001/XMLSchema-instance" , 
            "cat" : "http://standards.iso.org/iso/19115/-3/cat/1.0" , 
            "cit" : "http://standards.iso.org/iso/19115/-3/cit/1.0" , 
            "gcx" : "http://standards.iso.org/iso/19115/-3/gcx/1.0" , 
            "gex" : "http://standards.iso.org/iso/19115/-3/gex/1.0" , 
            "lan" : "http://standards.iso.org/iso/19115/-3/lan/1.0" , 
            "srv" : "http://standards.iso.org/iso/19115/-3/srv/2.0" , 
            "mas" : "http://standards.iso.org/iso/19115/-3/mas/1.0" , 
            "mcc" : "http://standards.iso.org/iso/19115/-3/mcc/1.0" , 
            "mco" : "http://standards.iso.org/iso/19115/-3/mco/1.0" , 
            "mda" : "http://standards.iso.org/iso/19115/-3/mda/1.0" , 
            "mds" : "http://standards.iso.org/iso/19115/-3/mds/1.0" , 
            "mdt" : "http://standards.iso.org/iso/19115/-3/mdt/1.0" , 
            "mex" : "http://standards.iso.org/iso/19115/-3/mex/1.0" , 
            "mmi" : "http://standards.iso.org/iso/19115/-3/mmi/1.0" , 
            "mpc" : "http://standards.iso.org/iso/19115/-3/mpc/1.0" , 
            "mrc" : "http://standards.iso.org/iso/19115/-3/mrc/1.0" , 
            "mrd" : "http://standards.iso.org/iso/19115/-3/mrd/1.0" , 
            "mri" : "http://standards.iso.org/iso/19115/-3/mri/1.0" , 
            "mrl" : "http://standards.iso.org/iso/19115/-3/mrl/1.0" , 
            "mrs" : "http://standards.iso.org/iso/19115/-3/mrs/1.0" , 
            "msr" : "http://standards.iso.org/iso/19115/-3/msr/1.0" , 
            "mdq" : "http://standards.iso.org/iso/19157/-2/mdq/1.0" , 
            "mac" : "http://standards.iso.org/iso/19115/-3/mac/1.0" , 
            "gco" : "http://standards.iso.org/iso/19115/-3/gco/1.0" , 
            "gml" : "http://www.opengis.net/gml/3.2" , 
            "xlink" : "http://www.w3.org/1999/xlink" , 
            "geonet" : "http://www.fao.org/geonetwork" , 
            }

def extract_service_info(tree):

    default_ns = get_iso19115_3_namespaces()
    root= tree.xpath("//*",namespaces=default_ns)[0]
    #default_ns = root.nsmap
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
       print(item)
       service = {}
       res = item.xpath("//mrd:MD_Format/mrd:formatSpecificationCitation/cit:CI_Citation/cit:title/gco:CharacterString/text()", namespaces=default_ns)
       service['title'] = res
       res = item.xpath("//mrd:MD_Format/mrd:formatSpecificationCitation/cit:CI_Citation/cit:edition/gco:CharacterString/text()", namespaces=default_ns)
       service['version'] = res [0]
       res = item.xpath("//mrd:MD_Format/mrd:formatDistributor/mrd:MD_Distributor/mrd:distributorTransferOptions/mrd:MD_DigitalTransferOptions/mrd:onLine/cit:CI_OnlineResource/cit:linkage/gco:CharacterString/text()", namespaces=default_ns)
       if(len(res) > 0):
          service['url'] = res[0]
       else:
          print(res)
       res = item.xpath("//mrd:MD_Format/mrd:formatDistributor/mrd:MD_Distributor/mrd:distributorTransferOptions/mrd:MD_DigitalTransferOptions/mrd:onLine/cit:CI_OnlineResource/cit:name/gco:CharacterString/text()", namespaces=default_ns)
       if(len(res) > 0):
          service['name'] = res[0]
       else:
          print(res)
       res = item.xpath("//mrd:MD_Format/mrd:formatDistributor/mrd:MD_Distributor/mrd:distributorTransferOptions/mrd:MD_DigitalTransferOptions/mrd:onLine/cit:CI_OnlineResource/cit:protocol/gco:CharacterString/text()", namespaces=default_ns)
       if(len(res) > 0):
          service['type'] = res[0]
       else:
          print(res)


       #fallback
       if 'name' not in service:
          #check transferOptions distribution
          res = item.xpath("//mrd:transferOptions/mrd:MD_DigitalTransferOptions/mrd:onLine/cit:CI_OnlineResource/cit:linkage/gco:CharacterString/text()", namespaces=default_ns)
          if(len(res) > 0):
             service['url'] = res[0]

          res = item.xpath("//mrd:transferOptions/mrd:MD_DigitalTransferOptions/mrd:onLine/cit:CI_OnlineResource/cit:name/gco:CharacterString/text()", namespaces=default_ns)
          if(len(res) > 0):
             service['name'] = res[0]

          res = item.xpath("//mrd:transferOptions/mrd:MD_DigitalTransferOptions/mrd:onLine/cit:CI_OnlineResource/cit:protocol/gco:CharacterString/text()", namespaces=default_ns)
          if(len(res) > 0):
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

    if('name' in service and 'url' in service):
       # get unique identifier for service instance
       # TODO: Let user specify the identifier as a parameter
       id = abs(hash(service['name'])) % (10 ** 8)

       s = URIRef(ns + str(id))
       g.add( (s, RDF.type, DPN.Service) )
       g.add( (s, RDFS.label, Literal(service['name'])) )
       if service['type'] == "OGC:WFS":
          g.add( (s, DPN.implements, DPNS.WFS) )
       elif service['type'] == "OGC:WMS":
          g.add( (s, DPN.implements, DPNS.WMS) )
       elif service['type'] == "ESRI: Map Service":
          g.add( (s, DPN.implements, DPNS.EsriMapService) )
       else:
           print("Service type: " + service['type'])
       g.add( (s, DPN.endpoint, URIRef(service['url'])) )

    return g

def load_and_graphify(record_id, serviceList, writedir=None):
    eprint("Loading DPN ontology...")
    dpn_g =  get_dpn_ontology()
    eprint("Creating DPN instance graph...")
    instance_g = get_dpn_instance_graph(dpn_g)
    for item in serviceList:
        if('name' in item):
           eprint("Adding DPN service instance to graph... for '" + item['name'] + "'...")
        instance_g = add_service_description(item, instance_g)
    if(writedir):
       fname = writedir + "/" + record_id + '.n3'
       eprint("Emitting RDF to " + fname)
       eprint("--------")
       instance_g.serialize(fname, format='n3')
    else: 
       eprint("Emitting RDF to stdout...")
       eprint("--------")
       print( instance_g.serialize(format='n3').decode("utf-8")  )

def iso2dpn_byfile(record_id, isofile, writedir=None):
    serviceList = extract_service_info_byfile(isofile)
    return load_and_graphify(record_id, serviceList, writedir=writedir)

def iso2dpn_bystring(record_id, isostring, writedir=None):
    serviceList = extract_service_info_bystring(isostring)
    return load_and_graphify(record_id, serviceList, writedir=writedir)

def iso2dpn(id, isoobj, object_type='file', writedir=None):
    if(object_type == 'file'):
       return iso2dpn_byfile(id, isoobj, writedir=writedir)
    else:
       return iso2dpn_bystring(id, isoobj, writedir=writedir)
    #eprint(json.dumps(serviceList, indent=3))



if __name__ == "__main__":
    if(len(sys.argv) < 2):
        eprint("Usage: python " + sys.argv[0] + " [iso-19115 XML file]")
        exit(1)

    iso2dpn(sys.argv[1])
