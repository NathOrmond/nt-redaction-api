from flask import Flask
from flask import request, jsonify
from flask_cors import CORS, cross_origin
from .redactioncalc import get_distances_from_filepaths
import os, sys,json
import numpy as np
app= Flask(__name__)
# cors = CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/', methods=['GET'])
def home():
  return '''<h1>New Testament Helper API</h1><p>A prototype API for New Testament Studies.</p>'''

# Route to return all available texts that can be compared
@app.route('/texts', methods=['GET'])
def texts():
  # TODO Rather than using local files use a database
  response = {
    'manuscripts': os.listdir('./testmss')
  }
  return jsonify(response)

@app.route('/display', methods=['GET'])
def display():
  #TODO this function returns an internal server error rather than displaying mss 
  # something to do with escape characters and format issues I think...
  mss_name = request.args.get('mss')
  mss_list = os.listdir('./testmss')
  content = ''
  if mss_name in mss_list: 
    filename = './testmss/' + mss_name
    content = get_file_contents(filename)
  else: 
    content ='Manuscript not found'
    response = {
    'contents' : content
    }
  return jsonify(response)

@app.route('/levenshtein', methods=['GET'])
def levenshtein():
  # Get parameters for documents to compare from url 
  mss1_name = request.args.get('mss1')
  mss2_name = request.args.get('mss2')
  response = {}
  
  if (mss1_name is None) or (mss2_name is None):
    response = {'error': 'invalid manuscript names'}
  else:  
    files = {
      mss1_name : concat_filepath(mss1_name),
      mss2_name : concat_filepath(mss2_name)
    }
    values = get_distances_from_filepaths(files)
    print(values)

    row1 = values.to_json()
    
    print(row1)
    print(json.loads(row1))
    
    response = {
     'levenshtein': {
        'mss': [mss1_name, mss2_name],
        'values': json.loads(row1)
      }
    }
  return jsonify(response)

def concat_filepath(filename): 
  return './testmss/' + filename

def get_file_contents(filename): 
  fd = os.open(filename, os.O_RDWR)
  ret = os.read(fd, os.path.getsize(filename))
  rval = ret.decode("utf-8")
  os.close(fd)
  return rval
