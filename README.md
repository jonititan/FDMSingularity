# FDMSingularity
A Singularity recipe for using prefect on a HPC system for flight data analysis

https://docs.prefect.io/



To build the singularity image
```
  $ sudo singularity build fdm.sif fdm.def
```

To launch the image and run a script from local folder
```
  $ singularity run fdm.sif test.py
```

To build the singularity images
```
  $ sudo singularity build fdm.sif fdm.def   
```
```                                     
  $ sudo singularity build post.sif post.def 
```
  
To use
1. Start postgres server instance

Reference command for docker from [Prefect Docs](https://docs.prefect.io/2.10.3/concepts/database/#configuring-a-postgresql-database)
docker run -d --name prefect-postgres -v prefectdb:/var/lib/postgresql/data -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=yourTopSecretPassword -e POSTGRES_DB=prefect postgres:latest

our command
```
  $ singularity instance start --cleanenv --containall --writable-tmpfs --bind ${PWD}/postgres:/var/lib/postgresql/data post.sif prefect-postgres
```

# to access the instance
```
  $ singularity shell -s /bin/bash instance://prefect-postgres
```

2. Run test
```
  $ singularity run --bind ${PWD}/src:/headless fdm.sif test.py
```
