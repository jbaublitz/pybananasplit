# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
