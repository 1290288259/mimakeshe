<template>

  <el-menu :default-active="$route.path" class="menu" :router="true">
    <el-menu-item index="/index/home" :to="{ path: '/index/home' }">
      <el-icon><House /></el-icon>
      <span>首页</span>
    </el-menu-item>
    <!-- 循环生成动态菜单项 -->
    <el-menu-item v-for="(module, index) in ModuleList" :key="index" :index="module.moduleRouter" :to="{ path: module.moduleRouter }">
      <el-icon><House /></el-icon>
      <span>{{ module.moduleDescription }}</span>
    </el-menu-item>
  </el-menu>
</template>


<script>
import { defineComponent } from 'vue';
import { House } from '@element-plus/icons-vue';  // 引入你使用的图标

export default defineComponent({
  name: "AsidePage",
  components: {
    House
  },
  data() {
    return {
      ModuleList: []
    };
  },
  mounted() {
    // 从sessionStorage中获取名为ModuleList的数据
    const storedModuleList = sessionStorage.getItem('ModuleList');
    if (storedModuleList) {
      // 将获取到的JSON字符串解析为JavaScript对象数组
      this.ModuleList = JSON.parse(storedModuleList);
    }
  }
});
</script>

<style scoped>
/* 调整菜单样式 */
.menu {
  background-color: #2c3e50; /* 侧边栏背景色 */
  color: #fff;
  height: 100%;
}

.el-menu-item {
  color: #ecf0f1;
  font-size: 14px;
}

.el-menu-item:hover {
  background-color: #34495e;
}

.el-menu-item .el-icon {
  margin-right: 10px; /* 图标与文字之间的间距 */
}

.el-menu-item span {
  vertical-align: middle;
  font-size: 14px;
  font-weight: 500;
}

/* 当前选中项的样式 */
.el-menu-item.is-active {
  background-color: #1abc9c;
  color: white;
}

/* 响应式设计：在较小屏幕下调整菜单宽度 */
@media (max-width: 768px) {
  .menu {
    width: 200px;
  }
}
</style>
