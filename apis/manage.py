from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from config import config
from app import create_app, db

app = create_app(config)

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def debug():
	app.run(debug=True, host="localhost")


if __name__ == '__main__':
	manager.run()