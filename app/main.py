from flask import Flask
from flask import request, jsonify
from .redactioncalc import get_distances_from_filepaths
import os, sys
app= Flask(__name__)

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
  # mss1_name = request.args.get('mss1')
  # mss2_name = request.args.get('mss2')
  # TODO populate response with parameters from levenshtein comparison algorithm
  response = { 'TEST': 'TEST' }
  # = {
  #   'levenshtein': {
  #     'mss': [mss1_name, mss2_name],
  #     'values': {
  #       'x': { 
  #         'label': mss1_name,
  #         'values': [1,2,3]
  #       },
  #       'y': {
  #         'label': mss2_name,
  #         'values': [1,2,3]
  #       }
  #    }
  #   }
  # }
  return jsonify(response)

def get_file_contents(filename): 
  fd = os.open(filename, os.O_RDWR)
  ret = os.read(fd, os.path.getsize(filename))
  rval = ret.decode("utf-8")
  os.close(fd)
  return rval
