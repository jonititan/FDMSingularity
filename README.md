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