from __future__ import print_function
import sys
import rdflib
from lxml import etree
import json

def eprint(*args, **kwargs):
   print(*args, file=sys.stderr, **kwargs)

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
       service['version'] = res
       res = item.xpath("//mrd:MD_Format/mrd:formatDistributor/mrd:MD_Distributor/mrd:distributorTransferOptions/mrd:MD_DigitalTransferOptions/mrd:onLine/cit:CI_OnlineResource/cit:linkage/gco:CharacterString/text()", namespaces=default_ns)
       service['url'] = res
       res = item.xpath("//mrd:MD_Format/mrd:formatDistributor/mrd:MD_Distributor/mrd:distributorTransferOptions/mrd:MD_DigitalTransferOptions/mrd:onLine/cit:CI_OnlineResource/cit:name/gco:CharacterString/text()", namespaces=default_ns)
       service['name'] = res
       res = item.xpath("//mrd:MD_Format/mrd:formatDistributor/mrd:MD_Distributor/mrd:distributorTransferOptions/mrd:MD_DigitalTransferOptions/mrd:onLine/cit:CI_OnlineResource/cit:protocol/gco:CharacterString/text()", namespaces=default_ns)
       service['type'] = res
       serviceList.append(service)
    return serviceList

def iso2dpn(isofile):
    serviceList = extract_service_info(isofile)
    print(json.dumps(serviceList, indent=3))

if __name__ == "__main__":
    if(len(sys.argv) < 2):
        eprint("Usage: python " + sys.argv[0] + " [iso-19115 XML file]")
        exit(1)

    iso2dpn(sys.argv[1])
