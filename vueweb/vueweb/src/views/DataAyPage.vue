<template>
  <div class="data-analysis-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <div class="header-icon">
        <el-icon><TrendCharts /></el-icon>
      </div>
      <h2 class="header-title">数据分析结果</h2>
    </div>
    
    <!-- 数据加载中提示 -->
    <div v-if="loading" class="loading-container">
      <el-icon class="is-loading"><Loading /></el-icon>
      <span>正在获取分析报告...</span>
    </div>
    
    <!-- 无数据提示 -->
    <el-empty v-if="!loading && dataList.length === 0" description="暂无分析记录" class="medical-empty"></el-empty>
    
    <!-- 数据展示区域 -->
    <div v-if="!loading && dataList.length > 0" class="data-display">
      <div class="total-info">
        <el-alert
          :title="`共找到 ${total} 条分析记录`"
          type="info"
          show-icon
          :closable="false"
          class="info-alert"
        />
      </div>
      
      <!-- 数据卡片循环 -->
      <el-card v-for="(item, index) in dataList" :key="index" class="data-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <div class="header-left">
              <el-tag effect="dark" type="primary" class="id-tag">ID: {{ item.original_data.id }}</el-tag>
              <span class="report-title">分析报告</span>
            </div>
            <el-tag v-if="item.analysis_result" 
                   :type="getTagType(item.analysis_result.avg_similarity)"
                   effect="plain"
                   class="similarity-tag">
              平均相似度: {{ item.analysis_result.avg_similarity }}%
            </el-tag>
          </div>
        </template>
        
        <!-- 原始数据展示 -->
        <div class="data-section">
          <div class="section-title">
            <span class="dot"></span>
            <h3>原始临床数据</h3>
          </div>
          <el-table :data="[item.original_data]" stripe border class="medical-table" :header-cell-style="{ background: '#f5f7fa' }">
            <el-table-column prop="age" label="年龄" width="80" align="center"></el-table-column>
            <el-table-column prop="sex" label="性别" width="80" align="center">
              <template #default="scope">
                {{ scope.row.sex === 1 ? '男' : '女' }}
              </template>
            </el-table-column>
            <el-table-column prop="BMI" label="BMI" width="100" align="center"></el-table-column>
            <el-table-column prop="cholesterol" label="胆固醇" align="center"></el-table-column>
            <el-table-column prop="triglyceride" label="甘油三酯" align="center"></el-table-column>
            <el-table-column prop="HDL" label="HDL" align="center"></el-table-column>
            <el-table-column prop="LDL" label="LDL" align="center"></el-table-column>
            <el-table-column prop="ALT" label="ALT" align="center"></el-table-column>
            <el-table-column prop="AST" label="AST" align="center"></el-table-column>
            <el-table-column prop="glucose" label="血糖" align="center"></el-table-column>
            <el-table-column prop="cirrhosis" label="肝硬化" width="100" align="center">
              <template #default="scope">
                <el-tag :type="scope.row.cirrhosis === 1 ? 'danger' : 'success'" size="small">
                  {{ scope.row.cirrhosis === 1 ? '是' : '否' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="PathDiagNum" label="病理编号" align="center"></el-table-column>
          </el-table>
        </div>
        
        <!-- 分析结果展示 -->
        <div v-if="item.analysis_result" class="data-section">
          <div class="section-title">
            <span class="dot warning"></span>
            <h3>相似度分析详情</h3>
          </div>
          <el-table :data="[formatSimilarityData(item.analysis_result)]" stripe border class="medical-table" :header-cell-style="{ background: '#fdf6ec' }">
            <el-table-column prop="age_similarity" label="年龄" align="center"></el-table-column>
            <el-table-column prop="sex_similarity" label="性别" align="center"></el-table-column>
            <el-table-column prop="BMI_similarity" label="BMI" align="center"></el-table-column>
            <el-table-column prop="cholesterol_similarity" label="胆固醇" align="center"></el-table-column>
            <el-table-column prop="triglyceride_similarity" label="甘油三酯" align="center"></el-table-column>
            <el-table-column prop="HDL_similarity" label="HDL" align="center"></el-table-column>
            <el-table-column prop="LDL_similarity" label="LDL" align="center"></el-table-column>
            <el-table-column prop="ALT_similarity" label="ALT" align="center"></el-table-column>
            <el-table-column prop="AST_similarity" label="AST" align="center"></el-table-column>
            <el-table-column prop="glucose_similarity" label="血糖" align="center"></el-table-column>
            <el-table-column prop="cirrhosis_similarity" label="肝硬化" align="center"></el-table-column>
            <el-table-column prop="PathDiagNum_similarity" label="病理编号" align="center"></el-table-column>
          </el-table>
          
          <div class="analysis-footer">
            <el-icon><Clock /></el-icon>
            <span class="analysis-time">生成时间: {{ item.analysis_result.created_at }}</span>
          </div>
        </div>
        
        <!-- 无分析结果提示 -->
        <div v-else class="no-analysis">
          <el-alert
            title="该数据尚未生成分析报告"
            type="info"
            :closable="false"
            show-icon>
          </el-alert>
          <div class="action-wrapper">
            <el-button 
              type="primary" 
              class="analysis-btn"
              @click="runAnalysis(item.original_data.id)">
              <el-icon><VideoPlay /></el-icon> 立即分析
            </el-button>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import axios from 'axios'; 
import { ElMessage, ElLoading } from 'element-plus'; 
import { Loading, TrendCharts, Clock, VideoPlay } from '@element-plus/icons-vue'; 

export default {
  name: 'DataAyPage', 
  components: {
    Loading,
    TrendCharts,
    Clock,
    VideoPlay
  },
  data() {
    return {
      userId: '', 
      dataList: [], 
      total: 0, 
      loading: false 
    };
  },
  created() {
    this.getUserIdAndFetchData();
  },
  methods: {
    // 辅助方法：格式化相似度数据，保留两位小数
    formatSimilarityData(data) {
      const formatted = {};
      for (const key in data) {
        if (typeof data[key] === 'number' && key.includes('similarity')) {
           // 如果是小数，保留2位
           formatted[key] = data[key].toFixed(2) + '%';
        } else {
           formatted[key] = data[key];
        }
      }
      return formatted;
    },
    // 辅助方法：根据相似度返回标签类型
    getTagType(similarity) {
      if (similarity >= 90) return 'success';
      if (similarity >= 70) return 'warning';
      return 'danger';
    },

    getUserIdAndFetchData() {
      const userString = sessionStorage.getItem('User');
      if (userString) {
        try {
          const user = JSON.parse(userString);
          this.userId = user.user_id;
          this.fetchData();
        } catch (error) {
          console.error('解析用户信息失败:', error);
          ElMessage.error('获取用户信息失败，请重新登录');
        }
      } else {
        ElMessage.warning('请先登录系统');
      }
    },
    
    async fetchData() {
      if (!this.userId) {
        ElMessage.warning('未获取到用户ID，请重新登录');
        return;
      }
      
      this.loading = true;
      
      try {
        const response = await axios.get(`/data/get_data_analysis_result?user_id=${this.userId}`);
        
        if (response.data.code === 200) {
          this.dataList = response.data.data;
          this.total = response.data.total;
          ElMessage.success('报告加载成功');
        } else {
          ElMessage.error(response.data.msg || '数据加载失败');
          this.dataList = [];
          this.total = 0;
        }
      } catch (error) {
        console.error('请求错误:', error);
        ElMessage.error('请求失败，请稍后重试');
        this.dataList = [];
        this.total = 0;
      } finally {
        this.loading = false;
      }
    },
    
    async runAnalysis(dataId) {
      try {
        ElLoading.service({
          fullscreen: true,
          text: '正在进行隐私计算分析，请稍候...',
          background: 'rgba(255, 255, 255, 0.8)'
        });
        
        const response = await axios.get(`/data/privacy_intersection?data_id=${dataId}`);
        // 这里假设接口返回成功后刷新数据，具体逻辑根据原代码调整
        if (response.data.code === 200) {
             ElMessage.success('分析完成');
             this.fetchData(); // 刷新列表
        } else {
             ElMessage.error(response.data.msg || '分析失败');
        }
      } catch (error) {
           ElMessage.error('分析请求异常');
      } finally {
           const loadingInstance = ElLoading.service();
           loadingInstance.close();
      }
    }
  }
};
</script>

<style scoped>
.data-analysis-container {
  padding: 24px;
  max-width: 100%;
}

.page-header {
  display: flex;
  align-items: center;
  margin-bottom: 24px;
}

.header-icon {
  width: 40px;
  height: 40px;
  background: var(--medical-primary);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  color: white;
  font-size: 20px;
  box-shadow: 0 4px 12px rgba(0, 94, 184, 0.2);
}

.header-title {
  font-size: 24px;
  color: var(--medical-text);
  margin: 0;
  font-weight: 600;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  color: var(--medical-text-secondary);
}

.total-info {
  margin-bottom: 20px;
}

.data-card {
  margin-bottom: 24px;
  border-radius: 12px;
  border: none;
  box-shadow: var(--medical-card-shadow);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.report-title {
  font-weight: 600;
  color: var(--medical-text);
  font-size: 16px;
}

.data-section {
  margin-bottom: 24px;
}

.section-title {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}

.dot {
  width: 4px;
  height: 16px;
  background: var(--medical-primary);
  border-radius: 2px;
  margin-right: 8px;
}

.dot.warning {
  background: var(--medical-warning);
}

.section-title h3 {
  margin: 0;
  font-size: 16px;
  color: var(--medical-text);
  font-weight: 600;
}

.medical-table {
  border-radius: 8px;
  overflow: hidden;
}

.analysis-footer {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  margin-top: 12px;
  color: var(--medical-text-secondary);
  font-size: 12px;
}

.analysis-time {
  margin-left: 6px;
}

.no-analysis {
  padding: 20px 0;
}

.action-wrapper {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}

.analysis-btn {
  border-radius: 6px;
}
</style>