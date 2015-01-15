import pygtk
pygtk.require('2.0')
import gtk

import re
from datetime import datetime, time

from splitter import TrackSplitter

class FrontEnd:
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.vbox_main = gtk.VBox(False, 0)
        self.add_button = gtk.Button(stock=gtk.STOCK_ADD)
        self.button_bar = gtk.HBox(False, 0)
        self.split_button = gtk.Button(label='Split file')
        self.filename = gtk.HBox(False, 0)
        self.filename_label = gtk.Label('File name: ')
        self.filename_entry = gtk.Entry(300)
        self.tracks = gtk.VBox(False, 0)

        self.window.connect('delete_event', self.delete_event)
        self.window.connect('destroy', self.destroy)
        self.split_button.connect('clicked', self.split_file)
        self.add_button.connect('clicked', self.add_track)

        self.button_bar.pack_start(self.split_button)

        self.filename.pack_start(self.filename_label)
        self.filename.pack_start(self.filename_entry)

        self.vbox_main.pack_start(self.button_bar)
        self.vbox_main.pack_start(self.filename)
        self.vbox_main.pack_start(self.add_button)
        self.vbox_main.pack_start(self.tracks)
        self.window.add(self.vbox_main)

        self.add_track()

        self.vbox_main.show()
        self.button_bar.show()
        self.split_button.show()
        self.add_button.show()
        self.filename.show()
        self.filename_label.show()
        self.filename_entry.show()
        self.tracks.show()

        self.window.show()

    def add_track(self, obj=None):
        hbox = gtk.HBox(False, 0)
        start_label = gtk.Label('Start: ')
        start = gtk.Entry(30)
        stop_label = gtk.Label('Stop: ')
        stop = gtk.Entry(30)
        button = gtk.Button(stock=gtk.STOCK_DELETE)

        button.connect('clicked', self.remove_track)

        hbox.pack_start(start_label)
        hbox.pack_start(start)
        hbox.pack_start(stop_label)
        hbox.pack_start(stop)
        hbox.pack_start(button)

        self.tracks.pack_start(hbox)

        hbox.show()
        start_label.show()
        start.show()
        stop_label.show()
        stop.show()
        button.show()

    def remove_track(self, obj):
        obj.parent.parent.remove(obj.parent)

        # Allow auto-shrink on track removal
        self.window.resize(1, 1)

    def split_file(self, obj):
        filename = self.filename_entry.get_text()
        try:
            with TrackSplitter(filename) as ts:
                rc, ipt = self.validate_input(ts.duration)
                if not rc:
                    raise IOError('Invalid input: %s' % ipt)
                for hbox in self.tracks:
                    self.create_track(hbox)
        except IOError, emsg:
            self.warning_dialog('WAV file split failed: %s' % emsg)

    def validate_input(self, duration):
        last_track = None
        for hbox in self.tracks:
            children = hbox.get_children()
            start_text = children[1].get_text()
            stop_text = children[3].get_text()

            invalid_input = None
            if not re.match(r'^([0-9]+:)?[0-5][0-9]:[0-5][0-9]$', start_text):
                invalid_input = start_text
            if not re.match(r'^([0-9]+:)?[0-5][0-9]:[0-5][0-9]$', stop_text):
                invalid_input = stop_text
            if invalid_input:
                return False, 'Incorrect track time format: %s'

            if last_track is not None and int(last_track.replace(':', None)) > \
                    int(start_text.replace(':', None)):
                return False, 'Tracks out of order, %s should be before %s' % \
                        (last_track, stop_text)
            if last_track is not None and int(start_text.replace(':', None)) > \
                    int(stop_text.replace(':', None)):
                return False, 'Tracks out of order, %s should be before %s' % \
                        (last_track, stop_text)

            last_track = stop_text

        if last_track is not None:
            fmt = None
            if len(last_track.split(':')) == 3:
                fmt = '%H:%M:%S'
            else:
                fmt = '%M:%S'
            time_obj = datetime.strptime(last_track, fmt).time()
            duration_obj = time(duration // 3600, duration % 3600 // 60, duration % 60)

            if time_obj > duration_obj:
                return False, 'Ending of last track extends past the end of the WAV file.'

        return True, 'Success'

    def warning_dialog(self, msg):
        message = gtk.MessageDialog(type=gtk.MESSAGE_WARNING)
        message.set_markup(msg)
        message.add_button(gtk.STOCK_OK, gtk.RESPONSE_CLOSE)
        rc = message.run()
        if rc == gtk.RESPONSE_CLOSE:
            message.destroy()

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def main(self):
        gtk.main()
