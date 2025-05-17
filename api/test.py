from flask import jsonify  # 导入jsonify用于返回JSON格式响应
from service.Paillier import PaillierEncryptor  # 导入Paillier加密器
from service.analyse import AnalyseService  # 导入分析服务
import random  # 导入随机数模块
import time  # 导入时间模块
from config import FLOAT_PRECISION  # 导入浮点精度配置

# 创建一个全局变量用于收集所有测试结果
test_results = []  # 初始化测试结果列表

# 创建一个全局变量用于存储测试数据集
test_datasets = {  # 初始化测试数据集字典
    "平均值计算": [],  # 平均值计算测试数据集
    "完全匹配": [],  # 完全匹配测试数据集
    "模糊匹配": []  # 模糊匹配测试数据集
}

def run_average_calculation_test():
    """
    测试加密数据和明文数据计算平均值的一致性
    """
    # 清空之前的测试结果
    global test_results, test_datasets
    test_results = []
    test_datasets["平均值计算"] = []  # 清空平均值计算测试数据集
    
    # 创建加密器实例
    encryptor = PaillierEncryptor()  # 初始化加密器
    
    # 创建分析服务实例
    analyse_service = AnalyseService()  # 初始化分析服务
    
    # 测试用例1：整数列表
    int_list = [10, 20, 30, 40, 50]  # 创建整数列表
    test_datasets["平均值计算"].append({  # 添加到测试数据集
        "名称": "整数列表平均值测试",
        "数据": int_list,
        "类型": "整数"
    })
    test_average(encryptor, analyse_service, int_list, is_float=False, test_name="整数列表平均值测试")  # 测试整数列表的平均值计算
    
    # 测试用例2：浮点数列表
    float_list = [10.5, 20.5, 30.5, 40.5, 50.5]  # 创建浮点数列表
    test_datasets["平均值计算"].append({  # 添加到测试数据集
        "名称": "浮点数列表平均值测试",
        "数据": float_list,
        "类型": "浮点数"
    })
    test_average(encryptor, analyse_service, float_list, is_float=True, test_name="浮点数列表平均值测试")  # 测试浮点数列表的平均值计算，标记为浮点数
    
    # 测试用例3：大量随机数据
    random_list = [random.randint(1, 1000) for _ in range(100)]  # 创建100个1-1000之间的随机整数
    test_datasets["平均值计算"].append({  # 添加到测试数据集
        "名称": "大量随机数据平均值测试",
        "数据": random_list,
        "类型": "整数"
    })
    test_average(encryptor, analyse_service, random_list, test_name="大量随机数据平均值测试")  # 测试随机数列表的平均值计算
    
    # 测试用例4：包含负数的列表
    mixed_list = [-50, -25, 0, 25, 50]  # 创建包含负数的列表
    test_datasets["平均值计算"].append({  # 添加到测试数据集
        "名称": "包含负数的列表平均值测试",
        "数据": mixed_list,
        "类型": "整数"
    })
    test_average(encryptor, analyse_service, mixed_list, test_name="包含负数的列表平均值测试")  # 测试包含负数的列表的平均值计算
    
    # 测试用例5：大数值列表
    large_list = [10000, 20000, 30000, 40000, 50000]  # 创建大数值列表
    test_datasets["平均值计算"].append({  # 添加到测试数据集
        "名称": "大数值列表平均值测试",
        "数据": large_list,
        "类型": "整数"
    })
    test_average(encryptor, analyse_service, large_list, test_name="大数值列表平均值测试")  # 测试大数值列表的平均值计算
    
    # 返回测试结果
    return test_results

