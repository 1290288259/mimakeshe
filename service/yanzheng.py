
# 修改导入语句
from db_config import db  # 直接从db_config导入数据库对象
from models import Shuju  # 导入模型

def calculate_averages(group_id=1):
        """
        计算shuju表中所有数值字段的平均值(排除id、sex、cirrhosis和PathDiagNum字段)
        参数:
            group_id: 分组ID，默认为1
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
            record_count = Shuju.query.filter_by(group_id=group_id).count()
            if record_count == 0:
                print(f"警告: 分组 {group_id} 表中没有数据记录")
                return averages
                
            # 计算每个字段的平均值
            for field in fields_to_calculate:
                # 查询该字段的总和
                total = db.session.query(
                    db.func.sum(getattr(Shuju, field))
                ).filter_by(group_id=group_id).scalar()
                
                # 计算平均值
                if total is not None:
                    avg = total / record_count
                    averages[field] = avg
                    print(f"字段 {field} 平均值计算完成: {avg:.2f}")
                else:
                    averages[field] = 0
                
            return averages
            
        except Exception as e:
            print(f"计算平均值时出错: {str(e)}")
            return {}

