from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import sys
sys.path.append('D:\PyCharmWorkSpace')
from FlaskDemo.flask_demo import app
from FlaskDemo.exts import db
from FlaskDemo.models import User

manager = Manager(app)
manager.add_command('db', MigrateCommand)

# 使用migrate绑定app和db
migrate = Migrate(app, db)

if __name__ == '__main__':
    manager.run()