def test_average(encryptor, analyse_service, data_list, is_float=False, test_name="未命名测试"):
    """
    测试指定数据列表的加密平均值和明文平均值是否一致
    
    参数:
        encryptor: Paillier加密器实例
        analyse_service: 分析服务实例
        data_list: 要测试的数据列表
        is_float: 是否为浮点数列表，默认为False
        test_name: 测试名称，用于结果收集
    """
    # 初始化结果字典
    result = {
        "测试名称": test_name,  # 测试名称
        "测试类型": "平均值计算",  # 测试类型
        "数据类型": "浮点数" if is_float else "整数",  # 数据类型
        "数据量": len(data_list),  # 数据量
        "明文数据": data_list[:10] + (["..."] if len(data_list) > 10 else []),  # 明文数据（限制显示前10个）
        "明文平均值": None,  # 明文平均值
        "加密平均值": None,  # 加密平均值
        "误差": None,  # 误差
        "加密耗时(秒)": None,  # 加密耗时
        "计算耗时(秒)": None,  # 计算耗时
        "结果": None  # 测试结果
    }
    
    # 计算明文平均值
    plaintext_avg = sum(data_list) / len(data_list)  # 计算明文平均值
    result["明文平均值"] = plaintext_avg  # 记录明文平均值
    
    # 加密数据
    start_time = time.time()  # 记录开始时间
    
    if is_float:
        # 浮点数需要先乘以精度因子，转为整数再加密
        encrypted_data = [str(encryptor.encrypt(int(value * FLOAT_PRECISION)).ciphertext()) for value in data_list]
    else:
        # 整数直接加密
        encrypted_data = [str(encryptor.encrypt(value).ciphertext()) for value in data_list]
    
    encryption_time = time.time() - start_time  # 计算加密耗时
    result["加密耗时(秒)"] = round(encryption_time, 4)  # 记录加密耗时
    
    # 使用加密数据计算平均值
    start_time = time.time()  # 记录开始时间
    encrypted_avg = analyse_service.average_encrypted_data(encrypted_data)  # 计算加密数据的平均值
    
    # 如果是浮点数，需要除以精度因子
    if is_float:
        encrypted_avg = encrypted_avg / FLOAT_PRECISION
    
    calculation_time = time.time() - start_time  # 计算平均值计算耗时
    result["计算耗时(秒)"] = round(calculation_time, 4)  # 记录计算耗时
    result["加密平均值"] = encrypted_avg  # 记录加密平均值
    
    # 比较结果
    error = abs(encrypted_avg - plaintext_avg)  # 计算误差
    result["误差"] = error  # 记录误差
    is_consistent = error < 0.0001  # 判断结果是否一致
    result["结果"] = "一致" if is_consistent else "不一致"  # 记录测试结果
    
    # 将结果添加到全局结果列表
    test_results.append(result)  # 添加结果到全局列表

