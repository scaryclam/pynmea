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
        self.parts = nmea_str.split(',')
        if '*' in self.parts[-1]:
            d, par, ck = self.parts.pop().rpartition('*')
            self.parts.extend([d, par+ck])

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
        {'N': 'North', 'S': 'South'}
        return self.


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
    #* $GPBOD - Bearing, Origin to Destination
    #* $GPBWC - Bearing & Distance to Waypoint, Great Circle
    #* $GPBWR - Bearing & Distance to Waypoint, Rhumb Line
    #* $GPBWW - Bearing, Waypoint to Waypoint
    #* $GPDBT - Depth Below Transducer
    #* $GPDCN - Decca Position
    #* $GPDPT - Depth
    #* $GPFSI - Frequency Set Information
    #* $GPGGA - Global Positioning System Fix Data
    #* $GPGLC - Geographic Position, Loran-C
    ####* $GPGLL - Geographic Position, Latitude/Longitude
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