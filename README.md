# m2m - Man to Molecule to Man

Artificially intelligent drug repurposing over federated knowledge sources.

This is a first checkin to start the conversation about the best structure for this system.

## Structure

The structure below provides a root m2m package with modules for:
* **App** The application can be run from the command line.
* **Hypothesis and Evaluation** Inputs are repurposing hypotheses. Outputs are evaluations of these hypotheses.
* **Knowledge**: This is a source for data which repurposing algorithms evaluate.
* **Algorithm**: A module for aggregating various evaluation methods.
* **Interface**: We might have several interfaces. Interfaces generate repurposing hypotheses.
* **API**: A web based smartAPI for the repurposing functionality. Multiple user interfaces might use this service.
* **Similarity**: A store for a library of similarity metrics.
```

├── README.md
├── api
│   └── service.py
└── m2m
    ├── app.py
    ├── evaluation.py
    ├── hypothesis.py
    ├── knowledge.py
    ├── repurpose
    │   ├── __init__.py
    │   ├── algorithm
    │   │   ├── __init__.py
    │   │   ├── core.py
    │   │   └── literature.py
    │   ├── api
    │   │   └── server.py
    │   └── interface
    │       ├── __init__.py
    │       ├── cli.py
    │       └── core.py
    └── similarity
        └── pmc.py
```

## To Run

### Setup
Install Python 3.6.x
Clone the repo.
Install requirements from the requirements.txt file.

### The application
This will create trivial interfaces and algorithms, wire them together, and output an evaluation.
```
[scox@mac~/dev/m2m]$ PYTHONPATH=$PWD python m2m/app.py
```
### The Similarity API

```
[~/dev/m2m]$ PYTHONPATH=$PWD python m2m/api/service.py
```

The service will be available at http://localhost:5000/apidocs.

### The API
This will start a web API.
```
[~/dev/m2m]$ PYTHONPATH=$PWD python m2m/repurpose/api/server.py
```

At [http://localhost:5000/apidocs](http://localhost:5000/apidocs), you should get this:

![image](https://github.com/TropshaGroup/m2m/blob/master/img/smartapi.png)
