from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import create_app, db

app = create_app()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def debug():
	app.run(debug=True)


@manager.command
def prod():
	app.run(debug=False, host='0.0.0.0', port='5000', ssl_context=('server.crt', 'server.key'))


if __name__ == '__main__':
	manager.run()