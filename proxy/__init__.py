import os
import sys

sys.path.append(os.getcwd())

import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from proxy.config import Config
from flask import Flask

app = Flask(__name__)

engine = create_engine(
    f"postgresql://{Config.USER}:{Config.PASS}@{Config.HOST}:{int(Config.PORT)}/{Config.NAME}"
)
session_db = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
Base = declarative_base()
Base.query = session_db.query_property()


@app.teardown_appcontext
def shutdown_session(exception=None):
    session_db.remove()


from proxy.proxy_services.proxy_view import proxies
from proxy.source_services.source_view import sources
from proxy.journal_services.journal_view import journal
from proxy.monitoring_service.mp_view import mp

app.register_blueprint(proxies)
app.register_blueprint(journal)
app.register_blueprint(sources)
app.register_blueprint(mp)
