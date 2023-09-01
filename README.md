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

You will then need to transfer these images to wherever you want to run them.  



  
## To use as a single script
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


## To use as a prefect server
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

It will automatically start the prefect server as the startscript in fdm.def has been updated to make that happen when the image is run as an instance.

```
5. Run test
```
  $ singularity run --env PREFECT_API_URL="http://localhost:4200/api" fdm.sif test.py
```
This overrides the API URL environment variable and ensures it connects to the running instance we created in the previous step rather than starting its own.

You will now be able to access the [prefect dashboard](https://docs.prefect.io/2.11.3/guides/host/)  and see the progress of your flow while it is running.

## Running on a HPC system with PBS
Add the following to your PBS script.
```
mkdir pgdata

mkdir pgrun

singularity instance start -B pgdata:/var/lib/postgresql/data -B pgrun:/var/run/postgresql -e -C --env-file post.envs post.sif  prefect-postgres

singularity run -B $HOME --env HOSTNAME=$PBS_NODEFILE fdm.sif nongputest.py

singularity instance stop --all

rm -rf pgdata 

rm -rf pgrun
```

## Errata
If you have GPU's you wish to include or your code needs them numba and dask-cuda are included in the fdm image and you can enable gpu pass through by including the --nv flag when you launch via "run" or via "instance start"
