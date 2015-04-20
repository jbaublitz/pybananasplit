import wave

class TrackSplitter:
    def __init__(self, in_filename):
        self.last_nsecs = None
        self.wave_file = wave.open(in_filename)
        self.params = self.wave_file.getparams()
        self.framerate = self.params[2]
        nframes = self.params[3]
        self.duration = nframes / self.framerate

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.wave_file.close()

    def create_track(self, out_filename, start_text, stop_text):
        start_nsecs = self.splitpoint_str_to_secs(start_text)
        stop_nsecs = self.splitpoint_str_to_secs(stop_text)

        if self.last_nsecs > start_nsecs or start_nsecs > stop_nsecs:
            raise ValueError('Tracks out of order.')

        # Discard silence between tracks and then write file
        if self.last_nsecs is not None:
            self.read_nsecs(start_nsecs - self.last_nsecs)
        self.write_file(out_filename, stop_nsecs - start_nsecs)

        self.last_nsecs = stop_nsecs

    def splitpoint_str_to_secs(self, text):
        l = text.split(':')
        if len(l) == 2:
            return int(l[0]) * 60 + int(l[1])
        elif len(l) == 3:
            return int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2])

    def write_file(self, out_filename, nsecs):
        data = self.read_nsecs(nsecs)
        if not data:
            raise IOError('End of file reached.')

        new_wave_file = wave.open(out_filename, 'w')
        new_wave_file.setparams(self.params)
        new_wave_file.writeframes(data)

        new_wave_file.close()

    def read_nsecs(self, nsecs):
        return self.wave_file.readframes(nsecs * self.framerate)
