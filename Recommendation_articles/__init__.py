import logging
from flask import Flask, request, redirect, jsonify
import azure.functions as func
import requests
from .Flask import app

# app = Flask(__name__)

# @app.route('/test', methods=['POST'])
# def hello():
#     req = request.form
#     user_id = req.get('user_id')
#     return user_id

# code from Azure functions 
def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    return func.WsgiMiddleware(app.wsgi_app).handle(req, context)











# @app.route('/test')
# def my_endpoint(request: func.HttpRequest):
#     logging.info('Python HTTP trigger function processed a request.')
#     if request.method == "POST":
#         return func.HttpResponse("Hello!")
    # return 'Hello, World!'





    
# code for Flask Application       




# def main(req: func.HttpRequest) -> func.HttpResponse:
#     logging.info('Python HTTP trigger function processed a request.')
#     name = req.params.get('name')
#     if not name:
#         try:
#             req_body = req.get_json()
#         except ValueError:
#             pass
#         else:
#             name = req_body.get('name')

#     if name:
#         return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
#     else:
#         return func.HttpResponse(
#              "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
#              status_code=200
#         )
