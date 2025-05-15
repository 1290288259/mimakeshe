
# 修改导入语句
from db_config import db  # 直接从db_config导入数据库对象
from models import Shuju  # 导入模型

def calculate_averages():
        """
        计算shuju表中所有数值字段的平均值(排除id、sex、cirrhosis和PathDiagNum字段)
        返回:
            包含各字段平均值的字典
        """
        # 需要计算平均值的字段列表
        fields_to_calculate = [
            'age', 'cholesterol', 'triglyceride', 
            'HDL', 'LDL', 'BMI', 'ALT', 'AST', 'glucose'
        ]
        
        averages = {}  # 存储计算结果的字典
        
        try:
            # 查询记录总数
            record_count = Shuju.query.count()
            if record_count == 0:
                print("警告: 表中没有数据记录")
                return averages
                
            # 计算每个字段的平均值
            for field in fields_to_calculate:
                # 查询该字段的总和
                total = db.session.query(
                    db.func.sum(getattr(Shuju, field))
                ).scalar()
                
                # 计算平均值
                avg = total / record_count
                averages[field] = avg
                
                print(f"字段 {field} 平均值计算完成: {avg:.2f}")
                
            return averages
            
        except Exception as e:
            print(f"计算平均值时出错: {str(e)}")
            return {}

