#!/usr/bin/python3
import sys
sys.path.insert(0,"/var/www/<appname>/")
sys.path.insert(0,"/var/www/<appname>/<appname>/")

import logging
logging.basicConfig(stream=sys.stderr)

from <appname> import app as application

