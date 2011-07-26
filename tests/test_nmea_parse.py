import unittest
from pynmea.nmea import NMEASentence, GPGLL, GPBOD, GPBWC, GPBWR, GPGGA, GPGSA, GPGSV
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
        p.parse("$GPBWC,220516,5130.02,N,00046.34,W,213.8,T,218.0,M,0004.6,N,EGLM*21")

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
        self.assertEquals("21", p.checksum)

    def test_checksum_passes(self):
        p = GPBWC()
        p.parse("$GPBWC,220516,5130.02,N,00046.34,W,213.8,T,218.0,M,0004.6,N,EGLM*21")

        result = p.check_chksum()
        self.assertTrue(result)


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


class TestGPGGA(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parses_map(self):
        p = GPGGA()
        p.parse("$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47")

        self.assertEquals("GPGGA", p.sen_type)
        self.assertEquals("123519", p.timestamp)
        self.assertEquals("4807.038", p.latitude)
        self.assertEquals("N", p.lat_direction)
        self.assertEquals("01131.000", p.longitude)
        self.assertEquals("E", p.lon_direction)
        self.assertEquals("1", p.gps_qual)
        self.assertEquals("08", p.num_sats)
        self.assertEquals("0.9", p.horizontal_dil)
        self.assertEquals("545.4", p.antenna_altitude)
        self.assertEquals("M", p.altitude_units)
        self.assertEquals("46.9", p.geo_sep)
        self.assertEquals("M", p.geo_sep_units)
        self.assertEquals("", p.age_gps_data)
        self.assertEquals("", p.ref_station_id)
        self.assertEquals("47", p.checksum)


class TestGPGLL(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parses_map1(self):
        p = GPGLL()
        p.parse("$GPGLL,3751.65,S,14507.36,E*77")

        self.assertEquals("GPGLL", p.sen_type)
        self.assertEquals("3751.65", p.lat)
        self.assertEquals("S", p.lat_dir)
        self.assertEquals("14507.36", p.lon)
        self.assertEquals("E", p.lon_dir)
        self.assertEquals("", p.timestamp)
        self.assertEquals("77", p.checksum)

    def test_parses_map2(self):
        p = GPGLL()
        p.parse("$GPGLL,4916.45,N,12311.12,W,225444,A")

        self.assertEquals("GPGLL", p.sen_type)
        self.assertEquals("4916.45", p.lat)
        self.assertEquals("N", p.lat_dir)
        self.assertEquals("12311.12", p.lon)
        self.assertEquals("W", p.lon_dir)
        self.assertEquals("225444", p.timestamp)
        self.assertEquals("A", p.checksum)

    def test_checksum_passes1(self):
        p = GPGLL()
        p.nmea_sentence = "$GPGLL,4916.45,N,12311.12,W,225444,A"
        p.checksum = 'A'
        p._use_data_validity = True

        result = p.check_chksum()
        self.assertTrue(result)

    def test_checksum_fails1(self):
        p = GPGLL()
        p.nmea_sentence = "$GPGLL,4916.45,N,12311.12,W,225444,B"
        p.checksum = 'B'
        p._use_data_validity = True

        result = p.check_chksum()
        self.assertFalse(result)

    def test_checksum_passes2(self):
        p = GPGLL()
        p.nmea_sentence = "$GPGLL,3751.65,S,14507.36,E*77"
        p.checksum = '77'

        result = p.check_chksum()
        self.assertTrue(result)

    def test_checksum_fails2(self):
        p = GPGLL()
        p.nmea_sentence = "$GPGLL,3751.65,S,14507.36,E*78"
        p.checksum = '78'

        result = p.check_chksum()
        self.assertFalse(result)

    def test_gets_properties(self):
        p = GPGLL()
        p.parse("$GPGLL,3751.65,S,14507.36,E*77")

        self.assertEquals(p.latitude, float('3751.65'))
        self.assertEquals(p.longitude, float('14507.36'))
        self.assertEquals(p.lat_direction, 'South')
        self.assertEquals(p.lon_direction, 'East')
        self.assertEquals(p.checksum, "77")

class TestGPGSA(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parses_map(self):
        p = GPGSA()
        p.parse("$GPGSA,A,3,04,05,,09,12,,,24,,,,,2.5,1.3,2.1*39")

        self.assertEquals("GPGSA", p.sen_type)
        self.assertEquals("A", p.mode)
        self.assertEquals("3", p.mode_fix_type)
        self.assertEquals("04", p.sv_id01)
        self.assertEquals("05", p.sv_id02)
        self.assertEquals("", p.sv_id03)
        self.assertEquals("09", p.sv_id04)
        self.assertEquals("12", p.sv_id05)
        self.assertEquals("", p.sv_id06)
        self.assertEquals("", p.sv_id07)
        self.assertEquals("24", p.sv_id08)
        self.assertEquals("", p.sv_id09)
        self.assertEquals("", p.sv_id10)
        self.assertEquals("", p.sv_id11)
        self.assertEquals("", p.sv_id12)
        self.assertEquals("2.5", p.pdop)
        self.assertEquals("1.3", p.hdop)
        self.assertEquals("2.1", p.vdop)
        self.assertEquals("39", p.checksum)

    def test_checsum_passes(self):
        p = GPGSA()
        p.checksum = '39'
        p.nmea_sentence = "$GPGSA,A,3,04,05,,09,12,,,24,,,,,2.5,1.3,2.1*39"

        result = p.check_chksum()

        self.assertTrue(result)

    def test_checsum_fails(self):
        p = GPGSA()
        p.checksum = '38'
        p.nmea_sentence = "$GPGSA,A,3,04,05,,09,12,,,24,,,,,2.5,1.3,2.1*38"

        result = p.check_chksum()

        self.assertFalse(result)


class TestGPGSV(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parses_map(self):
        p = GPGSV()
        p.parse("$GPGSV,3,1,11,03,03,111,00,04,15,270,00,06,01,010,00,13,06,292,00*74")

        self.assertEquals("GPGSV", p.sen_type)
        self.assertEquals('3', p.num_messages)
        self.assertEquals('1', p.msg_num)
        self.assertEquals('11', p.num_sv_in_view)
        self.assertEquals('03', p.sv_prn_num_1)
        self.assertEquals('03', p.elevation_deg_1)
        self.assertEquals('111', p.azimuth_1)
        self.assertEquals('00', p.snr_1)
        self.assertEquals('04', p.sv_prn_num_2)
        self.assertEquals('15', p.elevation_deg_2)
        self.assertEquals('270', p.azimuth_2)
        self.assertEquals('00', p.snr_2)
        self.assertEquals('06', p.sv_prn_num_3)
        self.assertEquals('01', p.elevation_deg_3)
        self.assertEquals('010', p.azimuth_3)
        self.assertEquals('00', p.snr_3)
        self.assertEquals('13', p.sv_prn_num_4)
        self.assertEquals('06', p.elevation_deg_4)
        self.assertEquals('292', p.azimuth_4)
        self.assertEquals('00', p.snr_4)
        self.assertEquals("74", p.checksum)

    def test_checsum_passes(self):
        p = GPGSV()
        p.checksum = '74'
        p.nmea_sentence = "$GPGSV,3,1,11,03,03,111,00,04,15,270,00,06,01,010,00,13,06,292,00*74"

        result = p.check_chksum()

        self.assertTrue(result)

    def test_checsum_fails(self):
        p = GPGSV()
        p.checksum = '73'
        p.nmea_sentence = "$GPGSV,3,1,11,03,03,111,00,04,15,270,00,06,01,010,00,13,06,292,00*74"

        result = p.check_chksum()

        self.assertFalse(result)


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
