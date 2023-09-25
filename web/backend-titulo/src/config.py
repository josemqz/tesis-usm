from flask_env import MetaFlaskEnv
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Configuration(metaclass=MetaFlaskEnv):
    
    DEBUG = True
    ENV = 'development'

    # SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
                            os.path.join(basedir, 'database/campus_occupancy.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False # ahorrar memoria

    # DB_ROOT_PASSWORD="123"
    # DB_NAME="campus_occupancy"
    # DB_USER="jq"
    # DB_PASSWORD="123"
    # DB_HOST="localhost"
    # DB_PORT=3307