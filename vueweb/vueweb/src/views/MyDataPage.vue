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
      userId: '' // 用户ID
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