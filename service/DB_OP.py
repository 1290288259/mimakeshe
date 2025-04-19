import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

try:
    # 读取CSV文件
    csv_path = 'E:\\桌面\\zuoye\\密码学课设\\Medical_data_analysis_system\\static\\hepatitis_C_EHRs_Japan.csv'
    df = pd.read_csv(csv_path)

    # 添加自增id列
    df.insert(0, 'id', range(1, len(df) + 1))

    # 创建数据库连接
    engine = create_engine('mysql://root:123456@localhost/keshe')

    # 存入MySQL
    df.to_sql('shuju', con=engine, if_exists='append', index=False)
    print("数据成功导入数据库")
except FileNotFoundError:
    print(f"错误：CSV文件未找到，路径为 {csv_path}")
except SQLAlchemyError as e:
    print(f"数据库操作失败: {e}")
except Exception as e:
    print(f"发生未知错误: {e}")