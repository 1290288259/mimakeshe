import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from Paillier import PaillierEncryptor
def import_csv_to_mysql():
    try:
        # 读取CSV文件
        csv_path = 'E:\\桌面\\zuoye\\密码学课设\\Medical_data_analysis_system\\static\\hepatitis_C_EHRs_Japan.csv'
        df = pd.read_csv(csv_path)
        print(f"CSV文件总行数: {len(df)}")  # 添加数据量检查
        
        # 添加自增id列
        df.insert(0, 'id', range(1, len(df) + 1))
        
        # 创建数据库连接
        engine = create_engine('mysql://root:123456@localhost/keshe')
        
        # 分批导入设置
        chunksize = 500  # 每批处理500条
        total_rows = len(df)
        
        # 清空表（如果存在）
        with engine.connect() as conn:
            from sqlalchemy import text  # 新增导入
            conn.execute(text('DROP TABLE IF EXISTS shuju'))
        
        # 分批导入数据
        for i in range(0, total_rows, chunksize):
            batch = df.iloc[i:i+chunksize].copy()
            
            # 定义需要保持为浮点型的列
            float_columns = ['BMI', 'LDL']
            
            # 转换数据类型
            for col in batch.columns:
                if col in float_columns:
                    batch[col] = pd.to_numeric(batch[col], errors='coerce').astype(float)
                elif col != 'id':
                    batch[col] = pd.to_numeric(batch[col], errors='coerce').fillna(0).astype(int)
            
            # 存入MySQL
            from sqlalchemy import Float, Integer
            dtype = {
                'BMI': Float,
                'LDL': Float
            }
            batch.to_sql('shuju',
                        con=engine,
                        if_exists='append',
                        index=False,
                        dtype=dtype)
            print(f"已导入 {min(i+chunksize, total_rows)}/{total_rows} 条记录")
        
        print("数据成功导入MySQL数据库，表名: shuju")
        print(f"共导入 {len(df)} 条记录")
        # 导入加密模块
        encryptor = PaillierEncryptor()
        
        # 从shuju表读取总行数
        total_rows = pd.read_sql('SELECT COUNT(*) FROM shuju', con=engine).iloc[0,0]
        print(f"开始加密处理 {total_rows} 条数据...")
        
        # 清空目标表
        with engine.connect() as conn:
            conn.execute(text('DROP TABLE IF EXISTS shuju2'))
        
        # 分批处理
        batch_size = 200  # 加密批次大小
        for offset in range(0, total_rows, batch_size):
            # 读取批次数据
            query = f'SELECT * FROM shuju LIMIT {batch_size} OFFSET {offset}'
            df_batch = pd.read_sql(query, con=engine)
            
            # 创建空DataFrame用于存储加密结果
            encrypted_batch = pd.DataFrame()
            encrypted_batch['id'] = df_batch['id']  # 保留ID列
            
            # 定义需要乘以10的列
            multiply_columns = ['BMI', 'LDL']
            
            # 加密并立即存储
            for col in df_batch.columns:
                if col != 'id':
                    if col in multiply_columns:
                        encrypted_batch[col] = df_batch[col].apply(lambda x: str(encryptor.encrypt(int(x*10)).ciphertext()))
                    else:
                        encrypted_batch[col] = df_batch[col].apply(lambda x: str(encryptor.encrypt(int(x)).ciphertext()))
            
            # 立即存储加密后的批次数据
            encrypted_batch.to_sql('shuju2', 
                                con=engine,
                                if_exists='append',
                                index=False)
            
            print(f"已加密处理 {min(offset+batch_size, total_rows)}/{total_rows} 条数据")
        
        print("数据加密完成并保存到shuju2表")
        
    except FileNotFoundError:
        print(f"错误：CSV文件未找到，路径为 {csv_path}")
    except SQLAlchemyError as e:
        print(f"数据库操作失败: {e}")
    except Exception as e:
        print(f"发生未知错误: {e}")
        
       

if __name__ == "__main__":
    import_csv_to_mysql()