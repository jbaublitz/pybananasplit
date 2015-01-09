import pygtk
pygtk.require('2.0')
import gtk

class BSplitFrontEnd:
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

        self.window.connect('delete_event', self.delete_event)
        self.window.connect('destroy', self.destroy)

        self.tracks = []
        self.add_tracks()

        self.window.show()

    def add_track(self):
        

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def main(self):
        gtk.main()
