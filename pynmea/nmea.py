from pynmea.utils import checksum_calc

class NMEASentence(object):
    """ Base sentence class. This is used to pull apart a sentence.
        It will not have any real reference to what things mean. Things that
        subclass this base class should all the additional functionality.
    """

    def __init__(self, parse_map):
        self.sen_type = None
        self.parse_map = parse_map

    def _parse(self, nmea_str):
        """ Tear the sentence apart, grabbing the name on the way. Create a
            parts attribute on the class and fill in the sentence type in
            sen_type
        """
        self.nmea_sentence = nmea_str
        self.parts = nmea_str.split(',')
        if '*' in self.parts[-1]:
            d, par, ck = self.parts.pop().rpartition('*')
            self.parts.extend([d, ck])

        self.sen_type = self.parts[0]
        if self.parts[0].startswith('$'):
            self.parts[0] = self.parts[0][1:]
        self.sen_type = self.parts[0]

    def parse(self, nmea_str):
        """ Use the parse map. Parse map should be in the format:
            (('Field name', 'field_name'),
             ('Field name', 'field_name'))

             Where the first entry in the tuple is the human readable name
             and the second is the parameter name
        """

        self._parse(nmea_str)
        assert len(self.parts[1:]) <= len(self.parse_map)
        for index, item in enumerate(self.parts[1:]):
            setattr(self, self.parse_map[index][1], item)

    def check_chksum(self):
        # If there is no checksum, raise AssertionError
        assert hasattr(self, 'checksum')

        result = checksum_calc(self.nmea_sentence)
        return (result.replace('0x', '') == self.checksum)




# ---------------------------------------------------------------------------- #
# Here are all the currently supported sentences. All should eventually be
# supported. They are being added as properties and other useful functions are
# implimented. Unit tests are also provided.
# ---------------------------------------------------------------------------- #

class GPGLL(NMEASentence):
    def __init__(self):
        parse_map = (("Latitude", "lat"),
                     ("Direction", "lat_dir"),
                     ("Longitude", "lon"),
                     ("Direction", "lon_dir"),
                     ("Checksum", "checksum"))

        super(GPGLL, self).__init__(parse_map)

    @property
    def latitude(self):
        return float(self.lat)

    @property
    def longitude(self):
        return float(self.lon)

    @property
    def lat_direction(self):
        mapping = {'N': 'North', 'S': 'South'}
        return mapping[self.lat_dir.upper()]

    @property
    def lon_direction(self):
        mapping = {"E": "East", "W": "West"}
        return mapping[self.lon_dir.upper()]


class GPBOD(NMEASentence):
    def __init__(self):
        # 045.,T,023.,M,DEST,START
        parse_map = (('Bearing True', 'bearing_t'),
                     ('Bearing True Type', 'bearing_t_type'),
                     ('Bearing Magnetic', 'bearing_mag'),
                     ('Bearing Magnetic Type', 'bearing_mag_type'),
                     ('Destination', 'dest'),
                     ('Start', 'start'))

        super(GPBOD, self).__init__(parse_map)

    @property
    def bearing_true(self):
        return ','.join([self.bearing_t, self.bearing_t_type])

    @property
    def bearing_magnetic(self):
        return ','.join([self.bearing_mag, self.bearing_mag_type])

    @property
    def destination(self):
        return self.dest

    @property
    def origin(self):
        return self.start


class GPBWC(NMEASentence):
    def __init__(self):
        parse_map = (
            ('Timestamp', 'timestamp'),
            ('Latitude of next Waypoint', 'lat_next'),
            ('Latitude of next Waypoint Direction', 'lat_next_direction'),
            ('Longitude of next Waypoint', 'lon_next'),
            ('Longitude of next Waypoint Direction', 'lon_next_direction'),
            ('True track to waypoint', 'true_track'),
            ('True Track Symbol', 'true_track_sym'),
            ('Magnetic track to waypoint', 'mag_track'),
            ('Magnetic Symbol', 'mag_sym'),
            ('Range to waypoint', 'range_next'),
            ('Unit of range', 'range_unit'),
            ('Waypoint Name', 'waypoint_name'),
            ('Checksum', 'checksum'))

        super(GPBWC, self).__init__(parse_map)


