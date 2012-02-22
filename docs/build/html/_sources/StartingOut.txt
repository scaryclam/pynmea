Starting Out
------------

Here is a short, quickstart guide to using pynmea

Using the NMEA part of this library is simple:

.. code-block:: python

    from pynmea import nmea
    
    # This is a GPGGA sentence
    data = '$GPGGA,064746.000,4925.4895,N,00103.9255,E,1,05,2.1,-68.0,M,47.1,M,,0000*4F'

    # Create the object
    gpgga = nmea.GPGGA()

    # Ask the object to parse the data
    gpgga.parse(data)


That's it. All of the data from the gpgga sentence is now accessible on the object. So gpgga.latitude is '4925.4895' and gpgga.num_sats is '05'.

This is only of limited use however. Splitting up and parsing the raw data is one of the more tedious jobs. For this reason the NMEAStreamer
was created:

.. code-block:: python

    from pynmea.streamer import NMEAStreamer

    with open('example_data_file.txt', 'r') as data_file:
        streamer = NMEAStreamer(data_file)
        next_data = streamer.get_strings()
        data = []
        while next_data:
            data += next_data
            next_data = streamer(read)

This code snippet would read an entire NMEA data file and output the contents into data, which is a list of sentences.

You may also chose to return a list of NMEA objects rather than plain text strings:

.. code-block:: python

    from pynmea.streamer import NMEAStreamer

    with open('example_data_file.txt', 'r') as data_file:
        streamer = NMEAStreamer(data_file)
        next_data = streamer.get_objects()
        data = []
        while next_data:
            data += next_data
            next_data = streamer(read)


You may also feed the streamer raw data from memory:

.. code-block:: python

    from pynmea.streamer import NMEAStreamer

    streamer = NMEAStreamer()

    raw_data = '$GPGGA,064746.000,4925.4895,N,00103.9255,E,1,05,2.1,-68.0,M,47.1,M,,0000*4F\n$GPGGA,064746.000,4925.4895,N,00103.9255,E,1,05,2.1,-68.0,M,47.1,M,,0000*4F\n$GPGGA,064746.000,4925.4895,N,00103.9255,E,1,05,2.1,-68.0,M,47.1,M,,0000*4F'

    data_obs = streamer.get_objects(data=raw_data)
    # Remember to make sure you feed some empty data to flush the last of the data out
    data_obs += streamer.get_objects(data='')

data is then a list of nmea objects. The same can be done with get_string(data=data) to retrieve a list of strings.


