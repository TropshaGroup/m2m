import argparse
import json
import os
import requests
import yaml
import shutil
from m2m.app import M2MApp
from m2m.hypothesis import TrivialHypothesis
from m2m.evaluation import TrivialEvaluation
from flask import Flask, jsonify, g, Response
from flasgger import Swagger
app = Flask(__name__)

template = {
  "swagger": "2.0",
  "info": {
    "title": "Drug Repurposing API",
    "description": "Web API for drug repurposing hypothesis evaluation service.",
    "contact": {
      "responsibleOrganization": "renci.org",
      "responsibleDeveloper": "scox@renci.org",
      "email": "scox@renci.org",
      "url": "www.renci.org",
    },
    "termsOfService": "http://renci.org/terms",
    "version": "0.0.1"
  },
  "schemes": [
    "http",
    "https"
  ]
}
app.config['SWAGGER'] = {
   'title': 'M2M Drug Repurposing'
}

swagger = Swagger(app, template=template)

m2m = None
def get_m2m():
    global m2m
    if not m2m:
        m2m = M2MApp ()
    return m2m

@app.route('/test/<substance>/<condition>/')
def evaluate(substance, condition):
   """ Evaluate a drug repurposing hypothesis.
   ---
   parameters:
     - name: substance
       in: path
       type: string
       required: true
       default: imatinib
       x-valueType:
         - http://schema.org/string
       x-requestTemplate:
         - valueType: http://schema.org/string
           template: /evaluate/{{ input }}/{{ input2 }}/
     - name: condition
       in: path
       type: string
       required: true
       default: asthma
       x-valueType:
         - http://schema.org/string
       x-requestTemplate:
         - valueType: http://schema.org/string
           template: /evaluate/{{ input }}/{{ input2 }}
   responses:
     200:
       description: ...
   """
   hypothesis = TrivialHypothesis (substance, condition)
   evaluation = get_m2m().evaluate_hypothesis (hypothesis)
   result = {
       "hypothesis" : hypothesis.__dict__,
       "evaluation" : evaluation.__dict__
   }
   return jsonify (result)

if __name__ == "__main__":
   print ("Starting m2m repurposing server.")
   parser = argparse.ArgumentParser(description='M2M Server')
   parser.add_argument('-p', '--port', type=int, help='Port to run service on.', default=None)
   parser.add_argument('-c', '--conf', help='Config file to use.', default=None)
   args = parser.parse_args ()
   app.run(host='0.0.0.0', port=args.port, debug=True, threaded=True)
