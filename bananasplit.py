import sys
import wave
import gtk

def usage():
    print "Usage:"
    print "\tbananasplit [FILE]"
    sys.exit(1)

if len(sys.argv) > 2:
    usage()

# Set up arguments
if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = "./Noise.wav"

wavinfile = wave.open(filename)
params = wavinfile.getparams()
