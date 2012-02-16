import unittest
from pynmea.nmea import (NMEASentence, GPAAM, GPALM, GPAPA, GPAPB, GPBEC, GPBOD,
                         GPBWC, GPBWR, GPBWW, GPGGA, GPGLL, GPGSA, GPGSV, GPHDG,
                         GPHDT, GPZDA, GPSTN, GPRMA, GPRMB, GPRMC, GPRTE, GPR00,
                         GPTRF, GPVBW, GPVTG, GPWCV, GPWNC, GPWPL, GPXTE,
                         PGRME, PGRMZ, PGRMM)

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
                     ("Direction", "lon_dir"))

        p = NMEASentence(parse_map)
        p._parse("$GPGLL,3751.65,S,14507.36,E*77")

        self.assertEquals("GPGLL", p.sen_type)
        self.assertEquals(p.parts,
                          ['GPGLL', '3751.65', 'S', '14507.36', 'E'])

    def test_parse(self):
        parse_map = (("Latitude", "lat"),
                     ("Direction", "lat_dir"),
                     ("Longitude", "lon"),
                     ("Direction", "lon_dir"))

        p = NMEASentence(parse_map)
        p.parse("$GPGLL,3751.65,S,14507.36,E*77")

        self.assertEquals("GPGLL", p.sen_type)
        self.assertEquals(p.parts,
                          ['GPGLL', '3751.65', 'S', '14507.36', 'E'])
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


