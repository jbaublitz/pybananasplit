import os
import sys
import git

from gui import FrontEnd

def usage():
    print "Usage:"
    print "\tbananasplit [UPDATE_DIR]"
    sys.exit(1)

if len(sys.argv) > 2:
    usage()

# Set up arguments
update_dir = None
if len(sys.argv) > 1:
    update_dir = sys.argv[1]

if update_dir:
    g = git.cmd.Git(update_dir)
    ret = g.pull()
    for info in ret:
        if not info.flags & HEAD_UPTODATE:
            os.execv(__file__, sys.argv)

fe = FrontEnd(None)
fe.main()
