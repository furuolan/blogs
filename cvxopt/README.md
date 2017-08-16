# CVXOPT example

## Blog post

[https://medium.com/@adamnovo/linear-programming-in-python-cvxopt-and-game-theory-8626a143d428](https://medium.com/@adamnovo/linear-programming-in-python-cvxopt-and-game-theory-8626a143d428)

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
