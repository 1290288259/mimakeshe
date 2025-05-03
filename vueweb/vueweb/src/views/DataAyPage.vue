<template>
  <div class="data-analysis-container">
    <!-- 页面标题 -->
    <h2 class="page-title">数据分析结果</h2>
    
    <!-- 数据加载中提示 -->
    <div v-if="loading" class="loading-container">
      <el-icon class="is-loading"><Loading /></el-icon>
      <span>数据加载中...</span>
    </div>
    
    <!-- 无数据提示 -->
    <el-empty v-if="!loading && dataList.length === 0" description="暂无数据"></el-empty>
    
    <!-- 数据展示区域 -->
    <div v-if="!loading && dataList.length > 0" class="data-display">
      <div class="total-info">共找到 {{ total }} 条记录</div>
      
      <!-- 数据卡片循环 -->
      <el-card v-for="(item, index) in dataList" :key="index" class="data-card">
        <template #header>
          <div class="card-header">
            <span>数据ID: {{ item.original_data.id }}</span>
            <el-tag v-if="item.analysis_result" 
                   :type="getTagType(item.analysis_result.avg_similarity)"
                   effect="dark">
              平均相似度: {{ item.analysis_result.avg_similarity }}%
            </el-tag>
          </div>
        </template>
        
        <!-- 原始数据展示 -->
        <div class="data-section">
          <h3>原始数据</h3>
          <el-table :data="[item.original_data]" stripe border>
            <el-table-column prop="age" label="年龄" width="80"></el-table-column>
            <el-table-column prop="sex" label="性别" width="80">
              <template #default="scope">
                {{ scope.row.sex === 1 ? '男' : '女' }}
              </template>
            </el-table-column>
            <el-table-column prop="BMI" label="BMI" width="100"></el-table-column>
            <el-table-column prop="cholesterol" label="胆固醇"></el-table-column>
            <el-table-column prop="triglyceride" label="甘油三酯"></el-table-column>
            <el-table-column prop="HDL" label="高密度脂蛋白"></el-table-column>
            <el-table-column prop="LDL" label="低密度脂蛋白"></el-table-column>
            <el-table-column prop="ALT" label="谷丙转氨酶"></el-table-column>
            <el-table-column prop="AST" label="谷草转氨酶"></el-table-column>
            <el-table-column prop="glucose" label="血糖"></el-table-column>
            <el-table-column prop="cirrhosis" label="肝硬化" width="100">
              <template #default="scope">
                {{ scope.row.cirrhosis === 1 ? '是' : '否' }}
              </template>
            </el-table-column>
            <el-table-column prop="PathDiagNum" label="病理诊断编号"></el-table-column>
          </el-table>
        </div>
        
        <!-- 分析结果展示 -->
        <div v-if="item.analysis_result" class="data-section">
          <h3>相似度分析</h3>
          <el-table :data="[formatSimilarityData(item.analysis_result)]" stripe border>
            <el-table-column prop="age_similarity" label="年龄相似度"></el-table-column>
            <el-table-column prop="sex_similarity" label="性别相似度"></el-table-column>
            <el-table-column prop="BMI_similarity" label="BMI相似度"></el-table-column>
            <el-table-column prop="cholesterol_similarity" label="胆固醇相似度"></el-table-column>
            <el-table-column prop="triglyceride_similarity" label="甘油三酯相似度"></el-table-column>
            <el-table-column prop="HDL_similarity" label="高密度脂蛋白相似度"></el-table-column>
            <el-table-column prop="LDL_similarity" label="低密度脂蛋白相似度"></el-table-column>
            <el-table-column prop="ALT_similarity" label="谷丙转氨酶相似度"></el-table-column>
            <el-table-column prop="AST_similarity" label="谷草转氨酶相似度"></el-table-column>
            <el-table-column prop="glucose_similarity" label="血糖相似度"></el-table-column>
            <el-table-column prop="cirrhosis_similarity" label="肝硬化相似度"></el-table-column>
            <el-table-column prop="PathDiagNum_similarity" label="病理诊断编号相似度"></el-table-column>
          </el-table>
          
          <div class="analysis-time">分析时间: {{ item.analysis_result.created_at }}</div>
        </div>
        
        <!-- 无分析结果提示 -->
        <div v-else class="no-analysis">
          <el-alert
            title="该数据尚未进行相似度分析"
            type="info"
            :closable="false">
          </el-alert>
          <el-button 
            type="primary" 
            size="small" 
            class="analysis-btn"
            @click="runAnalysis(item.original_data.id)">
            立即分析
          </el-button>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import axios from 'axios'; // 导入axios用于发送HTTP请求
