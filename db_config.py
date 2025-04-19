# 导入SQLAlchemy，用于ORM（对象关系映射）操作
from flask_sqlalchemy import SQLAlchemy

# 导入dotenv用于加载环境变量
from dotenv import load_dotenv

# 导入os模块用于访问操作系统环境变量
import os

# 加载.env文件中的环境变量
# 该文件通常用于存储敏感信息，如数据库连接信息
load_dotenv()

# 创建SQLAlchemy实例
# 该实例将用于所有数据库操作，包括模型定义和查询
db = SQLAlchemy()

# 数据库配置函数
def init_db(app):
    """
    初始化数据库配置
    
    参数:
        app: Flask应用实例
        
    功能:
        1. 设置数据库连接URL
        2. 配置SQLAlchemy选项
        3. 将数据库实例与Flask应用绑定
    """
    
    # 设置数据库连接URL
    # 从环境变量中获取DATABASE_URL，如果不存在则使用默认值
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+pymysql://root:@localhost:3306/flask_db')
    
    # 禁用SQLAlchemy的修改追踪功能
    # 该功能会消耗额外内存，在大多数情况下不需要
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # 配置数据库引擎选项
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_size': 10,        # 连接池大小，控制最大连接数
        'pool_recycle': 3600,   # 连接回收时间（秒），防止连接超时
        'pool_pre_ping': True   # 在每次使用连接前进行健康检查
    }
    
    # 将数据库实例与Flask应用绑定
    db.init_app(app)