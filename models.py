from db_config import db

class User(db.Model):
    """
    用户模型类，对应数据库中的user表
    
    属性:
        user_id: 用户ID，主键
        user_name: 用户名，唯一且不能为空
        user_password: 用户密码，不能为空
    """
    __tablename__ = 'user'  # 指定表名
    
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), unique=True, nullable=False)
    user_password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        """返回用户对象的字符串表示"""
        return f'<User {self.user_name}>'

class Module(db.Model):
    """
    模块模型类，对应数据库中的module表
    
    属性:
        module_id: 模块ID，主键
        permission_id: 权限ID
        module_description: 模块描述
        module_router: 模块路由
    """
    __tablename__ = 'module'
    
    module_id = db.Column(db.Integer, primary_key=True)
    permission_id = db.Column(db.Integer, nullable=False)
    module_description = db.Column(db.String(255), nullable=False)
    module_router = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        """返回模块对象的字符串表示"""
        return f'<Module {self.module_description}>'

class Permission(db.Model):
    """
    权限模型类，对应数据库中的permission表
    
    属性:
        user_id: 用户ID，主键
        permission_id: 权限ID
    """
    __tablename__ = 'permission'
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)  # user_id 设为主键
    permission_id = db.Column(db.Integer, nullable=False)  # permission_id 作为普通字段

    def __repr__(self):
        """返回权限对象的字符串表示"""
        return f'<Permission {self.user_id}>'

class UserInfo(db.Model):
    """
    用户信息模型类，对应数据库中的user_info表
    
    属性:
        user_id: 用户ID，主键
        name: 用户姓名
        user_address: 用户地址
        user_phone: 用户电话
    """
    __tablename__ = 'user_info'
    
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    user_address = db.Column(db.String(255))
    user_phone = db.Column(db.String(20))

    def __repr__(self):
        """返回用户信息对象的字符串表示"""
        return f'<UserInfo {self.user_id}>'

class Shuju(db.Model):
    """
    数据模型类，对应数据库中的shuju表

    属性:
        id: 主键
        cirrhosis: 肝硬化
        age: 年龄
        sex: 性别
        cholesterol: 胆固醇
        triglyceride: 甘油三酯
        HDL: 高密度脂蛋白
        LDL: 低密度脂蛋白
        PathDiagNum: 病理诊断编号
        BMI: 体重指数
        ALT: 谷丙转氨酶
        AST: 谷草转氨酶
        glucose: 血糖
    """
    __tablename__ = 'shuju'

    id = db.Column(db.Integer, primary_key=True)
    cirrhosis = db.Column(db.Float, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.Integer, nullable=False)
    cholesterol = db.Column(db.Float, nullable=False)
    triglyceride = db.Column(db.Float, nullable=False)
    HDL = db.Column(db.Float, nullable=False)
    LDL = db.Column(db.Float, nullable=False)
    PathDiagNum = db.Column(db.Integer, nullable=False)
    BMI = db.Column(db.Float, nullable=False)
    ALT = db.Column(db.Float, nullable=False)
    AST = db.Column(db.Float, nullable=False)
    glucose = db.Column(db.Float, nullable=False)

    def __repr__(self):
        """返回数据对象的字符串表示"""
        return f'<Shuju id={self.id}>'


class Shuju2(db.Model):
    """
    加密数据模型类，对应数据库中的shuju2表

    属性:
        id: 主键，int类型
        cirrhosis: 肝硬化，text类型
        age: 年龄，text类型
        sex: 性别，text类型
        cholesterol: 胆固醇，text类型
        triglyceride: 甘油三酯，text类型
        HDL: 高密度脂蛋白，text类型
        LDL: 低密度脂蛋白，text类型
        PathDiagNum: 病理诊断编号，text类型
        BMI: 体重指数，text类型
        ALT: 谷丙转氨酶，text类型
        AST: 谷草转氨酶，text类型
        glucose: 血糖，text类型
    """
    __tablename__ = 'shuju2'

    id = db.Column(db.Integer, primary_key=True)
    cirrhosis = db.Column(db.Text, nullable=False)
    age = db.Column(db.Text, nullable=False)
    sex = db.Column(db.Text, nullable=False)
    cholesterol = db.Column(db.Text, nullable=False)
    triglyceride = db.Column(db.Text, nullable=False)
    HDL = db.Column(db.Text, nullable=False)
    LDL = db.Column(db.Text, nullable=False)
    PathDiagNum = db.Column(db.Text, nullable=False)
    BMI = db.Column(db.Text, nullable=False)
    ALT = db.Column(db.Text, nullable=False)
    AST = db.Column(db.Text, nullable=False)
    glucose = db.Column(db.Text, nullable=False)

    def __repr__(self):
        """返回加密数据对象的字符串表示"""
        return f'<Shuju2 id={self.id}>'


class UserData(db.Model):
    """
    用户数据模型类，对应数据库中的user_data表

    属性:
        user_id: 用户ID，主键
        data_id: 数据ID，主键
    """
    __tablename__ = 'user_data'

    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    data_id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        """返回用户数据对象的字符串表示"""
        return f'<UserData user_id={self.user_id}, data_id={self.data_id}>'
    
    
