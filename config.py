import os

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
SQLALCHEMY_TRACK_MODIFICATIONS = True

#TOKENS
CASTING_ASSISTANT=os.getenv('CASTING_ASSISTANT')
CASTING_DIRECTOR=os.getenv('CASTING_DIRECTOR')
EXECUTIVE_PRODUCER=os.getenv('EXECUTIVE_PRODUCER')