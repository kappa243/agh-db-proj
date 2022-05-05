# import click
# from flask.cli import FlaskGroup
# from app import app
#
# cli = FlaskGroup(app)
#
#
# @cli.command('test')
# @click.argument('test_case', default='test*.py')
# def test(test_case='test*.py'):
#
#
# import os
# from flask_script import Manager
# from flask_migrate import Migrate, MigrateCommand
#
# from app import app, db
#
# app.config.from_object(os.environ['APP_SETTINGS'])
#
# migrate = Migrate(app, db)
# manager = Manager(app)
#
# manager.add_command('db', MigrateCommand)
#
# if __name__ == "__main__":
#     cli()
