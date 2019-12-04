from flask import render_template
from app import app, db

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

# For all the view functions that I created so far,
# I did not need to add a second return value because the default of 200 (the status code for a successful response) is what I wanted.
# In this case these are error pages, so I want the status code of the response to reflect that.
