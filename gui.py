import pygtk
pygtk.require('2.0')
import gtk

from wavefuncs import TrackSplitter

class FrontEnd:
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.vbox_main = gtk.VBox(False, 0)
        self.add_button = gtk.Button(stock=gtk.STOCK_ADD)
        self.button_bar = gtk.HBox(False, 0)
        self.split_button = gtk.Button(label='Split file')
        self.filename = gtk.HBox(False, 0)
        self.filename_label = gtk.Label('File name: ')
        self.filename_box = gtk.Entry(300)
        self.tracks = gtk.VBox(False, 0)

        self.window.connect('delete_event', self.delete_event)
        self.window.connect('destroy', self.destroy)
        self.split_button.connect('clicked', self.split_file)
        self.add_button.connect('clicked', self.add_track)

        self.button_bar.pack_start(self.split_button)

        self.filename.pack_start(self.filename_label)
        self.filename.pack_start(self.filename_box)

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
        self.filename_box.show()
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

    def split_file(self, obj):
        ts = TrackSplitter('Noise.wav')
        for w in self.tracks:
            print w

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def main(self):
        gtk.main()