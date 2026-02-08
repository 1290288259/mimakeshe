<template>
  <div class="header-bar">
    <!-- 左侧大标题 -->
    <div class="main-title-wrapper">
      <div class="main-title">
        <span class="title-text">医疗数据分析系统</span>
        <span class="title-en">Medical Data Analysis System</span>
      </div>
    </div>
    <!-- 右侧工具栏 -->
    <div class="toolbar">
      <div class="user-info">
        <el-tag :type="tagType" effect="light" round class="role-tag">{{ tagText }}</el-tag>
        <span class="user-name">{{name}}</span>
      </div>
      <el-dropdown trigger="click">
        <div class="setting-btn">
          <el-icon :size="20"><Setting /></el-icon>
        </div>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="logout">
              <el-icon><SwitchButton /></el-icon>退出登录
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<script setup>
import { Setting, SwitchButton } from "@element-plus/icons-vue";

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
    tagText = '未知权限';
}

function logout() {
  sessionStorage.removeItem('User');
  sessionStorage.removeItem('ModuleList');
  window.location.href = '/login';
}
</script>

<style scoped>
.header-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
  background: #fff;
  height: 64px;
  box-shadow: var(--medical-card-shadow);
  border-bottom: 1px solid #eef2f7;
  z-index: 100;
}

.main-title-wrapper {
  flex: 1;
  display: flex;
  align-items: center;
}

.main-title {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.title-text {
  font-size: 20px;
  font-weight: 600;
  color: var(--medical-primary);
  letter-spacing: 1px;
}

.title-en {
  font-size: 10px;
  color: var(--medical-text-secondary);
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-top: 2px;
}

.toolbar {
  display: flex;
  align-items: center;
  gap: 24px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.role-tag {
  font-weight: 500;
}

.user-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--medical-text);
}

.setting-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  color: var(--medical-text-secondary);
  cursor: pointer;
  transition: all 0.3s ease;
}

.setting-btn:hover {
  background-color: var(--medical-bg);
  color: var(--medical-primary);
}
</style>