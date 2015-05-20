#!/usr/bin/env python3

import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import *

engine = create_engine(sys.argv[1])
Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)
s = session()
user = User(token="aab8d0dc34b59ee9e804f1261a2da9a82feafb64054cd40c4a62fa0767aed228096e558b13452623579208ed33904c6762c4ad625c4e7b25c2b2688e2e5ebb0c", name="moritz")
s.add(user)
s.commit()