def run_exact_match_test():
    """
    测试隐私保护的完全匹配功能
    """
    # 清空之前的测试结果
    global test_results, test_datasets
    test_results = []
    test_datasets["完全匹配"] = []  # 清空完全匹配测试数据集
    
    # 创建加密器实例
    encryptor = PaillierEncryptor()  # 初始化加密器
    
    # 创建分析服务实例
    analyse_service = AnalyseService()  # 初始化分析服务
    
    # 定义多组测试用例
    test_cases = [
        {
            "测试名称": "性别字段完全匹配测试",  # 测试名称
            "数据类型": "整数",  # 数据类型
            "目标值": 1,  # 目标值（假设为男性，编码为1）
            "测试数据": [1, 0, 1, 0, 1, 1, 0, 1, 0, 1]  # 测试数据（模拟性别字段，1表示男性，0表示女性）
        },
        {
            "测试名称": "血型字段完全匹配测试",  # 测试名称
            "数据类型": "整数",  # 数据类型
            "目标值": 2,  # 目标值（假设为B型血，编码为2）
            "测试数据": [1, 2, 3, 4, 2, 1, 2, 3, 2, 4, 1, 2]  # 测试数据（模拟血型字段，1-4分别表示A、B、AB、O型血）
        },
        {
            "测试名称": "吸烟状态完全匹配测试",  # 测试名称
            "数据类型": "整数",  # 数据类型
            "目标值": 0,  # 目标值（假设为不吸烟，编码为0）
            "测试数据": [0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1]  # 测试数据（模拟吸烟状态，0表示不吸烟，1表示吸烟）
        }
    ]
    
    # 将测试用例添加到测试数据集
    for test_case in test_cases:
        test_datasets["完全匹配"].append({
            "名称": test_case["测试名称"],
            "数据": test_case["测试数据"],
            "目标值": test_case["目标值"],
            "类型": test_case["数据类型"]
        })
    
    # 循环测试每个测试用例
    for test_case in test_cases:
        # 获取目标值和测试数据
        target_value = test_case["目标值"]  # 目标值
        test_data = test_case["测试数据"]  # 测试数据
        
        # 初始化结果字典
        result = {
            "测试名称": test_case["测试名称"],  # 测试名称
            "测试类型": "完全匹配",  # 测试类型
            "数据类型": test_case["数据类型"],  # 数据类型
            "数据量": len(test_data),  # 数据量
            "目标值": target_value,  # 目标值
            "测试数据": test_data,  # 测试数据
            "明文匹配百分比": None,  # 明文匹配百分比
            "加密匹配百分比": None,  # 加密匹配百分比
            "误差": None,  # 误差
            "计算耗时(秒)": None,  # 计算耗时
            "结果": None  # 测试结果
        }
        
        # 加密数据
        encrypted_target = str(encryptor.encrypt(target_value).ciphertext())  # 加密目标值
        encrypted_data = [str(encryptor.encrypt(value).ciphertext()) for value in test_data]  # 加密测试数据
        
        # 计算明文匹配百分比（手动计算）
        match_count = sum(1 for value in test_data if value == target_value)  # 计算匹配数量
        plaintext_percentage = (match_count / len(test_data)) * 100  # 计算明文匹配百分比
        result["明文匹配百分比"] = plaintext_percentage  # 记录明文匹配百分比
        
        # 使用隐私保护的完全匹配方法计算
        start_time = time.time()  # 记录开始时间
        encrypted_percentage = analyse_service.privacy_preserving_exact_match(encrypted_target, encrypted_data)  # 计算加密数据的匹配百分比
        calculation_time = time.time() - start_time  # 计算匹配百分比计算耗时
        result["计算耗时(秒)"] = round(calculation_time, 4)  # 记录计算耗时
        result["加密匹配百分比"] = encrypted_percentage  # 记录加密匹配百分比
        
        # 比较结果
        error = abs(encrypted_percentage - plaintext_percentage)  # 计算误差
        result["误差"] = error  # 记录误差
        is_consistent = error < 0.0001  # 判断结果是否一致
        result["结果"] = "一致" if is_consistent else "不一致"  # 记录测试结果
        
        # 将结果添加到全局结果列表
        test_results.append(result)  # 添加结果到全局列表
    
    # 返回测试结果
    return test_results

