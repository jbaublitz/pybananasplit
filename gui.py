import pygtk
pygtk.require('2.0')
import gtk

class FrontEnd:
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

        self.window.connect('delete_event', self.delete_event)
        self.window.connect('destroy', self.destroy)

        self.tracks = []
        self.add_track()

        self.window.show()

    def add_track(self, widget=None, data=None):
        hbox = gtk.HBox(False, 0)
        textbox = gtk.Entry(100)
        button = gtk.Button(stock=gtk.STOCK_DELETE)

        hbox.pack_end(textbox)
        hbox.pack_end(button)

        self.tracks.append(hbox)
        self.window.add(hbox)

        hbox.show()
        textbox.show()
        button.show()

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def main(self):
        gtk.main()

fe = FrontEnd()
fe.main()
