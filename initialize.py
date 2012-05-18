#!/usr/bin/env python

from shuttle import db, Shuttle, ShuttleLeg

# WARNING! Drops all tables!
db.drop_all()

# Following will create the DB.
db.create_all()

aus = 'Austin Office'
spm = 'Southpark Meadows'
castle = 'Castle'

# Populate the shuttle table
shuttle_big = Shuttle(30, 'Big')
shuttle_small = Shuttle(15, 'Small')
db.session.add(shuttle_big)
db.session.add(shuttle_small)
db.session.commit()

# Populate shuttle_leg table

time0715 = 7 * 60 + 15 # Minutes since midnight

to_san_0715 = ShuttleLeg(aus, castle, time0715, None, 0, shuttle_big)
db.session.add(to_san_0715)
db.session.commit()

"""
Do the following to reconstitute datetime object based on minutes since midnight

>> from datetime import datetime, date, time, timedelta
>> d = date.today()
>> t = time(0, 0)
>> datetime.combine(d, t) + timedelta(minutes=435)
datetime.datetime(2012, 5, 18, 7, 15)
"""