# FDMSingularity
A Singularity recipe for using prefect on a HPC system for flight data analysis

https://docs.prefect.io/


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
  $ singularity instance start -B pgdata:/var/lib/postgresql/data -B pgrun:/var/run/postgresql -e -C --env-file post.envs post.sif  prefect-postgres
```

To access the instance
```
  $ singularity shell -s /bin/bash instance://prefect-postgres
```

1. Run test
```
  $ singularity run fdm.sif test.py
```
