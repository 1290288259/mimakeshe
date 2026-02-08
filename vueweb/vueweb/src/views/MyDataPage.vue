<template>
  <div class="data-container">
    <el-card class="medical-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <div class="header-title">
            <el-icon class="header-icon"><List /></el-icon>
            <h3>患者数据列表</h3>
          </div>
          <el-tag type="primary" effect="plain">共 {{ tableData.length }} 条记录</el-tag>
        </div>
      </template>
    
      <el-table 
        :data="tableData" 
        style="width: 100%" 
        stripe 
        border
        :header-cell-style="{ background: 'var(--medical-secondary)', color: 'var(--medical-primary)', fontWeight: 'bold' }"
        row-key="id"
      >
        <el-table-column prop="id" label="ID" width="80" align="center" fixed />
        <el-table-column prop="cirrhosis" label="肝硬化" width="100" align="center">
          <template #default="scope">
            <el-tag :type="scope.row.cirrhosis === 1 ? 'danger' : 'success'" effect="light">
              {{ scope.row.cirrhosis === 1 ? '有' : '无' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="age" label="年龄" width="80" align="center" />
        <el-table-column prop="sex" label="性别" width="80" align="center">
          <template #default="scope">
            <span v-if="scope.row.sex === 1"><el-icon><Male /></el-icon> 男</span>
            <span v-else-if="scope.row.sex === 2"><el-icon><Female /></el-icon> 女</span>
            <span v-else>未知</span>
          </template>
        </el-table-column>
        <el-table-column prop="cholesterol" label="胆固醇" width="100" align="center" />
        <el-table-column prop="triglyceride" label="甘油三酯" width="100" align="center" />
        <el-table-column prop="HDL" label="HDL" width="100" align="center" />
        <el-table-column prop="LDL" label="LDL" width="100" align="center" />
        <el-table-column prop="PathDiagNum" label="病理编号" width="120" align="center" />
        <el-table-column prop="BMI" label="BMI" width="100" align="center" />
        <el-table-column prop="ALT" label="ALT" width="100" align="center" />
        <el-table-column prop="AST" label="AST" width="100" align="center" />
        <el-table-column prop="glucose" label="血糖" width="100" align="center" />
        <el-table-column label="操作" width="120" fixed="right" align="center">
          <template #default="scope">
            <el-button 
              type="primary" 
              size="small" 
              plain
              @click="analyzeData(scope.row.id)"
              :loading="loadingId === scope.row.id"
              class="action-btn"
            >
              分析
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios';
import { ElMessage } from 'element-plus';
import { List, Male, Female, DataLine } from '@element-plus/icons-vue';

export default {
  components: { List, Male, Female, DataLine },
  data() {
    return {
      tableData: [], // 存储用户数据
      userId: '', // 用户ID
      loadingId: null // 当前正在分析的数据ID
    };
  },
  created() {
    // 从会话中取出User
    const userStr = sessionStorage.getItem('User');
    if (userStr) {
      let user = JSON.parse(userStr);
      this.userId = user.user_id; // 设置userId
      this.fetchData(); // 获取数据
    }
  },
  methods: {
    async fetchData() {
      try {
        const res = await axios.get('/data/getdataByuserid?user_id=' + this.userId);
        if (res.data.code === 200) {
          this.tableData = res.data.data; // 更新数据
          ElMessage.success('数据加载成功');
        } else {
          ElMessage.error('数据加载失败: ' + res.data.msg);
        }
      } catch (error) {
        ElMessage.error('数据加载失败: ' + error.message);
      }
    },
    
    // 分析数据方法
    async analyzeData(dataId) {
      this.loadingId = dataId; // 设置当前加载的ID
      
      try {
        // 调用隐私求交接口
        const res = await axios.get('/data/privacy_intersection', {
          params: { data_id: dataId }
        });
        
        if (res.data.code === 200) {
          ElMessage.success('数据分析成功');
        } else {
          ElMessage.error('数据分析失败: ' + res.data.msg);
        }
      } catch (error) {
        ElMessage.error('数据分析请求失败: ' + error.message);
      } finally {
        this.loadingId = null; // 清除加载状态
      }
    }
  }
};
</script>

<style scoped>
.data-container {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.medical-card {
  border-radius: 8px;
  border: none;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.header-icon {
  font-size: 20px;
  color: var(--medical-primary);
  background-color: var(--medical-secondary);
  padding: 8px;
  border-radius: 8px;
}

h3 {
  margin: 0;
  font-size: 18px;
  color: #333;
  font-weight: 600;
}
</style>