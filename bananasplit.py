import sys
import gtk

from gui import FrontEnd

def usage():
    print "Usage:"
    print "\tbananasplit [FILE]"
    sys.exit(1)

if len(sys.argv) > 2:
    usage()

# Set up arguments
filename = None
if len(sys.argv) > 1:
    filename = sys.argv[1]

fe = FrontEnd(filename)
fe.main()
