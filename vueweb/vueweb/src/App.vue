<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'App',
}
</script>

<style>
/* 全局变量定义 - 医疗风格配色 */
:root {
  --medical-primary: #005EB8;      /* NHS Blue - 主色 */
  --medical-hover: #004b93;        /* Darker Blue - 悬停色 */
  --medical-secondary: #41B6E6;    /* Light Blue - 辅助色 */
  --medical-success: #009639;      /* Green - 成功/健康 */
  --medical-warning: #FFB81C;      /* Amber - 警告 */
  --medical-danger: #DA291C;       /* Red - 危险/紧急 */
  --medical-bg: #F0F4F8;           /* 极淡的冷灰色背景 */
  --medical-text: #231F20;         /* 深灰黑色字体 */
  --medical-text-secondary: #525f7f;
  --medical-card-shadow: 0 4px 6px rgba(50, 50, 93, 0.11), 0 1px 3px rgba(0, 0, 0, 0.08);
}

body {
  margin: 0;
  padding: 0;
  height: 100%;
  overflow: hidden;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
  background-color: var(--medical-bg);
  color: var(--medical-text);
  -webkit-font-smoothing: antialiased;
}

#app {
  height: 100%;
}

/* 覆盖 Element Plus 的默认主题色 (可选，如果未配置 SCSS 变量) */
.el-button--primary {
  --el-button-bg-color: var(--medical-primary);
  --el-button-border-color: var(--medical-primary);
  --el-button-hover-bg-color: #004b93;
  --el-button-hover-border-color: #004b93;
}

.el-menu-item.is-active {
  color: var(--medical-primary) !important;
}
</style>
