import sys
import logging

sys.path.insert(0, "/home/lucas/MOinfo/Flask")

from app import app as application

# Log Python errors to Apache error log
logging.basicConfig(stream=sys.stderr)
