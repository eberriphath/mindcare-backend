from config import app ,db, api
from flask import Flask,jsonify,request,make_response

if __name__ == '__main__':
    app.run(port=5555, debug=True)