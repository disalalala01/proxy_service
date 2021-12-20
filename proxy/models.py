from . import db, Base, session_db
from sqlalchemy.orm import relationship
from sqlalchemy.exc import IntegrityError, OperationalError
import random
import logging
import requests


class SourceProxy(Base):
    __tablename__ = "source_proxy"
    id = db.Column(db.Integer, primary_key=True, index=True)
    source_id = db.Column(db.Integer, db.ForeignKey("source.id"))
    proxy_id = db.Column(db.Integer, db.ForeignKey("proxy.id"))

    @classmethod
    def remove(cls, id):
        try:
            cls.query.filter(cls.id == id).delete()
        except OperationalError:
            session_db.rollback()
            return cls.remove(id=id)
        except Exception as e:
            print(e)
            session_db.rollback()

    @staticmethod
    def save_proxy(source_id):
        try:
            proxies = Proxy.get_list()
            for proxy in proxies:
                sp = SourceProxy(source_id=source_id, proxy_id=proxy.id)
                sp.save()
        except OperationalError:
            session_db.rollback()
            return SourceProxy.save_proxy(source_id=source_id)
        except Exception as e:
            print(e)

    def save(self):
        try:
            session_db.add(self)
            session_db.commit()
        except OperationalError:
            session_db.rollback()
            return self.save()
        except Exception as e:
            print(e)
            session_db.rollback()

    @classmethod
    def get(cls, source_id: str):
        try:
            q = cls.query.filter(cls.source_id == source_id).all()
            if not q:
                s = session_db.query(Source).filter(Source.id == source_id).first()
                if s:
                    cls.save_proxy(source_id=source_id)
                    q = cls.query.filter(cls.source_id == source_id).all()
                else:
                    raise Exception(f"No Proxies for this source id : {source_id}")
            random_proxy = random.choice(q)
            for i in range(len(q)):
                proxy = {
                    "http://": random_proxy.proxies.ip,
                    "https://": random_proxy.proxies.ip,
                }
                try:
                    r = requests.get(q[0].sources.url, proxies=proxy, timeout=10)
                    if r.status_code == 200:
                        logging.info(f"Get proxy : {random_proxy.proxies.ip}")
                        return proxy
                except Exception as e:
                    logging.exception(e)
                    print(e)
                    cls.remove(id=random_proxy.id)
                    random_proxy = random.choice(q)
            else:
                return {"http": None, "https": None}
        except OperationalError:
            session_db.rollback()
            return cls.get(source_id=source_id)
        except Exception as e:
            print(e)
            session_db.rollback()
            return {"http": None, "https": None}


class Source(Base):
    __tablename__ = "source"
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String, unique=True)
    url = db.Column(db.String)
    source_proxy = relationship("SourceProxy", backref="sources", lazy=True)
    journal = relationship("Journal", backref="journals", lazy=True)

    @classmethod
    def get_list(cls):
        try:
            sources = cls.query.all()
            session_db.commit()
        except OperationalError:
            session_db.rollback()
            return cls.get_list()
        except Exception:
            session_db.rollback()
            raise
        return sources

    def save(self):
        try:
            session_db.add(self)
            session_db.commit()
        except IntegrityError:
            session_db.rollback()
            raise Exception("Exist source")
        except OperationalError:
            session_db.rollback()
            return self.save()
        except Exception:
            session_db.rollback()
            raise


class Proxy(Base):
    __tablename__ = "proxy"
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String, unique=True)
    source_proxy = relationship("SourceProxy", backref="proxies", lazy=True)

    def save(self):
        try:
            session_db.add(self)
            session_db.commit()
        except IntegrityError:
            session_db.rollback()
            raise Exception("Exist proxy")
        except OperationalError:
            session_db.rollback()
            return self.save()
        except Exception:
            session_db.rollback()
            raise

    @classmethod
    def get_list(cls):
        try:
            proxies = cls.query.all()
            session_db.commit()
        except OperationalError:
            session_db.rollback()
            return cls.get_list()
        except Exception:
            session_db.rollback()
            raise
        return proxies


class Journal(Base):
    __tablename__ = "journal"
    id = db.Column(db.BigInteger, primary_key=True)
    created = db.Column(db.TIMESTAMP)
    source_id = db.Column(db.Integer, db.ForeignKey("source.id"))
    status = db.Column(db.String)

    @classmethod
    def get(cls, date: str, source_id):
        try:
            journal = cls.query.filter(
                cls.created == date, cls.source_id == source_id
            ).first()
        except OperationalError:
            session_db.rollback()
            return cls.get(date, source_id)
        except Exception:
            session_db.rollback()
            raise
        return journal

    def save(self):
        try:
            session_db.add(self)
            session_db.commit()
        except IntegrityError:
            session_db.rollback()
            raise Exception("Exist proxy")
        except OperationalError:
            session_db.rollback()
            return self.save()
        except Exception:
            session_db.rollback()
            raise


class MonitoringPrice(Base):
    __tablename__ = "monitoring_price"
    id = db.Column(db.BigInteger, primary_key=True)
    city = db.Column(db.String)
    shop_name = db.Column(db.String, unique=True)
    shop_type = db.Column(db.String)
    shop_category = db.Column(db.String)
    provider = db.Column(db.String)
    product_name = db.Column(db.String)
    product_unit = db.Column(db.String)
    package = db.Column(db.String)
    thermal_state = db.Column(db.String)
    product_price = db.Column(db.Numeric)
    stationary_view = db.Column(db.String)
    composition = db.Column(db.String)
    channel = db.Column(db.String)
    source_id = db.Column(db.Integer)

    @classmethod
    def get(cls, source_id):
        try:
            mp = cls.query.filter(cls.source_id == source_id).first()
            if not mp:
                raise Exception(f"Empty source_id : {source_id}")
            return mp
        except OperationalError:
            session_db.rollback()
            return cls.get(source_id=source_id)
        except Exception:
            session_db.rollback()
            raise

    def save(self):
        try:
            session_db.add(self)
            session_db.commit()
        except IntegrityError:
            session_db.rollback()
            raise Exception("Exist mp")
        except OperationalError:
            session_db.rollback()
            return self.save()
        except Exception:
            session_db.rollback()
            raise
