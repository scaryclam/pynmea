import unittest
from nmea import NMEASentence, GPGLL

class TestNMEAParse(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_basic_parse(self):
        parse_map = (("Latitude", "lat"),
                     ("Direction", "lat_dir"),
                     ("Longitude", "lon"),
                     ("Direction", "lon_dir"),
                     ("Checksum", "checksum"))

        p = NMEASentence(parse_map)
        p._parse("$GPGLL,3751.65,S,14507.36,E*77")

        self.assertEquals("GPGLL", p.sen_type)
        self.assertEquals(p.parts,
                          ['GPGLL', '3751.65', 'S', '14507.36', 'E', '*77'])

    def test_parse(self):
        parse_map = (("Latitude", "lat"),
                     ("Direction", "lat_dir"),
                     ("Longitude", "lon"),
                     ("Direction", "lon_dir"),
                     ("Checksum", "checksum"))

        p = NMEASentence(parse_map)
        p.parse("$GPGLL,3751.65,S,14507.36,E*77")

        self.assertEquals("GPGLL", p.sen_type)
        self.assertEquals(p.parts,
                          ['GPGLL', '3751.65', 'S', '14507.36', 'E', '*77'])
        self.assertEquals(p.lat, '3751.65')
        self.assertEquals(p.lat_dir, 'S')
        self.assertEquals(p.lon, '14507.36')
        self.assertEquals(p.lon_dir, 'E')
        self.assertEquals(p.checksum, '*77')


class TestGPGLL(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parses_map(self):
        parse_map = (("Latitude", "lat"),
                     ("Direction", "lat_dir"),
                     ("Longitude", "lon"),
                     ("Direction", "lon_dir"),
                     ("Checksum", "checksum"))

        p = GPGLL()
        p.parse("$GPGLL,3751.65,S,14507.36,E*77")

        self.assertEquals("GPGLL", p.sen_type)
        self.assertEquals(p.parts,
                          ['GPGLL', '3751.65', 'S', '14507.36', 'E', '*77'])
        self.assertEquals(p.lat, '3751.65')
        self.assertEquals(p.lat_dir, 'S')
        self.assertEquals(p.lon, '14507.36')
        self.assertEquals(p.lon_dir, 'E')
        self.assertEquals(p.checksum, '*77')

    def test_gets_properties(self):
        parse_map = (("Latitude", "lat"),
                     ("Direction", "lat_dir"),
                     ("Longitude", "lon"),
                     ("Direction", "lon_dir"),
                     ("Checksum", "checksum"))

        p = GPGLL()
        p.parse("$GPGLL,3751.65,S,14507.36,E*77")

        self.assertEquals(p.latitude, 3751.65)
        self.assertEquals(p.longitude, 14507.36)
        self.assertEquals(p.lat_direction, 'South')
        self.assertEquals(p.lon_direction, 'East')
        self.assertEquals(p.checksum, "*77")
