from app import observ, db
from app.models import User, Sub

@observ.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Sub': Sub}
