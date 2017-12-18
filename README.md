Data Provider Node Ontology
===========================

![Travis CI Build status](https://travis-ci.org/CSIRO-LW-LD/dpn-ontology.svg?branch=master)

This ontology is being developed by CSIRO for describing data provider nodes, web services available and datasets that are hosted by them. This ontology features a module for describing Datasets. It does not however describe geospatial, temporal, organisational or domain concepts as these are intended to be included from other ontologies via the imports statement. Other modules complementary to the DPN ontology are:
* http://purl.org/dpn/dataset
* http://purl.org/dpn/services 

This version aligns DCAT and DC terms and imports DPN services.


This repository contains the master definition files for Data Provider Node and related concepts.

These processed and then be published in .ttl, .rdf and .html formats as per the following:
- dpn.ttl => <http://purl.org/dpn>.
- dpn-services.ttl => <http://purl.org/dpn/services>
- dpn-dataset.ttl => <http://purl.org/dpn/dataset>
