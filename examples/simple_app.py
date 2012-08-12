import os

from pynmea.streamer import NMEAStream


# Get the data file path
data_file = os.path.join(
    os.path.dirname(__file__), '..', 'tests', 'test_data', 'test_data.gps')


# Open the data file and get the NMEA objects
with open(data_file, 'r') as data_file_fd:
    nmea_stream = NMEAStream(stream_obj=data_file_fd)
    next_data = nmea_stream.get_objects()
    nmea_objects = []
    while next_data:
        nmea_objects += next_data
        next_data = nmea_stream.get_objects()


# All nmea objects are now in variable nmea_objects
for nmea_ob in nmea_objects:
    print nmea_ob.sen_type
