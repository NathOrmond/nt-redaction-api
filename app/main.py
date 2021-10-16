from flask import Flask
from flask import request, jsonify
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
      # TODO Read document and populate response with its contents
      filename = './testmss/' + mss_name
      fd = os.open(filename, os.O_RDWR)
      ret = os.read(fd, 12)
      print(ret)
      content = filename
      os.close(fd)
    else: 
      content ='Manuscript not found'
    response = {
      'contents' : content
    }
    return jsonify(response)

@app.route('/levenshtein', methods=['GET'])
def levenshtein():
  # TODO get parameters for documents to compare from url 
  # TODO populate response with parameters from levenshtein comparison algorithm
    response = {
        'levenshtein': {
            'mss': ['mss1', 'mss2'],
            'values': {
                'x': { 
                    'label': 'mss1',
                    'values': [1,2,3]
                },
                'y': {
                    'label': 'mss2',
                    'values': [1,2,3]
                }
            }
        }
    }
    return jsonify(response)
