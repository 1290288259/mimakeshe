<template>
  <div class="common-layout">
    <el-container class="app-container">
      
      <!-- Aside Section -->
      <el-aside width="240px" class="app-aside">
        <div class="aside-logo">
          <el-icon size="24" color="#005EB8"><Monitor /></el-icon>
          <span class="logo-text">医疗分析平台</span>
        </div>
        <AsidePage @menu-item-click="handleMenuItemClick" />
      </el-aside>

      <!-- Main Section -->
      <el-container class="main-container">
        <!-- Header section -->
        <el-header height="64px" class="app-header">
          <HeaderPage />
        </el-header>

        <!-- Main content area -->
        <el-main class="app-main">
          <div class="content-wrapper">
            <router-view></router-view>
          </div>
        </el-main>

        <!-- Footer section -->
        <el-footer height="40px" class="app-footer">
          <div class="footer-content">
            <span>© 2026 医疗数据分析系统 v1.0</span>
            <span class="divider">|</span>
            <span>Powered by Privacy Computing</span>
          </div>
        </el-footer>
      </el-container>

    </el-container>
  </div>
</template>

<script>
import { defineComponent } from 'vue';
import { Monitor } from '@element-plus/icons-vue';
import AsidePage from "@/views/AsidePage";
import HeaderPage from "@/views/HeaderPage";

export default defineComponent({
  name: "IndexPage",
  components: {
    AsidePage,
    HeaderPage,
    Monitor
  },
  methods: {
    handleMenuItemClick(route) {
      this.$router.push(route);
    }
  }
});
</script>

<style scoped>
.common-layout {
  height: 100vh;
  width: 100vw;
  background-color: var(--medical-bg);
  overflow: hidden;
}

.app-container {
  height: 100%;
}

/* 侧边栏样式 */
.app-aside {
  background-color: #fff;
  border-right: 1px solid #eef1f6;
  display: flex;
  flex-direction: column;
  box-shadow: 2px 0 8px rgba(0,0,0,0.02);
  z-index: 10;
}

.aside-logo {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  border-bottom: 1px solid #f0f0f0;
  margin-bottom: 10px;
}

.logo-text {
  font-size: 18px;
  font-weight: 600;
  color: var(--medical-primary);
  letter-spacing: 1px;
}

/* 主内容区容器 */
.main-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

/* 头部样式 */
.app-header {
  background-color: #fff;
  padding: 0;
  box-shadow: 0 1px 4px rgba(0,21,41,0.08);
  z-index: 9;
}

/* 主内容区域 */
.app-main {
  background-color: var(--medical-bg);
  padding: 20px;
  flex: 1;
  overflow-y: auto;
}

.content-wrapper {
  min-height: 100%;
  /* 如果页面本身有背景卡片，这里可以不设背景 */
}

/* 页脚样式 */
.app-footer {
  background-color: #fff;
  border-top: 1px solid #eef1f6;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #909399;
  font-size: 12px;
}

.footer-content {
  display: flex;
  align-items: center;
}

.divider {
  margin: 0 10px;
  color: #e0e0e0;
}
</style>
