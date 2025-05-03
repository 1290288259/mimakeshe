<template>
  <div class="data-st-page">
    <!-- 引入头部组件 -->
    <DataStHead />
    <!-- 主体内容为子路由出口 -->
    <el-container style="height: 100%; display: flex; flex-direction: column;">
      <el-main style="background-color: #f4f6f9; padding: 20px; flex: 1;">
        <router-view></router-view>
      </el-main>
    </el-container>
  </div>
</template>

<script>
// 引入头部组件
import DataStHead from './DataStHead.vue';

export default {
  name: "DataStPage",
  components: {
    DataStHead // 注册头部组件
  }
};
</script>

<style scoped>
.data-st-page {
  padding: 20px;
}
.nav-btns {
  margin-bottom: 20px;
}
.nav-link {
  margin-right: 20px;
  color: #409EFF;
  text-decoration: none;
  font-size: 18px;
}
.nav-link.router-link-exact-active {
  font-weight: bold;
  text-decoration: underline;
}
</style>