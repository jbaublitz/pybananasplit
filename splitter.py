import wave

class TrackSplitter:
    def __init__(self, in_filename):
        self.wave_file = wave.open(in_filename)
        self.params = self.wave_file.getparams()
        self.framerate = self.params[2]
        nframes = self.params[3]
        self.duration = nframes // self.framerate

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            print traceback
        self.wave_file.close()

    def create_track(self, out_filename, nsecs):
        data = self.wave_file.readframes(nsecs * self.framerate)

        new_wave_file = wave.open(out_filename, 'w')
        new_wave_file.setparams(self.params)
        new_wave_file.writeframes(data)

        new_wave_file.close()
