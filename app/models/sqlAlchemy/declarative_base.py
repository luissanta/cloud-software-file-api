import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://{user}:{pss}@{host}:{port}/{db}'.format(user=os.getenv("PGSQL_USER"),
                                                                             pss=os.getenv("PGSQL_PASSWORD"),
                                                                             host=os.getenv("PGSQL_HOST"),
                                                                             port=os.getenv("PGSQL_PORT"),
                                                                             db=os.getenv("PGSQL_DATABASE")))
Session = sessionmaker(bind=engine)

Base = declarative_base()
