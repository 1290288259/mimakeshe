<template>
  <div class="data-container">
    <el-table :data="tableData" style="width: 100%">
      <el-table-column prop="id" label="ID" width="120" />
      <el-table-column prop="cirrhosis" label="肝硬化" width="120" />
      <el-table-column prop="age" label="年龄" width="100" />
      <el-table-column prop="sex" label="性别" width="100" />
      <el-table-column prop="cholesterol" label="胆固醇" width="120" />
      <el-table-column prop="triglyceride" label="甘油三酯" width="120" />
      <el-table-column prop="HDL" label="高密度脂蛋白" width="140" />
      <el-table-column prop="LDL" label="低密度脂蛋白" width="140" />
      <el-table-column prop="PathDiagNum" label="病理诊断编号" width="140" />
      <el-table-column prop="BMI" label="体重指数" width="120" />
      <el-table-column prop="ALT" label="谷丙转氨酶" width="120" />
      <el-table-column prop="AST" label="谷草转氨酶" width="120" />
      <el-table-column prop="glucose" label="血糖" width="100" />
      <el-table-column label="操作" width="120">
        <template #default="scope">
          <el-button 
            type="primary" 
            size="small" 
            @click="analyzeData(scope.row.id)"
            :loading="loadingId === scope.row.id"
          >
            分析
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import axios from 'axios';
import { ElMessage } from 'element-plus';

export default {
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
  max-width: 1700px;
  margin: 0 auto;
}
</style>