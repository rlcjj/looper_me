from application.model.ext import Base, session
from sqlalchemy import Column, Integer, String
import tornado.options
from application.global_variable import KEY, AUTH_REQUIRED, ORIGIN_NUMBER


class Config(Base):
    __tablename__ = 'config'

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(128), default=KEY)
    auth_required = Column(Integer, default=AUTH_REQUIRED)
    origin_number = Column(Integer, default=ORIGIN_NUMBER)

    col = {'key': KEY, 'auth_required': AUTH_REQUIRED, 'origin_number': ORIGIN_NUMBER}

    @classmethod
    def load_config(cls):
        res = session.query(cls).first()
        data = {}
        for k, v in cls.col.items():
            data[k] = getattr(res, k) if hasattr(res, k) else v
        return data

    @classmethod
    def update(cls, **kwargs):
        model = session.query(cls).first()
        if model:
            for l in cls.col:
                setattr(model, l, kwargs.get(l))
        session.commit()

    @classmethod
    def system_start(cls):
        data = cls.load_config()
        for l in cls.col:
            setattr(tornado.options.options, l.upper(), bool(data.get(l)) if l == 'auth_required' else data.get(l))
