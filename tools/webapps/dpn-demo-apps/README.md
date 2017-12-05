# ncld-demo-apps
netCDF-LD demo web apps

## Pre-requisites
* docker
* docker-compose (v3)

## Quickstart 
```
#Step 1. init webapp and fuseki containers
$ docker-compose up 

#Step 2. in the web console (http://localhost:3030), create the dataset 'ncld'

#Step 3. stop the containers by Control-C

#Step 4. use docker-compose script to load data in the rdf/ dir
$ docker-compose -f docker-compose-load.yml up 

#Step 5. use docker-compose script to load data in the rdf/ dir
$ docker-compose -f docker-compose-load.yml up 

#Done! You can navigate to http://localhost:8088 for the demo-app, 
# and http://localhost:3030 for fuseki sparql

```

