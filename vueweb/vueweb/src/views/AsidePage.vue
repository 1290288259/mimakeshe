<template>
  <el-menu :default-active="$route.path" class="menu" :router="true">
    <el-menu-item index="/index/home" :to="{ path: '/index/home' }">
      <el-icon><House /></el-icon>
      <span>首页</span>
    </el-menu-item>
    <!-- 循环生成动态菜单项 -->
    <el-menu-item v-for="(module, index) in ModuleList" :key="index" :index="module.moduleRouter" :to="{ path: module.moduleRouter }">
      <el-icon><DataLine /></el-icon>
      <span>{{ module.moduleDescription }}</span>
    </el-menu-item>
  </el-menu>
</template>


<script>
import { defineComponent } from 'vue';
import { House, DataLine } from '@element-plus/icons-vue';

export default defineComponent({
  name: "AsidePage",
  components: {
    House,
    DataLine
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
.menu {
  background: #fff;
  height: 100%;
  border-right: none;
  padding-top: 8px;
}

.el-menu-item {
  color: var(--medical-text-secondary);
  font-size: 14px;
  font-weight: 500;
  margin: 4px 12px;
  border-radius: 8px;
  height: 48px;
  line-height: 48px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.el-menu-item:hover {
  background-color: var(--medical-bg);
  color: var(--medical-primary);
}

.el-menu-item.is-active {
  background-color: #e6f6ff;
  color: var(--medical-primary);
  font-weight: 600;
  box-shadow: inset 4px 0 0 var(--medical-primary);
  border-radius: 0 8px 8px 0;
  margin-left: 0;
  margin-right: 12px;
}

.el-menu-item .el-icon {
  margin-right: 12px;
  font-size: 18px;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .menu {
    width: 100%;
    margin: 0;
  }
}
</style>
