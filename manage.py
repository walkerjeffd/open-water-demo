import os
from app import create_app, db
from app.models import User
from app.models import User, Location, Project
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def test():
    """Run the unit tests.
    >> python manage.py test
    """
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.command
def bootstrap():
    """Bootstrap database
    >> python manage.py bootstrap
    """
    db.drop_all()
    db.create_all()
    user = User(email='jeff@walkerjeff.com',
                username='jeff',
                password='password',
                confirmed=True,
                name='Jeff Walker',
                location='Brunswick, ME')
    db.session.add(user)
    location = Location(name='Androscoggin River',
                        latitude=43.9211128,
                        longitude=-69.9603785)
    db.session.add(location)
    project = Project(name="Jeff's Backyard")
    db.session.add(project)
    db.session.commit()

if __name__ == '__main__':
    manager.run()
