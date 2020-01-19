#!/usr/bin/python3

import sys
from flask import Flask, jsonify

__author__ = 'Gabriel Cantu'

app = Flask(__name__)

#------------------------------------------------------------------------
@app.route('/<path:path>', methods=['GET'])
def extensionNumber(path):
    print ('FINAL WORD: {}'.format(path))
    return jsonify ({'extenso': path})

#------------------------------------------------------------------------
def runFlask():
    print ("Server Online")
    app.run(host='0.0.0.0', port=3000)

#------------------------------------------------------------------------
#-----------------------      MAIN      ---------------------------------
#------------------------------------------------------------------------
if __name__ == '__main__':
    runFlask()

