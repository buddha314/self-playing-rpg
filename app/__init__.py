from flask import Flask
app = Flask(__name__)

import models
import services
from services import *
from models import *

n_lat = 100
n_long = 100
n_initial_inhabitants = 20
n_days= 365
n_years = 2


world = World(n_lat,n_long, n_initial_inhabitants)
#run_world(world, n_days)
