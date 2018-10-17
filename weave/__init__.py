import os
import logging
import sys
from flask import Flask
from flask_cors import CORS
application = Flask(__name__, static_folder='../static')
CORS(application)
from .db import *

db = DBConnection()

import weave.routes.echo
import weave.routes.video
# import weave.routes.hardcode


# if 'DYNO' in os.environ:
#     logFormatter = logging.Formatter("%(asctime)s [%(filename)s] [%(funcName)s] [%(lineno)d] [%(levelname)-5.5s]  %(message)s")
#     specialHandler = logging.StreamHandler(sys.stdout)
#     specialHandler.setFormatter(logFormatter)
#     application.logger.addHandler(specialHandler)
#     # app.logger.addHandler(logging.StreamHandler(sys.stdout))
#     application.logger.setLevel(logging.INFO)
