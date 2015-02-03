#!/bin/bash

FILES="dpn
dpn-services
dpn-dataset"

for file in $FILES
do 
   java -jar jar/rdf2rdf-1.0.1-2.3.1.jar ${file}.ttl ${file}.rdf
done