import { ElMessage, ElLoading } from 'element-plus'; // 导入Element Plus的消息提示组件
import { Loading } from '@element-plus/icons-vue'; // 导入Loading图标

export default {
  name: 'DataAyPage', // 组件名称
  components: {
    Loading // 注册Loading图标组件
  },
  data() {
    return {
      userId: '', // 用户ID
      dataList: [], // 存储从后端获取的数据列表
      total: 0, // 数据总数
      loading: false // 加载状态标志
    };
  },
  // 组件创建时自动执行
  created() {
    // 从sessionStorage获取用户信息
    this.getUserIdAndFetchData();
  },
  methods: {
    // 获取用户ID并加载数据
    getUserIdAndFetchData() {
      // 从sessionStorage获取用户信息
      const userString = sessionStorage.getItem('User');
      if (userString) {
        try {
          // 解析用户信息
          const user = JSON.parse(userString);
          // 设置用户ID
          this.userId = user.user_id;
          // 获取数据
          this.fetchData();
        } catch (error) {
          // 处理JSON解析错误
          console.error('解析用户信息失败:', error);
          ElMessage.error('获取用户信息失败，请重新登录');
        }
      } else {
        // 如果没有用户信息，提示用户登录
        ElMessage.warning('请先登录系统');
        // 可以选择跳转到登录页面
        // this.$router.push('/login');
      }
    },
    
    // 获取数据分析结果
    async fetchData() {
      // 验证用户ID是否存在
      if (!this.userId) {
        ElMessage.warning('未获取到用户ID，请重新登录');
        return;
      }
      
      // 显示加载状态
      this.loading = true;
      
      try {
        // 发送GET请求到后端接口
        const response = await axios.get(`/data/get_data_analysis_result?user_id=${this.userId}`);
        
        // 处理响应数据
        if (response.data.code === 200) {
          // 更新数据列表和总数
          this.dataList = response.data.data;
          this.total = response.data.total;
          ElMessage.success('数据加载成功');
        } else {
          // 显示错误信息
          ElMessage.error(response.data.msg || '数据加载失败');
          this.dataList = [];
          this.total = 0;
        }
      } catch (error) {
        // 处理请求异常
        console.error('请求错误:', error);
        ElMessage.error('请求失败，请稍后重试');
        this.dataList = [];
        this.total = 0;
      } finally {
        // 无论成功失败都关闭加载状态
        this.loading = false;
      }
    },
    
    // 运行数据分析
    async runAnalysis(dataId) {
      try {
        // 显示全屏加载
        ElLoading.service({
          fullscreen: true,
          text: '正在分析数据，请稍候...',
          background: 'rgba(0, 0, 0, 0.7)'
        });
        
        // 发送请求进行数据分析
        const response = await axios.get(`/data/privacy_intersection?data_id=${dataId}`);
        
        // 处理响应
        if (response.data.code === 200) {
          ElMessage.success(response.data.msg || '分析成功');
          // 重新获取数据以显示分析结果
          this.fetchData();
        } else {
          ElMessage.error(response.data.msg || '分析失败');
        }
      } catch (error) {
        // 处理请求异常
        console.error('分析请求错误:', error);
        ElMessage.error('分析请求失败，请稍后重试');
      } finally {
        // 关闭加载提示
        ElLoading.service().close();
      }
    },
    
    // 格式化相似度数据，添加百分号
    formatSimilarityData(data) {
      const result = {};
      // 遍历对象的所有属性
      for (const key in data) {
        // 跳过created_at和avg_similarity属性
        if (key === 'created_at' || key === 'avg_similarity') continue;
        // 为每个相似度值添加百分号
        result[key] = data[key] + '%';
      }
      return result;
    },
    
    // 根据相似度值获取标签类型
    getTagType(similarity) {
      if (similarity >= 80) return 'success'; // 高相似度，绿色
      if (similarity >= 60) return 'warning'; // 中等相似度，黄色
      return 'danger'; // 低相似度，红色
    }
  }
};
</script>

<style scoped>
.data-analysis-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-title {
  text-align: center;
  margin-bottom: 20px;
  color: #303133;
}

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

.total-info {
  margin-bottom: 15px;
  color: #606266;
  font-size: 14px;
}

.data-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.data-section {
  margin-bottom: 20px;
}

.data-section h3 {
  margin-bottom: 10px;
  font-size: 16px;
  color: #303133;
}

.analysis-time {
  margin-top: 10px;
  text-align: right;
  color: #909399;
  font-size: 12px;
}

.no-analysis {
  margin-top: 15px;
}

.analysis-btn {
  margin-top: 10px;
}
</style>