class GPBWR(NMEASentence):
    def __init__(self):
        parse_map = (
            ('Timestamp', 'timestamp'),
            ('Latitude of next Waypoint', 'lat_next'),
            ('Latitude of next Waypoint Direction', 'lat_next_direction'),
            ('Longitude of next Waypoint', 'lon_next'),
            ('Longitude of next Waypoint Direction', 'lon_next_direction'),
            ('True track to waypoint', 'true_track'),
            ('True Track Symbol', 'true_track_sym'),
            ('Magnetic track to waypoint', 'mag_track'),
            ('Magnetic Symbol', 'mag_sym'),
            ('Range to waypoint', 'range_next'),
            ('Unit of range', 'range_unit'),
            ('Waypoint Name', 'waypoint_name'),
            ('Checksum', 'checksum'))

        super(GPBWR, self).__init__(parse_map)


#class GPAAM(NMEASentence):
    #def __init__(self):
        #super(GPAAM).__init__()


#class GPALM(NMEASentence):
    #def __init__(self):
        #super(GPALM).__init__()


#class GPAPA(NMEASentence):
    #def __init__(self):
        #super(GPAPA).__init__()


#class GPAPB(NMEASentence):
    #def __init__(self):
        #super(GPAPB).__init__()


#class GPASD(NMEASentence):
    #def __init__(self):
        #super(GPASD).__init__()


    #* $GPBEC - Bearing & Distance to Waypoint, Dead Reckoning



    #* $GPBWW - Bearing, Waypoint to Waypoint
    #* $GPDBT - Depth Below Transducer
    #* $GPDCN - Decca Position
    #* $GPDPT - Depth
    #* $GPFSI - Frequency Set Information
    #* $GPGGA - Global Positioning System Fix Data
    #* $GPGLC - Geographic Position, Loran-C
    #* $GPGSA - GPS DOP and Active Satellites
    #* $GPGSV - GPS Satellites in View
    #* $GPGXA - TRANSIT Position
    #* $GPHDG - Heading, Deviation & Variation
    #* $GPHDT - Heading, True
    #* $GPHSC - Heading Steering Command
    #* $GPLCD - Loran-C Signal Data
    #* $GPMTA - Air Temperature (to be phased out)
    #* $GPMTW - Water Temperature
    #* $GPMWD - Wind Direction
    #* $GPMWV - Wind Speed and Angle
    #* $GPOLN - Omega Lane Numbers
    #* $GPOSD - Own Ship Data
    #* $GPR00 - Waypoint active route (not standard)
    #* $GPRMA - Recommended Minimum Specific Loran-C Data
    #* $GPRMB - Recommended Minimum Navigation Information
    #* $GPRMC - Recommended Minimum Specific GPS/TRANSIT Data
    #* $GPROT - Rate of Turn
    #* $GPRPM - Revolutions
    #* $GPRSA - Rudder Sensor Angle
    #* $GPRSD - RADAR System Data
    #* $GPRTE - Routes
    #* $GPSFI - Scanning Frequency Information
    #* $GPSTN - Multiple Data ID
    #* $GPTRF - Transit Fix Data
    #* $GPTTM - Tracked Target Message
    #* $GPVBW - Dual Ground/Water Speed
    #* $GPVDR - Set and Drift
    #* $GPVHW - Water Speed and Heading
    #* $GPVLW - Distance Traveled through the Water
    #* $GPVPW - Speed, Measured Parallel to Wind
    #* $GPVTG - Track Made Good and Ground Speed
    #* $GPWCV - Waypoint Closure Velocity
    #* $GPWNC - Distance, Waypoint to Waypoint
    #* $GPWPL - Waypoint Location
    #* $GPXDR - Transducer Measurements
    #* $GPXTE - Cross-Track Error, Measured
    #* $GPXTR - Cross-Track Error, Dead Reckoning
    #* $GPZDA - Time & Date
    #* $GPZFO - UTC & Time from Origin Waypoint
    #* $GPZTG - UTC & Time to Destination Waypoint
