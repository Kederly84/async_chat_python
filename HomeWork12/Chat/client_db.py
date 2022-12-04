from sqlalchemy import Column, String, Integer, Text, DateTime, create_engine, func
from  sqlalchemy.orm import declarative_base, sessionmaker, Session
from datetime import datetime
from sqlalchemy.dialects.sqlite import insert

Base = declarative_base()

class ClientContacts(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)


class MessageHistory(Base):
    __tablename__ = 'message_history'
    id = Column(Integer, primary_key=True)
    from_user = Column(String(50))
    to_user = Column(String(50))
    message = Column(Text)
    date_time = Column(DateTime(timezone=True), server_default=func.now())

class ClientDB:

    def __init__(self, username):
        self.username = username
        engine = create_engine(f'sqlite:///{username}_db.db3', echo=True, pool_recycle=7200, pool_pre_ping=True)
        Base.metadata.create_all(engine)
        session = sessionmaker(bind=engine)
        self.sess: Session = session()

    def add_contact(self, contact):
        insert_contact = insert(ClientContacts).values({'name': contact}).on_conflict_do_nothing()
        self.sess.execute(insert_contact)
        self.sess.commit()

    def del_contact(self, contact):
        self.sess.query(ClientContacts).filter_by(name=contact).delete()
        self.sess.commit()

    def add_message(self, from_user, to_user, message, date_time = None):
        self.sess.add(MessageHistory(from_user=from_user, to_user=to_user, message=message, date_time=date_time))
        self.sess.commit()