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
</template>

<style scoped>

</style>