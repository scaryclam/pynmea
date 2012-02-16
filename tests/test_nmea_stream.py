import os
from unittest import TestCase

from pynmea.streamer import NMEAStream


class TestStream(TestCase):
    def test_splits_data(self):
        test_data = '$foo,bar,baz*77\n$Meep,wibble,123,321\n'
        streamer = NMEAStream()
        result = streamer._split(test_data)
        self.assertEqual(result, ['foo,bar,baz*77', 'Meep,wibble,123,321'])

    def test_splits_data_2(self):
        test_data = '$foo,bar,baz*77\r$Meep,wibble,123,321\r'
        streamer = NMEAStream()
        result = streamer._split(test_data)
        self.assertEqual(result, ['foo,bar,baz*77', 'Meep,wibble,123,321'])

    def test_splits_data_3(self):
        test_data = '$foo,bar,baz*77\r\n$Meep,wibble,123,321'
        streamer = NMEAStream()
        result = streamer._split(test_data)
        self.assertEqual(result, ['foo,bar,baz*77', 'Meep,wibble,123,321'])

    def test_splits_data_4(self):
        test_data = '$foo,bar,baz*77NOTHING$Meep,wibble,123,321NOTHING'
        streamer = NMEAStream()
        result = streamer._split(test_data, separator='NOTHING')
        self.assertEqual(result, ['foo,bar,baz*77', 'Meep,wibble,123,321'])

    def test_read_data(self):
        test_file = os.path.join(os.path.dirname(__file__), 'test_data',
                                 'gpsdata_feb_11_1-55.txt')
        with open(test_file, 'r') as test_file_fd:
            streamer = NMEAStream(stream_obj=test_file_fd)
            next_data = streamer.read()
            data = []
            while next_data:
                data += next_data
                next_data = streamer.read()

        self.assertEqual(data, [''])