def run_fuzzy_match_test():
    """
    测试隐私保护的模糊匹配功能
    """
    # 清空之前的测试结果
    global test_results, test_datasets
    test_results = []
    
    # 创建加密器实例
    encryptor = PaillierEncryptor()  # 初始化加密器
    
    # 创建分析服务实例
    analyse_service = AnalyseService()  # 初始化分析服务
    
    # 定义多组测试用例（浮点数）
    test_cases = [
        {
            "测试名称": "BMI字段模糊匹配测试1",  # 测试名称
            "数据类型": "浮点数",  # 数据类型
            "目标值": 23.5,  # 目标值（正常BMI）
            "测试数据": [22.3, 23.8, 24.5, 21.0, 23.4, 25.6, 23.6, 26.7, 23.3, 22.8]  # 测试数据（模拟BMI字段）
        },
        {
            "测试名称": "BMI字段模糊匹配测试2",  # 测试名称
            "数据类型": "浮点数",  # 数据类型
            "目标值": 18.5,  # 目标值（偏瘦BMI）
            "测试数据": [17.8, 18.2, 19.0, 18.7, 16.5, 18.4, 20.1, 18.6, 17.9, 18.3]  # 测试数据（模拟BMI字段）
        },
        {
            "测试名称": "BMI字段模糊匹配测试3",  # 测试名称
            "数据类型": "浮点数",  # 数据类型
            "目标值": 30.0,  # 目标值（肥胖BMI）
            "测试数据": [28.5, 31.2, 29.8, 32.5, 30.1, 29.5, 33.0, 30.2, 27.8, 31.5]  # 测试数据（模拟BMI字段）
        },
        {
            "测试名称": "胆固醇模糊匹配测试",  # 测试名称
            "数据类型": "浮点数",  # 数据类型
            "目标值": 5.2,  # 目标值（正常胆固醇）
            "测试数据": [4.8, 5.3, 5.5, 4.9, 5.1, 5.8, 5.0, 6.2, 5.4, 4.7]  # 测试数据（模拟胆固醇字段）
        },
        {
            "测试名称": "血糖模糊匹配测试",  # 测试名称
            "数据类型": "浮点数",  # 数据类型
            "目标值": 6.1,  # 目标值（血糖）
            "测试数据": [5.8, 6.3, 6.0, 5.9, 6.2, 6.5, 5.7, 6.4, 6.1, 5.6, 6.0, 6.2]  # 测试数据（模拟血糖字段）
        }
    ]
    
    # 将测试用例添加到测试数据集
    for test_case in test_cases:
        test_datasets["模糊匹配"].append({
            "名称": test_case["测试名称"],
            "数据": test_case["测试数据"],
            "目标值": test_case["目标值"],
            "类型": test_case["数据类型"]
        })
    
    # 循环测试每个测试用例
    for test_case in test_cases:
        # 获取目标值和测试数据
        target_value = test_case["目标值"]  # 目标值
        test_data = test_case["测试数据"]  # 测试数据
        
        # 初始化结果字典
        result = {
            "测试名称": test_case["测试名称"],  # 测试名称
            "测试类型": "模糊匹配",  # 测试类型
            "数据类型": test_case["数据类型"],  # 数据类型
            "数据量": len(test_data),  # 数据量
            "目标值": target_value,  # 目标值
            "测试数据": test_data,  # 测试数据
            "明文匹配百分比": None,  # 明文匹配百分比
            "加密匹配百分比": None,  # 加密匹配百分比
            "误差": None,  # 误差
            "计算耗时(秒)": None,  # 计算耗时
            "结果": None  # 测试结果
        }
        
        # 加密数据（注意：浮点数需要先乘以精度因子）
        encrypted_target = str(encryptor.encrypt(int(target_value * FLOAT_PRECISION)).ciphertext())  # 加密目标值
        encrypted_data = [str(encryptor.encrypt(int(value * FLOAT_PRECISION)).ciphertext()) for value in test_data]  # 加密测试数据
        
        # 计算明文模糊匹配百分比（手动计算，偏差在5%范围内）
        match_count = 0  # 初始化匹配计数
        for value in test_data:  # 遍历测试数据
            if target_value != 0:  # 避免除以零
                deviation_percentage = abs((value - target_value) / target_value) * 100  # 计算偏差百分比
                if deviation_percentage <= 5:  # 如果偏差在5%范围内
                    match_count += 1  # 匹配计数加1
        
        plaintext_percentage = (match_count / len(test_data)) * 100  # 计算明文匹配百分比
        result["明文匹配百分比"] = plaintext_percentage  # 记录明文匹配百分比
        
        # 使用隐私保护的模糊匹配方法计算
        start_time = time.time()  # 记录开始时间
        encrypted_percentage = analyse_service.privacy_preserving_fuzzy_match(encrypted_target, encrypted_data, FLOAT_PRECISION)  # 计算加密数据的模糊匹配百分比
        calculation_time = time.time() - start_time  # 计算模糊匹配百分比计算耗时
        result["计算耗时(秒)"] = round(calculation_time, 4)  # 记录计算耗时
        result["加密匹配百分比"] = encrypted_percentage  # 记录加密匹配百分比
        
        # 比较结果
        error = abs(encrypted_percentage - plaintext_percentage)  # 计算误差
        result["误差"] = error  # 记录误差
        is_consistent = error < 0.0001  # 判断结果是否一致
        result["结果"] = "一致" if is_consistent else "不一致"  # 记录测试结果
        
        # 将结果添加到全局结果列表
        test_results.append(result)  # 添加结果到全局列表
    
    # 返回测试结果
    return test_results

