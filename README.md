# smcompiler-diffie-beepboop
SMCompiler project of CS-523 Advanced Topics on Privacy Enhacing Technologies course at EPFL. Spring 2022 

## Run tests in Python 3.6 environment
```zsh
# build the image and mounts the code folder inside
docker compose build
# runs the tests in the docker image
docker compose up
# onces testing is finished, run this to remove stopped container
docker compose down
```