class TestGPAAM(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parses_map(self):
        p = GPAAM()
        p.parse("$GPAAM,A,A,0.10,N,WPTNME*32")

        self.assertEquals("GPAAM", p.sen_type)
        self.assertEquals("A", p.arrival_circ_entered)
        self.assertEquals("A", p.perp_passed)
        self.assertEquals("0.10", p.circle_rad)
        self.assertEquals("N", p.circle_rad_unit)
        self.assertEquals("WPTNME", p.waypoint_id)
        self.assertEquals("32", p.checksum)


class TestGPALM(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parses_map(self):
        p = GPALM()
        p.parse("$GPALM,32,1,01,5,00,264A,4E,0A5E,FD3F,A11257,B8E036,536C67,2532C1,069,000*7B")

        self.assertEquals("GPALM", p.sen_type)
        self.assertEquals("32", p.total_num_msgs)
        self.assertEquals("1", p.msg_num)
        self.assertEquals("01", p.sat_prn_num)
        self.assertEquals("5", p.gps_week_num)
        self.assertEquals("00", p.sv_health)
        self.assertEquals("264A", p.eccentricity)
        self.assertEquals("4E", p.alamanac_ref_time)
        self.assertEquals("0A5E", p.inc_angle)
        self.assertEquals("FD3F", p.rate_right_asc)
        self.assertEquals("A11257", p.root_semi_major_axis)
        self.assertEquals("B8E036", p.arg_perigee)
        self.assertEquals("536C67", p.lat_asc_node)
        self.assertEquals("2532C1", p.mean_anom)
        self.assertEquals("069", p.f0_clock_param)
        self.assertEquals("000", p.f1_clock_param)
        self.assertEquals("7B", p.checksum)


class TestGPAPA(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parses_map(self):
        p = GPAPA()
        p.parse("$GPAPA,A,A,0.10,R,N,V,V,011,M,DEST*82")

        self.assertEquals("GPAPA", p.sen_type)
        self.assertEquals("A", p.status_gen)
        self.assertEquals("A", p.status_cycle_lock)
        self.assertEquals("0.10", p.cross_track_err_mag)
        self.assertEquals("R", p.dir_steer)
        self.assertEquals("N", p.cross_track_unit)
        self.assertEquals("V", p.arr_circle_entered)
        self.assertEquals("V", p.perp_passed)
        self.assertEquals("011", p.bearing_to_dest)
        self.assertEquals("M", p.bearing_type)
        self.assertEquals("DEST", p.dest_waypoint_id)
        self.assertEquals("82", p.checksum)


class TestGPAPB(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parses_map(self):
        p = GPAPB()
        p.parse("$GPAPB,A,A,0.10,R,N,V,V,011,M,DEST,011,M,011,M*82")

        self.assertEquals("GPAPB", p.sen_type)
        self.assertEquals("A", p.status_gen)
        self.assertEquals("A", p.status_cycle_lock)
        self.assertEquals("0.10", p.cross_track_err_mag)
        self.assertEquals("R", p.dir_steer)
        self.assertEquals("N", p.cross_track_unit)
        self.assertEquals("V", p.arr_circle_entered)
        self.assertEquals("V", p.perp_passed)
        self.assertEquals("011", p.bearing_to_dest)
        self.assertEquals("M", p.bearing_type)
        self.assertEquals("DEST", p.dest_waypoint_id)
        self.assertEquals("011", p.bearing_pres_dest)
        self.assertEquals("M", p.bearing_pres_dest_type)
        self.assertEquals("011", p.heading_to_dest)
        self.assertEquals("M", p.heading_to_dest_type)
        self.assertEquals("82", p.checksum)


class TestGPBEC(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parses_map_1(self):
        """ No FAA mode indicator
        """
        p = GPBEC()
        p.parse("$GPBEC,081837,,,,,,T,,M,,N,*13")

        self.assertEquals("GPBEC", p.sen_type)
        self.assertEquals("081837", p.timestamp)
        self.assertEquals("", p.waypoint_lat)
        self.assertEquals("", p.waypoint_lat_dir)
        self.assertEquals("", p.waypoint_lon)
        self.assertEquals("", p.waypoint_lon_dir)
        self.assertEquals("", p.bearing_true)
        self.assertEquals("T", p.bearing_true_sym)
        self.assertEquals("", p.bearing_mag)
        self.assertEquals("M", p.bearing_mag_sym)
        self.assertEquals("", p.nautical_miles)
        self.assertEquals("N", p.nautical_miles_sym)
        self.assertEquals("", p.waypoint_id)
        self.assertEquals("13", p.checksum)

    def test_parses_map_2(self):
        """ No FAA mode indicator
        """
        p = GPBEC()
        p.parse("GPBEC,220516,5130.02,N,00046.34,W,213.8,T,218.0,M,0004.6,N,EGLM*11")

        self.assertEquals("GPBEC", p.sen_type)
        self.assertEquals("220516", p.timestamp)
        self.assertEquals("5130.02", p.waypoint_lat)
        self.assertEquals("N", p.waypoint_lat_dir)
        self.assertEquals("00046.34", p.waypoint_lon)
        self.assertEquals("W", p.waypoint_lon_dir)
        self.assertEquals("213.8", p.bearing_true)
        self.assertEquals("T", p.bearing_true_sym)
        self.assertEquals("218.0", p.bearing_mag)
        self.assertEquals("M", p.bearing_mag_sym)
        self.assertEquals("0004.6", p.nautical_miles)
        self.assertEquals("N", p.nautical_miles_sym)
        self.assertEquals("EGLM", p.waypoint_id)
        self.assertEquals("11", p.checksum)

    def test_parses_map_3(self):
        """ WITH FAA mode indicator
        """
        p = GPBEC()
        p.parse("GPBEC,220516,5130.02,N,00046.34,W,213.8,T,218.0,M,0004.6,N,EGLM,X*11")

        self.assertEquals("GPBEC", p.sen_type)
        self.assertEquals("220516", p.timestamp)
        self.assertEquals("5130.02", p.waypoint_lat)
        self.assertEquals("N", p.waypoint_lat_dir)
        self.assertEquals("00046.34", p.waypoint_lon)
        self.assertEquals("W", p.waypoint_lon_dir)
        self.assertEquals("213.8", p.bearing_true)
        self.assertEquals("T", p.bearing_true_sym)
        self.assertEquals("218.0", p.bearing_mag)
        self.assertEquals("M", p.bearing_mag_sym)
        self.assertEquals("0004.6", p.nautical_miles)
        self.assertEquals("N", p.nautical_miles_sym)
        self.assertEquals("EGLM", p.waypoint_id)
        self.assertEquals("X", p.faa_mode)
        self.assertEquals("11", p.checksum)


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


class TestGPBWW(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parses_map(self):
        p = GPBWW()
        p.parse("$GPBWW,x.x,T,x.x,M,c--c,c--c*ff")

        self.assertEquals("GPBWW", p.sen_type)
        self.assertEquals("x.x", p.bearing_deg_true)
        self.assertEquals("T", p.bearing_deg_true_sym)
        self.assertEquals("x.x", p.bearing_deg_mag)
        self.assertEquals("M", p.bearing_deg_mag_sym)
        self.assertEquals("c--c", p.waypoint_id_dest)
        self.assertEquals("c--c", p.waypoint_id_orig)
        self.assertEquals("ff", p.checksum)


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
        #self.assertEquals("", p.timestamp) # No timestamp given
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
        self.assertEquals("A", p.data_valid)

    #def test_checksum_passes1(self):
        #p = GPGLL()
        #p.nmea_sentence = "$GPGLL,4916.45,N,12311.12,W,225444,A"
        #p.data_validity = 'A'
        ##p._use_data_validity = True

        #result = p.check_chksum()
        #self.assertTrue(result)

    #def test_checksum_fails1(self):
        #p = GPGLL()
        #p.nmea_sentence = "$GPGLL,4916.45,N,12311.12,W,225444,B"
        #p.checksum = 'B'
        #p._use_data_validity = True

        #result = p.check_chksum()
        #self.assertFalse(result)

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

    def test_checksum_passes(self):
        p = GPGSA()
        p.checksum = '39'
        p.nmea_sentence = "$GPGSA,A,3,04,05,,09,12,,,24,,,,,2.5,1.3,2.1*39"

        result = p.check_chksum()

        self.assertTrue(result)

    def test_checksum_fails(self):
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

    def test_checksum_passes(self):
        p = GPGSV()
        p.checksum = '74'
        p.nmea_sentence = "$GPGSV,3,1,11,03,03,111,00,04,15,270,00,06,01,010,00,13,06,292,00*74"

        result = p.check_chksum()

        self.assertTrue(result)

    def test_checksum_fails(self):
        p = GPGSV()
        p.checksum = '73'
        p.nmea_sentence = "$GPGSV,3,1,11,03,03,111,00,04,15,270,00,06,01,010,00,13,06,292,00*74"

        result = p.check_chksum()

        self.assertFalse(result)


class TestGPHDG(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parses_map(self):
        p = GPHDG()
        p.parse("$GPHDG,190.7,,E,0.0,E*7F")

        self.assertEquals("GPHDG", p.sen_type)
        self.assertEquals("190.7", p.heading)
        self.assertEquals("", p.deviation)
        self.assertEquals("E", p.dev_dir)
        self.assertEquals("0.0", p.variation)
        self.assertEquals("E", p.var_dir)
        self.assertEquals("7F", p.checksum)

    def test_checksum_passes(self):
        p = GPHDG()
        p.checksum = '7F'
        p.nmea_sentence = "$GPHDG,190.7,,E,0.0,E*7F"

        result = p.check_chksum()

        self.assertTrue(result)

    def test_checksum_fails(self):
        p = GPHDG()
        p.checksum = '7E'
        p.nmea_sentence = "$GPHDG,190.7,,E,0.0,E*7E"

        result = p.check_chksum()

        self.assertFalse(result)


class TestGPHDT(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parses_map(self):
        p = GPHDT()
        p.parse("$GPHDT,227.66,T*02")

        self.assertEquals("GPHDT", p.sen_type)
        self.assertEquals("227.66", p.heading)
        self.assertEquals("T", p.hdg_true)
        self.assertEquals("02", p.checksum)

    def test_checksum_passes(self):
        p = GPHDT()
        p.checksum = '02'
        p.nmea_sentence = '$GPHDT,227.66,T*02'

        result = p.check_chksum()

        self.assertTrue(result)

    def test_checksum_fails(self):
        p = GPHDT()
        p.checksum = '03'
        p.nmea_sentence = '$GPHDT,227.66,T*03'

        result = p.check_chksum()

        self.assertFalse(result)


class TestGPR00(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parses_map_1(self):
        p = GPR00()
        p.parse("$GPR00,EGLL,EGLM,EGTB,EGUB,EGTK,MBOT,EGTB,,,,,,,*58")

        self.assertEquals("GPR00", p.sen_type)
        self.assertEquals(['EGLL', 'EGLM', 'EGTB', 'EGUB', 'EGTK', 'MBOT',
                           'EGTB', '', '', '', '', '', '', ''],
                          p.waypoint_list)
        self.assertEquals("58", p.checksum)

    def test_parses_map_2(self):
        p = GPR00()
        p.parse("$GPR00,MINST,CHATN,CHAT1,CHATW,CHATM,CHATE,003,004,005,006,007,,,*05")

        self.assertEquals("GPR00", p.sen_type)
        self.assertEquals(['MINST', 'CHATN', 'CHAT1', 'CHATW', 'CHATM', 'CHATE',
                           '003', '004', '005', '006', '007', '', '', ''],
                          p.waypoint_list)
        self.assertEquals("05", p.checksum)

    def test_checksum_passes(self):
        p = GPR00()
        p.checksum = '58'
        p.nmea_sentence = "$GPR00,EGLL,EGLM,EGTB,EGUB,EGTK,MBOT,EGTB,,,,,,,*58"

        result = p.check_chksum()

        self.assertTrue(result)

    def test_checksum_fails(self):
        p = GPR00()
        p.checksum = '57'
        p.nmea_sentence = "$GPR00,EGLL,EGLM,EGTB,EGUB,EGTK,MBOT,EGTB,,,,,,,*57"

        result = p.check_chksum()

        self.assertFalse(result)


class TestGPRMA(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parses_map(self):
        p = GPRMA()
        p.parse("$GPRMA,A,4630.129,N,147.372,W,,,12.2,5,7,N*51")

        self.assertEquals("GPRMA", p.sen_type)
        self.assertEquals("A", p.data_status)
        self.assertEquals("4630.129", p.lat)
        self.assertEquals("N", p.lat_dir)
        self.assertEquals("147.372", p.lon)
        self.assertEquals("W", p.lon_dir)
        self.assertEquals("", p.not_used_1)
        self.assertEquals("", p.not_used_2)
        self.assertEquals("12.2", p.spd_over_grnd)
        self.assertEquals("5", p.crse_over_grnd)
        self.assertEquals("7", p.variation)
        self.assertEquals("N", p.var_dir)
        self.assertEquals("51", p.checksum)

    def test_checksum_passes(self):
        p = GPRMA()
        p.checksum = '51'
        p.nmea_sentence = '$GPRMA,A,4630.129,N,147.372,W,,,12.2,5,7,N*51'
        result = p.check_chksum()
        self.assertTrue(result)

    def test_checksum_fails(self):
        p = GPRMA()
        p.checksum = '52'
        p.nmea_sentence = '$GPRMA,A,4630.129,N,147.372,W,,,12.2,5,7,N*52'
        result = p.check_chksum()
        self.assertFalse(result)


class TestGPRMB(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parses_map_1(self):
        p = GPRMB()
        p.parse("$GPRMB,A,0.66,L,003,004,4917.24,N,12309.57,W,001.3,052.5,000.5,V*20")

        self.assertEquals("GPRMB", p.sen_type)
        self.assertEquals("A", p.validity)
        self.assertEquals("0.66", p.cross_track_error)
        self.assertEquals("L", p.cte_correction_dir)
        self.assertEquals("003", p.origin_waypoint_id)
        self.assertEquals("004", p.dest_waypoint_id)
        self.assertEquals("4917.24", p.dest_lat)
        self.assertEquals("N", p.dest_lat_dir)
        self.assertEquals("12309.57", p.dest_lon)
        self.assertEquals("W", p.dest_lon_dir)
        self.assertEquals("001.3", p.dest_range)
        self.assertEquals("052.5", p.dest_true_bearing)
        self.assertEquals("000.5", p.dest_velocity)
        self.assertEquals("V", p.arrival_alarm)
        self.assertEquals("20", p.checksum)

    def test_parses_map_2(self):
        p = GPRMB()
        p.parse("$GPRMB,A,4.08,L,EGLL,EGLM,5130.02,N,00046.34,W,004.6,213.9,122.9,A*3D")

        self.assertEquals("GPRMB", p.sen_type)
        self.assertEquals("A", p.validity)
        self.assertEquals("4.08", p.cross_track_error)
        self.assertEquals("L", p.cte_correction_dir)
        self.assertEquals("EGLL", p.origin_waypoint_id)
        self.assertEquals("EGLM", p.dest_waypoint_id)
        self.assertEquals("5130.02", p.dest_lat)
        self.assertEquals("N", p.dest_lat_dir)
        self.assertEquals("00046.34", p.dest_lon)
        self.assertEquals("W", p.dest_lon_dir)
        self.assertEquals("004.6", p.dest_range)
        self.assertEquals("213.9", p.dest_true_bearing)
        self.assertEquals("122.9", p.dest_velocity)
        self.assertEquals("A", p.arrival_alarm)
        self.assertEquals("3D", p.checksum)

    def test_parses_map_3(self):
        p = GPRMB()
        p.parse("$GPRMB,A,x.x,a,c--c,d--d,llll.ll,e,yyyyy.yy,f,g.g,h.h,i.i,j*kk")

        self.assertEquals("GPRMB", p.sen_type)
        self.assertEquals("A", p.validity)
        self.assertEquals("x.x", p.cross_track_error)
        self.assertEquals("a", p.cte_correction_dir)
        self.assertEquals("c--c", p.origin_waypoint_id)
        self.assertEquals("d--d", p.dest_waypoint_id)
        self.assertEquals("llll.ll", p.dest_lat)
        self.assertEquals("e", p.dest_lat_dir)
        self.assertEquals("yyyyy.yy", p.dest_lon)
        self.assertEquals("f", p.dest_lon_dir)
        self.assertEquals("g.g", p.dest_range)
        self.assertEquals("h.h", p.dest_true_bearing)
        self.assertEquals("i.i", p.dest_velocity)

        # This should include the bogus checksum as the checksum is not a valid
        # hex pair and should not be stripped off
        self.assertEquals("j*kk", p.arrival_alarm)

        # There should be no checksum as it was not a valid hex pair
        self.assertFalse(hasattr(p, 'checksum'))

    def test_checksum_passes(self):
        p = GPRMB()
        p.checksum = '20'
        p.nmea_sentence = '$GPRMB,A,0.66,L,003,004,4917.24,N,12309.57,W,001.3,052.5,000.5,V*20'
        result = p.check_chksum()
        self.assertTrue(result)

    def test_checksum_fails(self):
        p = GPRMB()
        p.checksum = '21'
        p.nmea_sentence = '$GPRMB,A,0.66,L,003,004,4917.24,N,12309.57,W,001.3,052.5,000.5,V*21'
        result = p.check_chksum()
        self.assertFalse(result)


class TestGPRMC(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parses_map_1(self):
        p = GPRMC()
        p.parse("$GPRMC,081836,A,3751.65,S,14507.36,E,000.0,360.0,130998,011.3,E*62")

        self.assertEquals("GPRMC", p.sen_type)
        self.assertEquals("081836", p.timestamp)
        self.assertEquals("A", p.data_validity)
        self.assertEquals("3751.65", p.lat)
        self.assertEquals("S", p.lat_dir)
        self.assertEquals("14507.36", p.lon)
        self.assertEquals("E", p.lon_dir)
        self.assertEquals("000.0", p.spd_over_grnd)
        self.assertEquals("360.0", p.true_course)
        self.assertEquals("130998", p.datestamp)
        self.assertEquals("011.3", p.mag_variation)
        self.assertEquals("E", p.mag_var_dir)
        self.assertEquals("62", p.checksum)

    def test_parses_map_2(self):
        p = GPRMC()
        p.parse("$GPRMC,225446,A,4916.45,N,12311.12,W,000.5,054.7,191194,020.3,E*68")

        self.assertEquals("GPRMC", p.sen_type)
        self.assertEquals("225446", p.timestamp)
        self.assertEquals("A", p.data_validity)
        self.assertEquals("4916.45", p.lat)
        self.assertEquals("N", p.lat_dir)
        self.assertEquals("12311.12", p.lon)
        self.assertEquals("W", p.lon_dir)
        self.assertEquals("000.5", p.spd_over_grnd)
        self.assertEquals("054.7", p.true_course)
        self.assertEquals("191194", p.datestamp)
        self.assertEquals("020.3", p.mag_variation)
        self.assertEquals("E", p.mag_var_dir)
        self.assertEquals("68", p.checksum)

    def test_parses_map_3(self):
        p = GPRMC()
        p.parse("$GPRMC,220516,A,5133.82,N,00042.24,W,173.8,231.8,130694,004.2,W*70")

        self.assertEquals("GPRMC", p.sen_type)
        self.assertEquals("220516", p.timestamp)
        self.assertEquals("A", p.data_validity)
        self.assertEquals("5133.82", p.lat)
        self.assertEquals("N", p.lat_dir)
        self.assertEquals("00042.24", p.lon)
        self.assertEquals("W", p.lon_dir)
        self.assertEquals("173.8", p.spd_over_grnd)
        self.assertEquals("231.8", p.true_course)
        self.assertEquals("130694", p.datestamp)
        self.assertEquals("004.2", p.mag_variation)
        self.assertEquals("W", p.mag_var_dir)
        self.assertEquals("70", p.checksum)

    def test_checksum_passes(self):
        p = GPRMC()
        p.checksum = '70'
        p.nmea_sentence = '$GPRMC,220516,A,5133.82,N,00042.24,W,173.8,231.8,130694,004.2,W*70'
        result = p.check_chksum()
        self.assertTrue(result)

    def test_checksum_fails(self):
        p = GPRMC()
        p.checksum = '71'
        p.nmea_sentence = '$GPRMC,220516,A,5133.82,N,00042.24,W,173.8,231.8,130694,004.2,W*71'
        result = p.check_chksum()
        self.assertFalse(result)


class TestGPRTE(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parses_map1(self):
        p = GPRTE()
        p.parse("$GPRTE,2,1,c,0,PBRCPK,PBRTO,PTELGR,PPLAND,PYAMBU,PPFAIR,PWARRN,PMORTL,PLISMR*73")

        self.assertEquals("GPRTE", p.sen_type)
        self.assertEquals("2", p.num_in_seq)
        self.assertEquals("1", p.sen_num)
        self.assertEquals("c", p.start_type)
        self.assertEquals("0", p.active_route_id)
        self.assertEquals(["PBRCPK", "PBRTO", "PTELGR", "PPLAND", "PYAMBU",
                           "PPFAIR", "PWARRN", "PMORTL", "PLISMR"],
                          p.waypoint_list)
        self.assertEquals("73", p.checksum)

    def test_parses_map2(self):
        p = GPRTE()
        p.parse("$GPRTE,2,2,c,0,PCRESY,GRYRIE,GCORIO,GWERR,GWESTG,7FED*34")
        self.assertEquals("GPRTE", p.sen_type)
        self.assertEquals("2", p.num_in_seq)
        self.assertEquals("2", p.sen_num)
        self.assertEquals("c", p.start_type)
        self.assertEquals("0", p.active_route_id)
        self.assertEquals(
            ["PCRESY", "GRYRIE", "GCORIO", "GWERR", "GWESTG", "7FED"],
            p.waypoint_list)
        self.assertEquals("34", p.checksum)

    def test_checksum_passes(self):
        p = GPRTE()
        p.checksum = "73"
        p.nmea_sentence = "$GPRTE,2,1,c,0,PBRCPK,PBRTO,PTELGR,PPLAND,PYAMBU,PPFAIR,PWARRN,PMORTL,PLISMR*73"

        result = p.check_chksum()
        self.assertTrue(result)

    def test_checksum_fails(self):
        p = GPRTE()
        p.checksum = "74"
        p.nmea_sentence = "$GPRTE,2,1,c,0,PBRCPK,PBRTO,PTELGR,PPLAND,PYAMBU,PPFAIR,PWARRN,PMORTL,PLISMR*74"

        result = p.check_chksum()
        self.assertFalse(result)


class TestGPSTN(unittest.TestCase):
    def setup(self):
        pass

    def tearDown(self):
        pass

    def test_parses_map1(self):
        p = GPSTN()
        p.parse("$GPSTN,10")

        self.assertEquals("GPSTN", p.sen_type)
        self.assertEquals("10", p.talker_id)

    def test_parses_map2(self):
        p = GPSTN()
        p.parse("$GPSTN,10*73")

        self.assertEquals("GPSTN", p.sen_type)
        self.assertEquals("10", p.talker_id)
        self.assertEquals("73", p.checksum)


class TestGPTRF(unittest.TestCase):
    def setup(self):
        pass

    def tearDown(self):
        pass

    def test_parses_map(self):
        p = GPTRF()
        p.parse("$GPTRF,121314.15,020112,123.321,N,0987.232,W,2.3,4.5,6.7,8.9,ABC")

        self.assertEquals("GPTRF", p.sen_type)
        self.assertEquals("121314.15", p.timestamp)
        self.assertEquals("020112", p.date)
        self.assertEquals("123.321", p.lat)
        self.assertEquals("N", p.lat_dir)
        self.assertEquals("0987.232", p.lon)
        self.assertEquals("W", p.lon_dir)
        self.assertEquals("2.3", p.ele_angle)
        self.assertEquals("4.5", p.num_iterations)
        self.assertEquals("6.7", p.num_doppler_intervals)
        self.assertEquals("8.9", p.update_dist)
        self.assertEquals("ABC", p.sat_id)


class TestGPVBW(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parses_map(self):
        p = GPVBW()
        p.parse("$GPVBW,10.1,-0.2,A,9.8,-0.5,A*62")

        self.assertEquals("GPVBW", p.sen_type)
        self.assertEquals("10.1", p.lon_water_spd)
        self.assertEquals("-0.2", p.trans_water_spd)
        self.assertEquals("A", p.data_validity_water_spd)
        self.assertEquals("9.8", p.lon_grnd_spd)
        self.assertEquals("-0.5", p.trans_grnd_spd)
        self.assertEquals("A", p.data_validity_grnd_spd)


class TestGPVTG(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parses_map_1(self):
        p = GPVTG()
        p.parse("$GPVTG,360.0,T,348.7,M,000.0,N,000.0,K*43")

        self.assertEquals("GPVTG", p.sen_type)
        self.assertEquals("360.0", p.true_track)
        self.assertEquals("T", p.true_track_sym)
        self.assertEquals("348.7", p.mag_track)
        self.assertEquals("M", p.mag_track_sym)
        self.assertEquals("000.0", p.spd_over_grnd_kts)
        self.assertEquals("N", p.spd_over_grnd_kts_sym)
        self.assertEquals("000.0", p.spd_over_grnd_kmph)
        self.assertEquals("K", p.spd_over_grnd_kmph_sym)
        self.assertEquals('43', p.checksum)

    def test_parses_map_2(self):
        p = GPVTG()
        p.parse("GPVTG,054.7,T,034.4,M,005.5,N,010.2,K")

        self.assertEquals("GPVTG", p.sen_type)
        self.assertEquals("054.7", p.true_track)
        self.assertEquals("T", p.true_track_sym)
        self.assertEquals("034.4", p.mag_track)
        self.assertEquals("M", p.mag_track_sym)
        self.assertEquals("005.5", p.spd_over_grnd_kts)
        self.assertEquals("N", p.spd_over_grnd_kts_sym)
        self.assertEquals("010.2", p.spd_over_grnd_kmph)
        self.assertEquals("K", p.spd_over_grnd_kmph_sym)
        self.assertFalse(hasattr(p, 'checksum'))

    def test_parses_map3(self):
        p = GPVTG()
        p.parse("$GPVTG,t,T,,,s.ss,N,s.ss,K*hh")

        self.assertEquals("GPVTG", p.sen_type)
        self.assertEquals("t", p.true_track)
        self.assertEquals("T", p.true_track_sym)
        self.assertEquals("", p.mag_track)
        self.assertEquals("", p.mag_track_sym)
        self.assertEquals("s.ss", p.spd_over_grnd_kts)
        self.assertEquals("N", p.spd_over_grnd_kts_sym)
        self.assertEquals("s.ss", p.spd_over_grnd_kmph)

        # The checksum did not get stripped off as it is invalid
        # (not a hex pair).
        self.assertEquals("K*hh", p.spd_over_grnd_kmph_sym)

        # Despite a checksum being listed in the sentence, there should NOT be
        # on on the object as 'hh' is not a valid hex pair
        self.assertFalse(hasattr(p, 'checksum'))


class TestGPZDA(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parses_map(self):
        p = GPZDA()
        p.parse("$GPZDA,025959.000,01,01,1970,,*5B")

        self.assertEquals("GPZDA", p.sen_type)
        self.assertEquals("025959.000", p.timestamp)
        self.assertEquals("01", p.day)
        self.assertEquals("01", p.month)
        self.assertEquals("1970", p.year)
        self.assertEquals("", p.local_zone)
        self.assertEquals("", p.local_zone_minutes)
        self.assertEquals("5B", p.checksum)

    def test_checksum_passes(self):
        p = GPZDA()
        p.checksum = '5B'
        p.nmea_sentence = '$GPZDA,025959.000,01,01,1970,,*5B'

        result = p.check_chksum()

        self.assertTrue(result)

    def test_checksum_fails(self):
        p = GPZDA()
        p.checksum = 'b5'
        p.nmea_sentence = '$GPZDA,025959.000,01,01,1970,,*b5'

        result = p.check_chksum()

        self.assertFalse(result)


class TestGPWCV(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parses_map(self):
        p = GPWCV()
        p.parse("$GPWCV,2.3,N,ABCD*1C")

        self.assertEquals("GPWCV", p.sen_type)
        self.assertEquals("2.3", p.velocity)
        self.assertEquals("N", p.vel_units)
        self.assertEquals("ABCD", p.waypoint_id)

    def test_checksum_passes(self):
        p = GPWCV()
        p.checksum = '1C'
        p.nmea_sentence = '$GPWCV,2.3,N,ABCD*1C'

        result = p.check_chksum()

        self.assertTrue(result)

    def test_checksum_fails(self):
        p = GPWCV()
        p.checksum = '1B'
        p.nmea_sentence = '$GPWCV,2.3,N,ABCD*1B'

        result = p.check_chksum()

        self.assertFalse(result)


class TestGPWNC(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parses_map(self):
        p = GPWNC()
        p.parse("$GPWNC,1.1,N,2.2,K,c--c,c--c*ff")

        self.assertEquals("GPWNC", p.sen_type)
        self.assertEquals("1.1", p.dist_nautical_miles)
        self.assertEquals("N", p.dist_naut_unit)
        self.assertEquals("2.2", p.dist_km)
        self.assertEquals("K", p.dist_km_unit)
        self.assertEquals("c--c", p.waypoint_origin_id)
        self.assertEquals("c--c", p.waypoint_dest_id)
        self.assertEquals("ff", p.checksum)


class TestGPWPL(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parses_map_1(self):
        p = GPWPL()
        p.parse("$GPWPL,4917.16,N,12310.64,W,003*65")

        self.assertEquals("GPWPL", p.sen_type)
        self.assertEquals("4917.16", p.lat)
        self.assertEquals("N", p.lat_dir)
        self.assertEquals("12310.64", p.lon)
        self.assertEquals("W", p.lon_dir)
        self.assertEquals("003", p.waypoint_id)
        self.assertEquals("65", p.checksum)

    def test_parses_map_2(self):
        p = GPWPL()
        p.parse("$GPWPL,5128.62,N,00027.58,W,EGLL*59")

        self.assertEquals("GPWPL", p.sen_type)
        self.assertEquals("5128.62", p.lat)
        self.assertEquals("N", p.lat_dir)
        self.assertEquals("00027.58", p.lon)
        self.assertEquals("W", p.lon_dir)
        self.assertEquals("EGLL", p.waypoint_id)
        self.assertEquals("59", p.checksum)


class TestGPXTE(unittest.TestCase):
    def setUp(Self):
        pass

    def tearDown(self):
        pass

    def test_parses_map_1(self):
        p = GPXTE()
        p.parse("$GPXTE,A,A,0.67,L,N")

        self.assertEquals("GPXTE", p.sen_type)
        self.assertEquals("A", p.warning_flag)
        self.assertEquals("A", p.lock_flag)
        self.assertEquals("0.67", p.cross_track_err_dist)
        self.assertEquals("L", p.correction_dir)
        self.assertEquals("N", p.dist_units)

    def test_parses_map_2(self):
        p = GPXTE()
        p.parse("$GPXTE,A,A,4.07,L,N*6D")

        self.assertEquals("GPXTE", p.sen_type)
        self.assertEquals("A", p.warning_flag)
        self.assertEquals("A", p.lock_flag)
        self.assertEquals("4.07", p.cross_track_err_dist)
        self.assertEquals("L", p.correction_dir)
        self.assertEquals("N", p.dist_units)
        self.assertEquals("6D", p.checksum)


class TestPGRME(unittest.TestCase):
    def test_parses_map(self):
        p = PGRME()
        p.parse("$PGRME,3.1,M,4.2,M,5.2,M*2D")

        self.assertEqual("PGRME", p.sen_type)
        self.assertEqual("3.1", p.hpe)
        self.assertEqual("M", p.hpe_unit)
        self.assertEqual("4.2", p.vpe)
        self.assertEqual("M", p.vpe_unit)
        self.assertEqual("5.2", p.osepe)
        self.assertEqual("M", p.osepe_unit)


class TestPGRMM(unittest.TestCase):
    def test_parses_map(self):
        p = PGRMM()
        p.parse("PGRMM,WGS 84*06")

        self.assertEqual("PGRMM", p.sen_type)
        self.assertEqual("WGS 84", p.datum)


class TestPGRMZ(unittest.TestCase):
    def test_parses_map(self):
        p = PGRMZ()
        p.parse("PGRMZ,492,f,3*14")

        self.assertEqual("PGRMZ", p.sen_type)
        self.assertEqual("492", p.altitude)
        self.assertEqual("f", p.altitude_unit)
        self.assertEqual("3", p.pos_fix_dim)


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
        nmea_str7 = '$GPHDT,227.66,T*02'

        result1 = checksum_calc(nmea_str1)
        result2 = checksum_calc(nmea_str2)
        result3 = checksum_calc(nmea_str3)
        result4 = checksum_calc(nmea_str4)
        result5 = checksum_calc(nmea_str5)
        result6 = checksum_calc(nmea_str6)
        result7 = checksum_calc(nmea_str7)

        self.assertEquals(result1, '77')
        self.assertEquals(result2, '77')
        self.assertEquals(result3, '77')
        self.assertEquals(result4, '77')
        self.assertEquals(result5, '77')
        self.assertEquals(result6, '77')
        self.assertEquals(result7, '02')
