# Overview

An API has been developed in order to calculate the optimal power output which should be produced by a set of power producers in order to reach a given load while minimizing costs, taking into account the cost of the fuel, the price linked to CO2 emissions and the efficiency of the different power plants available.

This exercice is based on the instructions given in https://github.com/gem-spaas/powerplant-coding-challenge.

# How to use the API?

## Requirements

* Docker

## Start/build the app

In a terminal, go to root project path and run:
```
docker-compose up --build -d
docker-compose down
```
The Swagger UI can now be accessed at http://localhost:8888/docs.

## Run the tests

In a terminal, go to root project path and run:
```
docker exec -it engie_app_1 python -m pytest tests/main.py
```

Cédric Prieels (June 2024)

