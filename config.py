import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = 'MHS-v4C1sTS1u%jwU4w$Cv%So5'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:ujDjBkmM46d4E78CFogO@mhs-db.cln5dmhlm9o9.us-east-2.rds.amazonaws.com:5432/postgres' or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    APPLICATION_ROOT = "/api"
