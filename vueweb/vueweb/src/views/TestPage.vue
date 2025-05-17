<template>
  <div class="test-container">
    <!-- 页面标题 -->
    <h2 class="page-title">系统测试页面</h2>
    
    <!-- 测试类型选择按钮组 -->
    <div class="test-buttons">
      <el-button-group>
        <el-button 
          type="primary" 
          :plain="currentTest !== 'all'" 
          @click="selectTest('all')"
          :loading="loading && currentTest === 'all'">
          全部测试
        </el-button>
        <el-button 
          type="primary" 
          :plain="currentTest !== 'average'" 
          @click="selectTest('average')"
          :loading="loading && currentTest === 'average'">
          平均值计算测试
        </el-button>
        <el-button 
          type="primary" 
          :plain="currentTest !== 'exact_match'" 
          @click="selectTest('exact_match')"
          :loading="loading && currentTest === 'exact_match'">
          完全匹配测试
        </el-button>
        <el-button 
          type="primary" 
          :plain="currentTest !== 'fuzzy_match'" 
          @click="selectTest('fuzzy_match')"
          :loading="loading && currentTest === 'fuzzy_match'">
          模糊匹配测试
        </el-button>
      </el-button-group>
    </div>
    
    <!-- 测试结果汇总卡片 -->
    <el-card v-if="testSummary" class="summary-card">
      <template #header>
        <div class="card-header">
          <span>测试结果汇总</span>
          <el-tag :type="testSummary['成功率'] === 100 ? 'success' : 'warning'" effect="dark">
            成功率: {{ testSummary['成功率'] }}%
          </el-tag>
        </div>
      </template>
      <el-descriptions :column="4" border>
        <el-descriptions-item label="总测试数">{{ testSummary['总测试数'] }}</el-descriptions-item>
        <el-descriptions-item label="成功测试数">{{ testSummary['成功测试数'] }}</el-descriptions-item>
        <el-descriptions-item label="失败测试数">{{ testSummary['失败测试数'] }}</el-descriptions-item>
        <el-descriptions-item label="成功率">{{ testSummary['成功率'] }}%</el-descriptions-item>
        <el-descriptions-item label="平均值计算测试数">{{ testSummary['平均值计算测试数'] }}</el-descriptions-item>
        <el-descriptions-item label="完全匹配测试数">{{ testSummary['完全匹配测试数'] }}</el-descriptions-item>
        <el-descriptions-item label="模糊匹配测试数">{{ testSummary['模糊匹配测试数'] }}</el-descriptions-item>
      </el-descriptions>
    </el-card>
    
    <!-- 测试结果详情 -->
    <div v-if="testResults.length > 0" class="test-results">
      <h3>测试详情</h3>
      
      <!-- 平均值计算测试结果 -->
      <div v-if="hasTestType('平均值计算')" class="test-section">
        <h4>平均值计算测试</h4>
        <el-table :data="getTestsByType('平均值计算')" stripe border>
          <el-table-column prop="测试名称" label="测试名称" width="180"></el-table-column>
          <el-table-column prop="数据类型" label="数据类型" width="100"></el-table-column>
          <el-table-column prop="数据量" label="数据量" width="100"></el-table-column>
          <el-table-column prop="明文平均值" label="明文平均值" width="120"></el-table-column>
          <el-table-column prop="加密平均值" label="加密平均值" width="120"></el-table-column>
          <el-table-column prop="误差" label="误差" width="120"></el-table-column>
          <el-table-column prop="加密耗时(秒)" label="加密耗时(秒)" width="120"></el-table-column>
          <el-table-column prop="计算耗时(秒)" label="计算耗时(秒)" width="120"></el-table-column>
          <el-table-column prop="结果" label="结果" width="100">
            <template #default="scope">
              <el-tag :type="scope.row.结果 === '一致' ? 'success' : 'danger'">
                {{ scope.row.结果 }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
      </div>
      
      <!-- 完全匹配测试结果 -->
      <div v-if="hasTestType('完全匹配')" class="test-section">
        <h4>完全匹配测试</h4>
        <el-table :data="getTestsByType('完全匹配')" stripe border>
          <el-table-column prop="测试名称" label="测试名称" width="180"></el-table-column>
          <el-table-column prop="数据类型" label="数据类型" width="100"></el-table-column>
          <el-table-column prop="数据量" label="数据量" width="100"></el-table-column>
          <el-table-column prop="目标值" label="目标值" width="100"></el-table-column>
          <el-table-column prop="明文匹配百分比" label="明文匹配百分比" width="150"></el-table-column>
          <el-table-column prop="加密匹配百分比" label="加密匹配百分比" width="150"></el-table-column>
          <el-table-column prop="误差" label="误差" width="120"></el-table-column>
          <el-table-column prop="计算耗时(秒)" label="计算耗时(秒)" width="120"></el-table-column>
          <el-table-column prop="结果" label="结果" width="100">
            <template #default="scope">
              <el-tag :type="scope.row.结果 === '一致' ? 'success' : 'danger'">
                {{ scope.row.结果 }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
      </div>
      
      <!-- 模糊匹配测试结果 -->
      <div v-if="hasTestType('模糊匹配')" class="test-section">
        <h4>模糊匹配测试</h4>
        <el-table :data="getTestsByType('模糊匹配')" stripe border>
          <el-table-column prop="测试名称" label="测试名称" width="180"></el-table-column>
          <el-table-column prop="数据类型" label="数据类型" width="100"></el-table-column>
          <el-table-column prop="数据量" label="数据量" width="100"></el-table-column>
          <el-table-column prop="目标值" label="目标值" width="100"></el-table-column>
          <el-table-column prop="明文匹配百分比" label="明文匹配百分比" width="150"></el-table-column>
          <el-table-column prop="加密匹配百分比" label="加密匹配百分比" width="150"></el-table-column>
          <el-table-column prop="误差" label="误差" width="120"></el-table-column>
          <el-table-column prop="计算耗时(秒)" label="计算耗时(秒)" width="120"></el-table-column>
          <el-table-column prop="结果" label="结果" width="100">
            <template #default="scope">
              <el-tag :type="scope.row.结果 === '一致' ? 'success' : 'danger'">
                {{ scope.row.结果 }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
    
    <!-- 加载中提示 -->
    <div v-if="loading" class="loading-container">
      <el-icon class="is-loading"><Loading /></el-icon>
      <span>测试执行中，请稍候...</span>
    </div>
    
    <!-- 无数据提示 -->
    <el-empty v-if="!loading && testResults.length === 0" description="暂无测试数据，请选择测试类型并执行测试"></el-empty>
  </div>
</template>

<script>
// 引入axios用于发送HTTP请求
import axios from 'axios';
// 引入element-plus的消息提示组件
import { ElMessage } from 'element-plus';
// 引入Loading图标
import { Loading } from '@element-plus/icons-vue';

export default {
  name: 'TestPage', // 组件名称
  components: {
    Loading // 注册Loading图标组件
  },
  data() {
    return {
      // 当前选择的测试类型
      currentTest: '', 
      // 测试结果列表
      testResults: [],
      // 测试结果汇总
      testSummary: null,
      // 加载状态
      loading: false
    };
  },
  methods: {
    // 选择测试类型并执行测试
    selectTest(testType) {
      // 设置当前测试类型
      this.currentTest = testType;
      // 执行测试
      this.runTest(testType);
    },
    
    // 执行测试
    async runTest(testType) {
      // 设置加载状态
      this.loading = true;
      
      try {
        // 根据测试类型选择不同的API接口
        const apiUrl = `/api/test/${testType}`;
        
        // 发送GET请求到后端接口
        const response = await axios.get(apiUrl);
        
        // 处理响应数据
        if (response.data.code === 200) {
          // 更新测试结果和汇总
          this.testResults = response.data.data['测试结果'];
          this.testSummary = response.data.data['测试汇总'];
          
          // 显示成功消息
          ElMessage.success(response.data.msg || '测试执行成功');
        } else {
          // 显示错误信息
          ElMessage.error(response.data.msg || '测试执行失败');
          this.testResults = [];
          this.testSummary = null;
        }
      } catch (error) {
        // 处理请求异常
        console.error('测试请求错误:', error);
        ElMessage.error('测试请求失败，请稍后重试');
        this.testResults = [];
        this.testSummary = null;
      } finally {
        // 无论成功失败都关闭加载状态
        this.loading = false;
      }
    },
    
    // 检查是否有指定类型的测试结果
    hasTestType(testType) {
      return this.testResults.some(test => test['测试类型'] === testType);
    },
    
    // 获取指定类型的测试结果
    getTestsByType(testType) {
      return this.testResults.filter(test => test['测试类型'] === testType);
    }
  }
};
</script>

<style scoped>
/* 外层容器样式 */
.test-container {
  padding: 20px;
  max-width: 1600px;
  margin: 0 auto;
}

/* 页面标题样式 */
.page-title {
  text-align: center;
  margin-bottom: 20px;
  color: #303133;
}

/* 测试按钮组样式 */
.test-buttons {
  display: flex;
  justify-content: center;
  margin-bottom: 30px;
}

/* 汇总卡片样式 */
.summary-card {
  margin-bottom: 30px;
}

/* 卡片头部样式 */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* 测试结果区域样式 */
.test-results {
  margin-top: 20px;
}

/* 测试类型区域样式 */
.test-section {
  margin-bottom: 30px;
}

/* 测试类型标题样式 */
.test-section h4 {
  margin-bottom: 15px;
  color: #409EFF;
}

/* 加载中提示样式 */
.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100px;
  color: #909399;
}

.loading-container .el-icon {
  margin-right: 10px;
  font-size: 20px;
}
</style>