def generate_test_summary(results):
    """
    生成测试结果汇总
    """
    # 按测试类型分组
    avg_tests = [r for r in results if r["测试类型"] == "平均值计算"]  # 平均值计算测试
    exact_match_tests = [r for r in results if r["测试类型"] == "完全匹配"]  # 完全匹配测试
    fuzzy_match_tests = [r for r in results if r["测试类型"] == "模糊匹配"]  # 模糊匹配测试
    
    # 计算成功率
    success_count = sum(1 for r in results if r["结果"] == "一致")  # 计算成功测试数量
    total_count = len(results)  # 计算总测试数量
    success_rate = (success_count / total_count * 100) if total_count > 0 else 0  # 计算成功率
    
    # 构建汇总信息
    summary = {
        "总测试数": total_count,  # 总测试数
        "成功测试数": success_count,  # 成功测试数
        "失败测试数": total_count - success_count,  # 失败测试数
        "成功率": round(success_rate, 2),  # 成功率
        "平均值计算测试数": len(avg_tests),  # 平均值计算测试数
        "完全匹配测试数": len(exact_match_tests),  # 完全匹配测试数
        "模糊匹配测试数": len(fuzzy_match_tests)  # 模糊匹配测试数
    }
    
    return summary

# API接口函数
def run_all_tests():
    """
    运行所有测试并返回结果
    """
    # 清空之前的测试结果
    global test_results, test_datasets
    test_results = []
    
    # 运行平均值计算测试
    avg_results = run_average_calculation_test()
    
    # 运行完全匹配测试
    exact_match_results = run_exact_match_test()
    
    # 运行模糊匹配测试
    fuzzy_match_results = run_fuzzy_match_test()
    
    # 合并所有测试结果
    all_results = avg_results + exact_match_results + fuzzy_match_results
    
    # 生成测试汇总
    summary = generate_test_summary(all_results)
    
    # 返回结果
    return jsonify({
        'code': 200,
        'msg': '测试执行成功',
        'data': {
            '测试结果': all_results,
            '测试汇总': summary,
            '测试数据集': test_datasets  # 添加测试数据集到响应
        }
    })

def run_average_test():
    """
    仅运行平均值计算测试
    """
    results = run_average_calculation_test()
    summary = generate_test_summary(results)
    
    return jsonify({
        'code': 200,
        'msg': '平均值计算测试执行成功',
        'data': {
            '测试结果': results,
            '测试汇总': summary,
            '测试数据集': {"平均值计算": test_datasets["平均值计算"]}  # 添加平均值计算测试数据集到响应
        }
    })

def run_exact_match_test_api():
    """
    仅运行完全匹配测试
    """
    results = run_exact_match_test()
    summary = generate_test_summary(results)
    
    return jsonify({
        'code': 200,
        'msg': '完全匹配测试执行成功',
        'data': {
            '测试结果': results,
            '测试汇总': summary,
            '测试数据集': {"完全匹配": test_datasets["完全匹配"]}  # 添加完全匹配测试数据集到响应
        }
    })

def run_fuzzy_match_test_api():
    """
    仅运行模糊匹配测试
    """
    results = run_fuzzy_match_test()
    summary = generate_test_summary(results)
    
    return jsonify({
        'code': 200,
        'msg': '模糊匹配测试执行成功',
        'data': {
            '测试结果': results,
            '测试汇总': summary,
            '测试数据集': {"模糊匹配": test_datasets["模糊匹配"]}  # 添加模糊匹配测试数据集到响应
        }
    })