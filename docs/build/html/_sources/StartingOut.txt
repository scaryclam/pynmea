Using the NMEA part of this library is simple:

.. code-block:: python

    from pynmea import nmea
    
    # This is a GPGGA sentence
    data = '$GPGGA,064746.000,4925.4895,N,00103.9255,E,1,05,2.1,-68.0,M,47.1,M,,0000*4F'

    # Create the object
    gpgga = nmea.GPGGA()

    # Ask the object to parse the data
    gpgga.parse(data)


That's it. All of the data from the gpgga sentence is not accessible on the object. So gpgga.latitude is '4925.4895' and gpgga.num_sats is '05'.
