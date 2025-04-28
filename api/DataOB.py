# 导入必要的模块
from service.analyse import AnalyseService
from flask import jsonify, current_app
import threading
from concurrent.futures import ThreadPoolExecutor

def get_averages():
    """
    获取各字段加密数据的平均值(多线程版本)
    返回:
        JSON响应: 包含状态码、消息和各字段平均值数据
    """
    try:
        # 获取当前应用上下文
        app = current_app._get_current_object()
        
        # 创建分析服务实例
        service = AnalyseService()
        
        # 定义需要计算平均值的字段列表
        numeric_fields = ['cirrhosis', 'age', 'cholesterol',
                         'triglyceride', 'HDL', 'LDL', 'BMI',
                         'ALT', 'AST', 'glucose']
        
        # 初始化线程安全的结果字典
        results = {}
        lock = threading.Lock()

        def calculate_avg(field):
            # 在每个线程中创建新的应用上下文
            with app.app_context():
                try:
                    # 调用分析服务的平均值计算方法
                    avg = service.average_encrypted_data(field)
                    # 使用锁保证线程安全
                    with lock:
                        results[field] = avg
                except Exception as e:
                    print(f"计算{field}平均值时出错: {str(e)}")
        
        # 使用线程池创建线程(最大10个并发线程)
        with ThreadPoolExecutor(max_workers=10) as executor:
            # 为每个字段提交计算任务
            executor.map(calculate_avg, numeric_fields)
        
        # 返回成功的JSON响应
        return jsonify({
            'code': 200,
            'msg': '平均值计算成功',
            'data': results
        })
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'平均值计算失败: {str(e)}'
        })