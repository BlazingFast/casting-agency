import os
from dotenv import load_dotenv

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

#TOKENS & DB
load_dotenv()
CASTING_ASSISTANT=os.getenv('CASTING_ASSISTANT')
CASTING_DIRECTOR=os.getenv('CASTING_DIRECTOR')
EXECUTIVE_PRODUCER=os.getenv('EXECUTIVE_PRODUCER')
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
SQLALCHEMY_TRACK_MODIFICATIONS = True