import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    HYGRAPH_ENDPOINT = os.environ.get('HYGRAPH_ENDPOINT')
    HYGRAPH_PERMANENTAUTH_TOKEN = os.environ.get('HYGRAPH_PERMANENTAUTH_TOKEN')
    smtp_password = os.environ.get('smtp_password')