# coding=utf-8
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from ihome import create_app, db

# 需求：不修改业务逻辑代码，只通过修改manager.py的代码
app = create_app('development')
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
