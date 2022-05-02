# smcompiler-diffie-beepboop
SMCompiler project of CS-523 Advanced Topics on Privacy Enhacing Technologies course at EPFL. Spring 2022 

## Run tests in Python 3.6 environment
```zsh
# build the image in Dockerfile and names it smc-523
docker build -t smc-523 .
# mounts the smcompiler folder in the code_data mountpoint of the container, names it smc-test and runs pytest -s in this one
docker run -v smcompiler:/code_data --name smc-tests smc-523 pytest -s
# onces testing is finished, run this to remove stopped container
docker container prune
```