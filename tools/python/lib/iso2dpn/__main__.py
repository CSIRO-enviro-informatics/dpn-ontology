from __future__ import print_function
import sys
import rdflib
from rdflib import Graph, URIRef, BNode, Literal
from rdflib.namespace import RDF, RDFS
from rdflib.namespace import Namespace, NamespaceManager
from lxml import etree
import json
import hashlib
from iso2dpn import common


def main():
    if(len(sys.argv) < 2):
        eprint("Usage: python " + sys.argv[0] + " [iso-19115 XML file]")
        exit(1)
    common.iso2dpn(sys.argv[1])


if __name__ == "__main__":
    main()
