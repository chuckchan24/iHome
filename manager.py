# coding=utf-8
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from ihome import app, db



# 创建Manager管理对象
manager = Manager(app)
Migrate(app, db)
# 添加迁移命令
manager.add_command('db', MigrateCommand)


@app.route('/')
def index():

    return 'index'


if __name__ == '__main__':
    manager.run()
