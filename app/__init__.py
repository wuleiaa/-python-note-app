from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from app.config import Config

# 初始化数据库插件，但在 create_app 中才绑定 app
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # 加载配置
    app.config.from_object(Config)
    # 初始化插件
    db.init_app(app)
    CORS(app)  # 允许跨域
    # 注册蓝图 (Blueprints)

    # 注册蓝图
    from app.routes.user import user_bp
    app.register_blueprint(user_bp)
    # 【新增】注册笔记蓝图
    from app.routes.note import note_bp
    app.register_blueprint(note_bp)
    # 【新增 1】注册待办蓝图
    from app.routes.todo import todo_bp
    app.register_blueprint(todo_bp)
    # 【新增 1】注册分类和工具蓝图
    from app.routes.category import category_bp
    app.register_blueprint(category_bp)
    from app.routes.tool import tool_bp
    app.register_blueprint(tool_bp)
    # 创建数据库表（如果不存在）
    with app.app_context():
        # 必须导入模型，create_all 才能识别到表
        from app.models.user import User
        # 【新增】导入 Note 模型，否则 create_all 无法创建表
        from app.models.note import Note
        # 【新增 2】导入 Todo 模型
        from app.models.todo import Todo
        # 【新增 2】导入 Category 模型
        from app.models.category import Category

        db.create_all()

    return app