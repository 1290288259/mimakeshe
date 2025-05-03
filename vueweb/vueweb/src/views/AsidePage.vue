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
/* 优化菜单样式为更现代的浅蓝渐变主题，并增加圆角和阴影 */
.menu {
  background: #fff;           /* 只保留纯白色背景 */
  color: #1565c0;             /* 深蓝色字体 */
  height: 100%;
  border-radius: 18px;        /* 圆角 */
  padding-top: 12px;
  padding-bottom: 12px;
  margin: 12px;
  border: none;               /* 无边框 */
  box-shadow: none;           /* 无阴影 */
}

.el-menu-item {
  color: #1976d2;            /* 普通项字体颜色更柔和 */
  font-size: 15px;
  border-radius: 10px;       /* 菜单项圆角 */
  margin: 4px 8px;
  transition: background 0.2s, color 0.2s;
}

.el-menu-item:hover {
  background-color: #e1f5fe; /* 更亮的浅蓝色悬浮 */
  color: #0d47a1;
  box-shadow: 0 2px 8px 0 rgba(33, 150, 243, 0.10); /* 悬浮时有轻微阴影 */
}

.el-menu-item .el-icon {
  margin-right: 10px; /* 图标与文字之间的间距 */
}

.el-menu-item span {
  vertical-align: middle;
  font-size: 15px;
  font-weight: 500;
}

/* 当前选中项的样式 */
.el-menu-item.is-active {
  background-color: #90caf9; /* 选中项更深的浅蓝色 */
  color: #0d47a1;
  font-weight: bold;
  box-shadow: 0 2px 12px 0 rgba(33, 150, 243, 0.15);
}

/* 响应式设计：在较小屏幕下调整菜单宽度 */
@media (max-width: 768px) {
  .menu {
    width: 200px;
    margin: 0;
    border-radius: 0;
  }
}
</style>
