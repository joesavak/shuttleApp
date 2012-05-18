#!/usr/bin/env python

from shuttle import db

# WARNING! Drops all tables!
db.drop_all()

# Following will create the DB.
db.create_all()