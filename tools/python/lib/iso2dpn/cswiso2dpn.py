from __future__ import print_function
import sys
#import rdflib
#from rdflib import Graph, URIRef, BNode, Literal
#from rdflib.namespace import RDF, RDFS
#from rdflib.namespace import Namespace, NamespaceManager
#from lxml import etree
#import json
#import hashlib
import os
from iso2dpn import common
from iso2dpn import cswcrawler
import argparse


def crawl(csw_endpoint, num_records=10, writedir=None):
    outfile = 'out.txt'
    #cswcrawler.query_csw(outfile, csw_endpoint, 5, 10, cswcrawler.print_csw_record)

    #std out only
    #cswcrawler.query_csw(outfile, csw_endpoint, 5, 10, cswcrawler.csw_record_to_dpn)
    
    #writedir
    dir = writedir

    if not os.path.exists(dir):
        os.makedirs(dir)
    print(csw_endpoint)
    cswcrawler.query_csw(outfile, csw_endpoint, num_records, 10, cswcrawler.csw_record_to_dpn, writedir=dir)
    

def main():

    parser = argparse.ArgumentParser(description='Crawl CSW for ISO records and convert to DPN Ontology RDF.')
    parser.add_argument('--num_records', dest='num_records', type=int, default=10, help='Number of records')
    parser.add_argument('--writedir', dest='writedir', default=None, help='Write dir for RDF')
    parser.add_argument('csw_endpoint',  help='CSW endpoint')

    #if(len(sys.argv) < 2):
    #   eprint("Usage: python " + sys.argv[0] + " [CSW endpoint]")
    args = parser.parse_args()

    crawl(args.csw_endpoint, num_records=args.num_records, writedir=args.writedir)


if __name__ == "__main__":
   main()

