import unittest
from pynmea.nmea import NMEASentence, GPGLL, GPBOD, GPBWC, GPBWR
from pynmea.utils import checksum_calc

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
                          ['GPGLL', '3751.65', 'S', '14507.36', 'E', '77'])

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
                          ['GPGLL', '3751.65', 'S', '14507.36', 'E', '77'])
        self.assertEquals(p.lat, '3751.65')
        self.assertEquals(p.lat_dir, 'S')
        self.assertEquals(p.lon, '14507.36')
        self.assertEquals(p.lon_dir, 'E')
        self.assertEquals(p.checksum, '77')

    def test_checksum_passes(self):
        parse_map = ('Checksum', 'checksum')
        nmea_str = "$GPGLL,3751.65,S,14507.36,E*77"
        p = NMEASentence(parse_map)
        p.checksum = '77'
        p.nmea_sentence = nmea_str
        result = p.check_chksum()

        self.assertTrue(result)

    def test_checksum_fails_wrong_checksum(self):
        parse_map = ('Checksum', 'checksum')
        nmea_str = "$GPGLL,3751.65,S,14507.36,E*78"
        p = NMEASentence(parse_map)
        p.checksum = '78'
        p.nmea_sentence = nmea_str
        result = p.check_chksum()

        self.assertFalse(result)

    def test_checksum_fails_wrong_str(self):
        parse_map = ('Checksum', 'checksum')
        nmea_str = "$GPGLL,3751.65,S,14507.36,W*77"
        p = NMEASentence(parse_map)
        p.checksum = '77'
        p.nmea_sentence = nmea_str
        result = p.check_chksum()

        self.assertFalse(result)

class TestGPGLL(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parses_map(self):
        p = GPGLL()
        p.parse("$GPGLL,3751.65,S,14507.36,E*77")

        self.assertEquals("GPGLL", p.sen_type)
        self.assertEquals(p.parts,
                          ['GPGLL', '3751.65', 'S', '14507.36', 'E', '77'])
        self.assertEquals(p.lat, '3751.65')
        self.assertEquals(p.lat_dir, 'S')
        self.assertEquals(p.lon, '14507.36')
        self.assertEquals(p.lon_dir, 'E')
        self.assertEquals(p.checksum, '77')

    def test_gets_properties(self):
        p = GPGLL()
        p.parse("$GPGLL,3751.65,S,14507.36,E*77")

        self.assertEquals(p.latitude, 3751.65)
        self.assertEquals(p.longitude, 14507.36)
        self.assertEquals(p.lat_direction, 'South')
        self.assertEquals(p.lon_direction, 'East')
        self.assertEquals(p.checksum, "77")


class TestGPBOD(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parses_map(self):
        p = GPBOD()
        p.parse("$GPBOD,045.,T,023.,M,DEST,START")

        self.assertEquals("GPBOD", p.sen_type)
        self.assertEquals(p.parts,
                          ['GPBOD', '045.', 'T', '023.', 'M', 'DEST', 'START'])
        self.assertEquals(p.bearing_t, '045.')
        self.assertEquals(p.bearing_t_type, 'T')
        self.assertEquals(p.bearing_mag, '023.')
        self.assertEquals(p.bearing_mag_type, 'M')
        self.assertEquals(p.dest, 'DEST')
        self.assertEquals(p.start, 'START')

    def test_gets_properties(self):
        p = GPBOD()
        p.parse("$GPBOD,045.,T,023.,M,DEST,START")

        self.assertEquals(p.bearing_true, '045.,T')
        self.assertEquals(p.bearing_magnetic, '023.,M')
        self.assertEquals(p.destination, 'DEST')
        self.assertEquals(p.origin, 'START')


class TestGPBWC(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parses_map(self):
        p = GPBWC()
        p.parse("$GPBWC,220516,5130.02,N,00046.34,W,213.8,T,218.0,M,0004.6,N,EGLM*11")

        self.assertEquals("GPBWC", p.sen_type)
        self.assertEquals("220516", p.timestamp)
        self.assertEquals("5130.02", p.lat_next)
        self.assertEquals("N", p.lat_next_direction)
        self.assertEquals("00046.34", p.lon_next)
        self.assertEquals("W", p.lon_next_direction)
        self.assertEquals("213.8", p.true_track)
        self.assertEquals("T", p.true_track_sym)
        self.assertEquals("218.0", p.mag_track)
        self.assertEquals("M", p.mag_sym)
        self.assertEquals("0004.6", p.range_next)
        self.assertEquals("N", p.range_unit)
        self.assertEquals("EGLM", p.waypoint_name)
        self.assertEquals("11", p.checksum)


class TestGPBWR(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parses_map(self):
        p = GPBWR()
        p.parse("$GPBWR,161102,4217.4920,N,07055.7950,W,296.9,T,311.9,M,47.664,N,0001*3E")
        self.assertEquals("GPBWR", p.sen_type)
        self.assertEquals("161102", p.timestamp)
        self.assertEquals("4217.4920", p.lat_next)
        self.assertEquals("N", p.lat_next_direction)
        self.assertEquals("07055.7950", p.lon_next)
        self.assertEquals("W", p.lon_next_direction)
        self.assertEquals("296.9", p.true_track)
        self.assertEquals("T", p.true_track_sym)
        self.assertEquals("311.9", p.mag_track)
        self.assertEquals("M", p.mag_sym)
        self.assertEquals("47.664", p.range_next)
        self.assertEquals("N", p.range_unit)
        self.assertEquals("0001", p.waypoint_name)
        self.assertEquals("3E", p.checksum)


class TestUtils(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_checksum_calc(self):
        nmea_str1 = 'GPGLL,3751.65,S,14507.36,E'
        nmea_str2 = '$GPGLL,3751.65,S,14507.36,E'
        nmea_str3 = 'GPGLL,3751.65,S,14507.36,E*77'
        nmea_str4 = '$GPGLL,3751.65,S,14507.36,E*77'
        nmea_str5 = '$GPGLL,3751.65,S,14507.36,E*'
        nmea_str6 = 'GPGLL,3751.65,S,14507.36,E*'

        expected_chksum = 77
        result1 = checksum_calc(nmea_str1)
        result2 = checksum_calc(nmea_str2)
        result3 = checksum_calc(nmea_str3)
        result4 = checksum_calc(nmea_str4)
        result5 = checksum_calc(nmea_str5)
        result6 = checksum_calc(nmea_str6)

        self.assertEquals(result1, '0x77')
        self.assertEquals(result2, '0x77')
        self.assertEquals(result3, '0x77')
        self.assertEquals(result4, '0x77')
        self.assertEquals(result5, '0x77')
        self.assertEquals(result6, '0x77')
