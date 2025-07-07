import os

class DevelopmentConfig:
  SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:Cam.110196@localhost/invoice_api"
  SECRET_KEY = os.getenv("SECRET_KEY") or "super secret key"
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  CACHE_TYPE = "SimpleCache"
  DEBUG = True