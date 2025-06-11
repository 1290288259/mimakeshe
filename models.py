from db_config import db
from datetime import datetime, timezone, timedelta # 导入timezone和timedelta

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
        group_id: 分组ID，用于数据分组
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
    group_id = db.Column(db.Integer, default=1, nullable=False)  # 新增分组字段，默认为1

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
        group_id: 分组ID，用于数据分组
    """
    __tablename__ = 'shuju2'

    id = db.Column(db.String(11), primary_key=True)  # 将整数类型改为字符串类型，长度为50
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
    group_id = db.Column(db.Integer, default=1, nullable=False)  # 新增分组字段，默认为1

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


class Avg(db.Model):
    """
    平均值模型类，对应数据库中的avg表
    属性:
        id: 主键，自增
        age: 年龄字段平均值
        cholesterol: 胆固醇字段平均值
        triglyceride: 甘油三酯字段平均值
        HDL: 高密度脂蛋白字段平均值
        LDL: 低密度脂蛋白字段平均值
        BMI: 体重指数字段平均值
        ALT: 谷丙转氨酶字段平均值
        AST: 谷草转氨酶字段平均值
        glucose: 血糖字段平均值
        created_at: 存入时间，自动记录
    """
    __tablename__ = 'avg'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键，自增
    age = db.Column(db.Float)            # 年龄字段平均值
    cholesterol = db.Column(db.Float)    # 胆固醇字段平均值
    triglyceride = db.Column(db.Float)   # 甘油三酯字段平均值
    HDL = db.Column(db.Float)            # 高密度脂蛋白字段平均值
    LDL = db.Column(db.Float)            # 低密度脂蛋白字段平均值
    BMI = db.Column(db.Float)            # 体重指数字段平均值
    ALT = db.Column(db.Float)            # 谷丙转氨酶字段平均值
    AST = db.Column(db.Float)            # 谷草转氨酶字段平均值
    glucose = db.Column(db.Float)        # 血糖字段平均值
   # 强制存储北京时间（UTC+8）
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(hours=8)
    ) 

    def __repr__(self):
        """返回平均值对象的字符串表示"""
        return f'<Avg id={self.id} created_at={self.created_at}>'


class Analysis_result(db.Model):
    """
    分析结果模型类，对应数据库中的analysis_result表

    属性:
        id: 主键，自增
        cirrhosis: 肝硬化，浮点型
        age: 年龄，浮点型
        sex: 性别，浮点型
        cholesterol: 胆固醇，浮点型
        triglyceride: 甘油三酯，浮点型
        HDL: 高密度脂蛋白，浮点型
        LDL: 低密度脂蛋白，浮点型
        PathDiagNum: 病理诊断编号，浮点型
        BMI: 体重指数，浮点型
        ALT: 谷丙转氨酶，浮点型
        AST: 谷草转氨酶，浮点型
        glucose: 血糖，浮点型
        created_at: 创建时间，自动记录当前时间
    """
    __tablename__ = 'analysis_result'  # 指定表名
    
    id = db.Column(db.Integer, primary_key=True)  # 主键
    cirrhosis = db.Column(db.Float)      # 肝硬化，浮点型
    age = db.Column(db.Float)            # 年龄，浮点型
    sex = db.Column(db.Float)            # 性别，浮点型
    cholesterol = db.Column(db.Float)    # 胆固醇，浮点型
    triglyceride = db.Column(db.Float)   # 甘油三酯，浮点型
    HDL = db.Column(db.Float)            # 高密度脂蛋白，浮点型
    LDL = db.Column(db.Float)            # 低密度脂蛋白，浮点型
    PathDiagNum = db.Column(db.Float)    # 病理诊断编号，浮点型
    BMI = db.Column(db.Float)            # 体重指数，浮点型
    ALT = db.Column(db.Float)            # 谷丙转氨酶，浮点型
    AST = db.Column(db.Float)            # 谷草转氨酶，浮点型
    glucose = db.Column(db.Float)        # 血糖，浮点型
    # 强制存储北京时间（UTC+8）
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(hours=8)
    )
    
    def __repr__(self):
        """返回分析结果对象的字符串表示"""
        return f'<Analysis_result id={self.id}>'
    
    
class AgeGroupAvg(db.Model):
    __tablename__ = 'age_group_avg'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True) # 主键，自动递增
    field_name = db.Column(db.String(50), unique=True, nullable=False) # 字段名称，非空且唯一
    age_0_9 = db.Column(db.Float)    # 0-9岁年龄段平均值
    age_10_19 = db.Column(db.Float)  # 10-19岁年龄段平均值
    age_20_29 = db.Column(db.Float)  # 20-29岁年龄段平均值
    age_30_39 = db.Column(db.Float)  # 30-39岁年龄段平均值
    age_40_49 = db.Column(db.Float)  # 40-49岁年龄段平均值
    age_50_59 = db.Column(db.Float)  # 50-59岁年龄段平均值
    age_60_69 = db.Column(db.Float)  # 60-69岁年龄段平均值
    age_70_79 = db.Column(db.Float)  # 70-79岁年龄段平均值
    age_80_plus = db.Column(db.Float) # 80岁及以上年龄段平均值
    # 强制存储北京时间（UTC+8）
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(hours=8)
    )

    def __repr__(self):
        return f'<AgeGroupAvg {self.field_name}>'
