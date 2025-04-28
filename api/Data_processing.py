from flask import request, jsonify
from service.analyse import AnalyseService  # 导入分析服务类

def data_processing():  # 定义数据处理接口
    try:
        analyse_service = AnalyseService()  # 创建分析服务实例
        average_age = analyse_service.average_encrypted_data('age')  # 计算age字段的平均值
        return jsonify({'code': 200, 'data': average_age})  # 返回平均值
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'服务器内部错误: {str(e)}'})  # 返回错误信息
