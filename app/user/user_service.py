from app import db
from flask import current_app
from app.models import User, Activity, Checkout


#
# Save a user
#
def save(user):
    db.session.add(user)
    db.session.commit()
    return user


def get_total_checkouts(id):
    checkouts = Checkout.query.filter_by(user_id = id, returned=False).all()
    return len(checkouts)

#
# Add a post to user
#


#
# Remove post
#
