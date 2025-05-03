<template>
  <div class="head-container">
    <!-- 平均值按钮，点击后跳转到平均值页面 -->
    <el-button type="primary" @click="onAvgClick">平均值</el-button>
    <el-button type="success" @click="onAgeClick">年龄分布</el-button>
    <el-button type="info" @click="onAgeAvgClick">年龄趋势</el-button>
    <!-- 这里可以放其他内容 -->
  </div>
</template>

<script>
export default {
  name: "DataStHead",
  methods: {
    // 点击平均值按钮的处理函数
    onAvgClick() {
      // 跳转到平均值子路由页面
      this.$router.push('/index/datast/avg');
    },
    onAgeClick() {
      this.$router.push('/index/datast/agedbt');
    },
    onAgeAvgClick() {
      this.$router.push('/index/datast/ageavg');
    }
  }
}
</script>

<style scoped>
.head-container {
  padding: 20px;
  border: 2px solid #409EFF; /* 添加蓝色边框 */
  border-radius: 8px;         /* 圆角让边框更美观 */
  background: #fff;           /* 背景色为白色，突出显示 */
  box-shadow: 0 2px 8px rgba(64,158,255,0.08); /* 添加轻微阴影增强立体感 */
  margin-bottom: 20px;        /* 与下方内容留出间距 */
}
</style>