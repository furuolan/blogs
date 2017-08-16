# CVXOPT example

## Blog post: medium.com/@adamnovo/linear-programming-in-python-cvxopt-and-game-theory

## Instructions to run code in Docker:
  - Get docker image

        docker-compose up

  - SSH into docker container

        docker exec -it cvxopt_container /bin/bash

  - Install dependencies

        cd mnt/app
        bash requirements.sh

  - Run example problems
  
        python cvxopt.py
