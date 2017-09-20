import os
from app import create_app,db
from app.models import User,Role
from flask.ext.migrate import Migrate,MigrateCommand
from flask.ext.script import Manager,Shell

app = create_app(os.environ.get('FLASK_CONFIG') or 'default')
manage = Manager(app)
migrate = Migrate(app,db)

def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role)
manage.add_command("shell",Shell(make_shell_context))
manage.add_command('db',MigrateCommand)

# @manage.command
# def test():
#     """Run the unit tests."""
#     import unittest
#     tests = unittest.TestLoader.discover('tests','.')
#     unittest.TextTestRunner(verbosity=2).run(tests)





if __name__ == "__main__":
    manage.run()
