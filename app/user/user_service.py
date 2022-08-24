from app import db
from flask import current_app
from app.models import User, Activity


#
# Save a user
#
def save(user):
    db.session.add(user)
    db.session.commit()
    return user


#
# Add a post to user
#


#
# Remove post
#
