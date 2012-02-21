from pynmea.streamer import NMEAStream

data_file = '../tests/test_data/test_data.gps'

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
