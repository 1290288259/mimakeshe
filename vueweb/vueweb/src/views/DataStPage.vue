<template>
  <div class="data-container">
    <h2>数据分析统计</h2>
    <el-table :data="averagesData" style="width: 100%">
      <el-table-column prop="field" label="指标" width="180" />
      <el-table-column prop="value" label="平均值" width="180" />
    </el-table>
  </div>
</template>

<script>
import axios from 'axios';
import { ElMessage } from 'element-plus';

export default {
  data() {
    return {
      averagesData: [] // 存储从DataOB.py获取的平均值数据
    };
  },
  created() {
    this.fetchAverages();
  },
  methods: {
    async fetchAverages() {
      try {
        const res = await axios.get('/data/averages');
        if (res.data.code === 200) {
          // 转换数据格式以便表格显示
          this.averagesData = Object.entries(res.data.data).map(([field, value]) => ({
            field: this.getFieldName(field),
            value
          }));
        } else {
          ElMessage.error('获取平均值失败: ' + res.data.msg);
        }
      } catch (error) {
        ElMessage.error('获取平均值失败: ' + error.message);
      }
    },
    getFieldName(field) {
      // 将字段名转换为中文显示
      const fieldNames = {
        cirrhosis: '肝硬化',
        age: '年龄',
        cholesterol: '胆固醇',
        triglyceride: '甘油三酯',
        HDL: '高密度脂蛋白',
        LDL: '低密度脂蛋白',
        BMI: '体重指数',
        ALT: '谷丙转氨酶',
        AST: '谷草转氨酶',
        glucose: '血糖'
      };
      return fieldNames[field] || field;
    }
  }
};
</script>

<style scoped>
.data-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}
</style>