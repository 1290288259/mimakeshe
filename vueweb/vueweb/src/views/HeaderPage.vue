<script setup>

import {Setting} from "@element-plus/icons-vue";

const user = JSON.parse(sessionStorage.getItem('User'));
const name = user.name;
let permissionId = user.permission_id || 0;

let tagType;
let tagText;

switch (permissionId) {
  case 0:
    tagType = 'success';
    tagText = '超级管理员';
    break;
  case 1:
    tagType = 'warning';
    tagText = '管理员';
    break;
  case 2:
    tagType = 'primary';
    tagText = '普通用户';
    break;
  default:
    tagType = 'info';
    tagText = '未知权限用户';
}
function logout() {
  // 清除 sessionStorage 中的用户信息
  sessionStorage.removeItem('User');
  // 重置路由
  sessionStorage.removeItem('ModuleList');

  // 重定向到登录页面
  window.location.href = '/login';  // 假设 login 页面路径是 '/login'
}
</script>

<template>
  <div class="header-bar">
    <!-- 左侧大标题，宽度80%，居中显示 -->
    <div class="main-title-wrapper">
      <div class="main-title">医疗数据分析系统</div>
    </div>
    <!-- 右侧工具栏 -->
    <div class="toolbar">
      <el-dropdown>
        <el-icon style="margin-right: 8px; margin-top: 1px;">
          <setting />
        </el-icon>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="logout">退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
      <el-tag :type="tagType">{{ tagText }}</el-tag>
      <span style="font-size: 14px; font-weight: 500; color: #333;">{{name}}</span>
    </div>
  </div>
</template>

<style scoped>
/* 整体横向排列，左右分布 */
.header-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px 0 24px;
  background: #fff;
  height: 64px;
  box-shadow: 0 2px 8px rgba(64,158,255,0.08);
  margin-bottom: 20px;
}

/* 包裹大标题的div，占80%宽度，并让标题居中 */
.main-title-wrapper {
  width: 80%;
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center;     /* 垂直居中 */
  height: 100%;
}

/* 大标题样式，浅蓝色，居中 */
.main-title {
  font-size: 32px;
  font-weight: bold;
  color: #5dade2; /* 浅蓝色 */
  letter-spacing: 4px;
  text-align: center;
  width: 100%;
}

/* 工具栏内容右对齐 */
.toolbar {
  display: flex;
  align-items: center;
  gap: 16px;
}
</style>