import sys
import gtk

from front import BSplitFrontEnd

def usage():
    print "Usage:"
    print "\tbananasplit [FILE]"
    sys.exit(1)

if len(sys.argv) > 2:
    usage()

# Set up arguments
if len(sys.argv) > 1:
    filename = sys.argv[1]

fe = BSplitFrontEnd()
fe.main()
