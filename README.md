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
  
To use as a single script
1. Create the folders needed
```
  $ mkdir pgrun
```
```
  $ mkdir pgdata
```

2. Start postgres server instance

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

3. Run test
```
  $ singularity run fdm.sif test.py
```


To use as a prefect server
1. Create the folders needed
```
  $ mkdir pgrun
```
```
  $ mkdir pgdata
```

2. Start postgres server instance

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

3. Start prefect server instance
```
  $ singularity instance start fdm.sif prefect-server

```

4. Login to the prefect server instance
```
  $ singularity shell -s /bin/bash instance://prefect-server

```
5. Activate the conda environment in the shell instance
```
  $ conda activate fdm

```
6. Start prefect
```
  $ prefect server start

```


Errata
If you have GPU's you wish to include or your code needs them numba and dask-cuda are included in the fdm image and you can enable gpu pass through by including the --nv flag when you launch via "run" or via "instance start"
