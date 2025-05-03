<template style="height: 100vh">
  <div class="common-layout" style="min-height: 100vh; display: flex; flex-direction: column;">
    <el-container style="height: 100%">

      <!-- Aside Section -->
      <el-aside style="background-color: #2c3e50; color: white; width: 250px; height: 100%; padding-top: 20px;">
        <AsidePage @menu-item-click="handleMenuItemClick" />
      </el-aside>

      <!-- Main Section -->
      <el-container style="height: 100%; display: flex; flex-direction: column;">
        <!-- Header section -->
        <el-header style="background-color: #fff; padding: 0 20px;">
          <HeaderPage />
        </el-header>

        <!-- Main content area -->
        <el-main style="background-color: #f4f6f9; padding: 20px; flex: 1;">
          <router-view></router-view>
        </el-main>

        <!-- Footer section -->
        <el-footer style="background-color: #fff; padding: 10px 20px; text-align: center; border-top: 1px solid #ddd;">
          © 2024 2200350223黄仕轩
        </el-footer>
      </el-container>

    </el-container>
  </div>
</template>

<script>
import { defineComponent } from 'vue';
import AsidePage from "@/views/AsidePage";
import HeaderPage from "@/views/HeaderPage";

export default defineComponent({
  name: "IndexPage",
  components: {
    AsidePage,
    HeaderPage
  },
  methods: {
    handleMenuItemClick(route) {
      // 路由跳转
      this.$router.push(route);
    }
  }
});
</script>

<style scoped>
/* 布局容器 */
.common-layout {
  min-height: 100vh; /* 使父容器至少占满整个屏幕 */
  display: flex;
  flex-direction: column;
  font-family: 'Arial', sans-serif;
}

/* 头部样式 */
.el-header {
  background-color: #fff;
  padding: 10px 20px;
  border-bottom: 1px solid #ddd;
}

/* 侧边栏样式 */
.el-aside {
  background-color: #fff; /* 侧边栏背景为白色 */
  color: white;
  padding-top: 20px;
  height: 100%; /* 高度占满父容器 */
  min-height: 100vh; /* 保证在内容较少时也能占满视口高度 */
}

/* 工具栏样式 */
.toolbar {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  height: 100%;
}

.toolbar span {
  font-size: 14px;
  font-weight: 500;
  color: #333;
  margin-left: 10px;
}

/* 菜单和内容区的样式 */
.el-main {
  padding: 20px;
  background-color: #f4f6f9;
  flex: 1;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

/* 菜单项的样式（假设你有菜单组件） */
.el-menu {
  background-color: #2c3e50;
  padding: 0;
  border-right: none;
}

.el-menu-item {
  color: #ecf0f1;
}

.el-menu-item:hover {
  background-color: #34495e;
}

/* 修改 el-dropdown 的样式 */
.el-dropdown-menu {
  background-color: #fff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  border-radius: 6px;
  min-width: 140px;
}

.el-dropdown-item {
  font-size: 13px;
  padding: 8px 12px;
  color: #333;
}

.el-dropdown-item:hover {
  background-color: #f5f5f5;
}

/* 简单的响应式设计 */
@media (max-width: 1024px) {
  .el-aside {
    width: 200px;
  }

  .el-header {
    padding: 10px;
  }

  .toolbar {
    justify-content: flex-start;
  }
}
</style>
