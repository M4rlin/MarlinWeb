import sys, os
INTERP = "/home/marlin/public_html/Marlin/bin/python3"
#INTERP is present twice so that the new Python interpreter knows the actual executable path
if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)
import SP.wsgi
application = SP.wsgi.application
