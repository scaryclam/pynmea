import os
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from pynmea.streamer import NMEAStream


data_file = os.path.join(
    os.path.dirname(__file__), '..', 'tests', 'test_data', 'test_data.gps')


with open(data_file, 'r') as data_file_fd:
    nmea_stream = NMEAStream(stream_obj=data_file_fd)
    next_data = nmea_stream.get_objects()
    nmea_objects = []
    while next_data:
        nmea_objects += next_data
        next_data = nmea_stream.get_objects()


# SIMPLE SQLALCHEMY SETUP
engine = create_engine('sqlite:///example.db')
Base = declarative_base()


class NMEATable(Base):
    __tablename__ = 'nmea'

    # Column definitions
    id = Column(Integer, primary_key=True)
    sen_type = Column(String)

    # Other column definitions go here ...

    def __init__(self, sen_type):
        self.sen_type = sen_type


# create tables
Base.metadata.create_all(engine)

# Make session
Session = sessionmaker(bind=engine)
session = Session()

# END SQLALCHEMY SETUP


# Populate database
# All nmea objects are now in variable nmea_objects
for nmea_ob in nmea_objects:
    new_db_entry = NMEATable(nmea_ob.sen_type)
    session.add(new_db_entry)
    session.commit()
