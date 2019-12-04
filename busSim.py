from app import app, db
from app.models import User

@app.shell_context_processor #registers the function as a shell context function
def make_shell_context():
    return {'db': db, 'User': User}
