# coding=utf-8
"""项目启动文件"""

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from ihome import create_app, db, models

# 需求：不修改业务逻辑代码，只通过修改manager.py的代码，实现转换不同模式：开发，测试，生产
app = create_app('development')
# 创建Manager管理对象
manager = Manager(app)
Migrate(app, db)
# 添加迁移命令
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
