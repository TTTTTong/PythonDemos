from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from FlaskDemo.flask_demo import app
from FlaskDemo.exts import db

manager = Manager(app)
manager.add_command('db', MigrateCommand)

# 使用migrate绑定app和db
migrate = Migrate(app, db)

if __name__ == '__main__':
    manager.run()