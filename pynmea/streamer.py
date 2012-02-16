""" For dealing with streams of nmea data
"""

class NMEAStream(object):
    """ NMEAStream object is used to
    """
    def __init__(self, stream_obj=None):
        """ stream_obj should be a file like object.
            If the requirement is just to split data in memory, no stream_obj
            is required. Simply create an instance of this class and
            call _split directly with the data.
        """
        self.stream = stream_obj
        self.head = ''

    def read(self, size=1024):
        """ Read size bytes of data. Always strip off the last record and
            append to the start of the data stream on the next call.
            This ensures that only full sentences are returned.
        """
        data = self.stream.read(size)
        data = self.head + data
        raw_sentences = self._split(data)
        self.head = raw_sentences[-1]
        full_sentences = raw_sentences[:-1]
        return full_sentences

    def _split(self, data, separator=None):
        """ Take some data and split up based on the notion that a sentence
            looks something like:
            $x,y,z or $x,y,z*ab

            separator is for cases where there is something strange or
            non-standard as a separator between sentences.
            Without this, there is no real way to tell whether:
            $x,y,zSTUFF
            is legal or if STUFF should be stripped.
        """
        sentences = data.split('$')
        clean_sentences = []
        for item in sentences:
            cleaned_item = item.rstrip()
            if separator:
                cleaned_item = cleaned_item.rstrip(separator)
            if '*' in cleaned_item.split(',')[-1]:
                # There must be a checksum. Remove any trailing fluff:
                try:
                    first, checksum = cleaned_item.split('*')
                except ValueError:
                    # Some GPS data recorders have been shown to output
                    # run-together sentences (no leading $).
                    # In this case, ignore error and continue, discarding the
                    # erroneous data.
                    # TODO: try and fix the data.
                    continue
                cleaned_item = '*'.join([first, checksum[:2]])
            if cleaned_item:
                clean_sentences.append(cleaned_item)

        return clean_sentences
