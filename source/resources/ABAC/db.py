#db.py
from sqlalchemy import create_engine


def get_sqlalchemy_engine(db_config):
    connection_string = f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}"
    engine = create_engine(connection_string)
    return engine

