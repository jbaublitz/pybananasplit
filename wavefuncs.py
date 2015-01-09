import wave

class TrackSplitter:
    def __init__(self, in_filename):
        self.wave_file = wave.open(in_filename)
        self.params = self.wave_file.getparams()

    def __enter__(self):
        return self

    def __exit__(self):
        self.wave_file.close()

    def create_track(self, out_filename, nsecs):
        framerate = self.params[2]
        data = self.wave_file.readframes(nsecs * framerate)

        new_wave_file = wave.open(out_filename, 'w')
        new_wave_file.setparams(self.params)
        new_wave_file.writeframes(data)

        new_wave_file.close()
