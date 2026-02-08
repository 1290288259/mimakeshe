<template>
  <div class="user-center">
    <div class="profile-card-wrapper">
      <el-card class="box-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon class="header-icon"><User /></el-icon>
            <span>个人资料卡</span>
          </div>
        </template>
        
        <div class="profile-content">
          <div class="avatar-section">
            <el-avatar :size="80" icon="UserFilled" class="user-avatar" />
            <h3 class="user-display-name">{{ filteredUser.name || 'User' }}</h3>
            <el-tag type="success" size="small" round>在线</el-tag>
          </div>

          <el-descriptions :column="1" border class="user-descriptions">
            <el-descriptions-item label="账号ID">{{ filteredUser.user_id }}</el-descriptions-item>
            <el-descriptions-item label="用户名">{{ filteredUser.user_name }}</el-descriptions-item>
            <el-descriptions-item label="联系电话">{{ filteredUser.user_phone || '未填写' }}</el-descriptions-item>
            <el-descriptions-item label="联系地址">{{ filteredUser.user_address || '未填写' }}</el-descriptions-item>
            <el-descriptions-item label="权限等级">
              <el-tag size="small">{{ filteredUser.permission_id === 0 ? '超级管理员' : (filteredUser.permission_id === 1 ? '管理员' : '普通用户') }}</el-tag>
            </el-descriptions-item>
          </el-descriptions>
        </div>
        
        <div class="edit-button-wrapper">
          <el-button type="primary" class="edit-btn" @click="updateProfile">
            <el-icon><Edit /></el-icon>编辑资料
          </el-button>
        </div>
      </el-card>
    </div>

    <el-dialog
        v-model="dialogVisible1"
        title="编辑个人资料"
        width="500px"
        :before-close="handleClose"
        destroy-on-close
        class="medical-dialog"
    >
      <el-form
          :model="form"
          label-width="80px"
          label-position="right"
          class="edit-form"
      >
        <el-form-item label="账号">
          <el-input v-model="form.userName" disabled />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.userPassword" type="password" show-password />
        </el-form-item>
        <el-form-item label="姓名">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="住址">
          <el-input v-model="form.userAddress" />
        </el-form-item>
        <el-form-item label="电话">
          <el-input v-model="form.userPhone" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible1 = false">取消</el-button>
          <el-button type="primary" @click="frompost">
            保存修改
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { ElMessage } from "element-plus";
import { User, Edit, UserFilled } from '@element-plus/icons-vue';
import axios from 'axios';

// 从sessionStorage获取用户信息字符串
const userStr = sessionStorage.getItem('User');
const user = userStr? JSON.parse(userStr) : {};
const filteredUser = ref({});
// 使用ref创建响应式数据，用于控制对话框的显示隐藏
const dialogVisible1 = ref(false);
// 创建用于表单数据绑定的响应式对象form，并初始化为已有用户数据（若存在）
const form = ref({
  userId: user.user_id || '',
  userName: user.user_name || '',
  userPassword: user.user_password || '',
  permissionId: user.permission_id ,
  name: user.name || '',
  userAddress: user.user_address || '',
  userPhone: user.user_phone || ''
});

// 过滤掉值为null的属性
for (const key in user) {
  if (user[key]!== null) {
    filteredUser.value[key] = user[key];
  }
}

const updateProfile = () => {
  // 每次打开编辑对话框时，确保表单数据是最新的用户数据
  form.value = {
    userId: filteredUser.value.user_id || '',
    userName: filteredUser.value.user_name || '',
    userPassword: filteredUser.value.user_password || '',
    permissionId: filteredUser.value.permission_id ,
    name: filteredUser.value.name || '',
    userAddress: filteredUser.value.user_address || '',
    userPhone: filteredUser.value.user_phone || ''
  };
  console.log(filteredUser.value);
  console.log(form.value);
  dialogVisible1.value = true;
};

const frompost = () => {
  // 这里暂时简单打印，实际需根据业务添加发送数据到后端等逻辑
  console.log('提交表单，当前表单数据为：', form.value);
  axios.post("user/update", form.value).then(res => res.data) // 获取返回的响应数据
      .then(res => {
           if (res.code === 200) {
               // 保存成功，更新用户信息
             ElMessage.success('修改成功，重新登录后生效');
           }
           else {
               // 保存失败，提示错误信息
            console.log(res);
             ElMessage.error('修改失败');
           }
           dialogVisible1.value = false; // 关闭对话框

      });

};

const handleClose = () => {
  dialogVisible1.value = false;
  // 可以在这里重置表单数据，示例如下（根据实际需求调整）
  form.value = {
    userId: filteredUser.value.user_id || '',
    userName: filteredUser.value.user_name || '',
    userPassword: filteredUser.value.user_password || '',
    permissionId: filteredUser.value.permission_id || '',
    name: filteredUser.value.name || '',
    userAddress: filteredUser.value.user_address || '',
    userPhone: filteredUser.value.user_phone || ''
  };
};
</script>

<style scoped>
.user-center {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.profile-card-wrapper {
  max-width: 600px;
  margin: 0 auto;
}

.box-card {
  border-radius: 12px;
  border: none;
  box-shadow: var(--medical-card-shadow);
  overflow: hidden;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 600;
  color: var(--medical-primary);
  padding: 8px 0;
}

.header-icon {
  margin-right: 8px;
  font-size: 20px;
}

.profile-content {
  padding: 20px;
}

.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 30px;
}

.user-avatar {
  background-color: var(--medical-secondary);
  color: white;
  margin-bottom: 12px;
  border: 4px solid #fff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.user-display-name {
  margin: 0 0 8px 0;
  font-size: 20px;
  color: var(--medical-text);
}

.user-descriptions :deep(.el-descriptions__label) {
  width: 120px;
  justify-content: flex-end;
  font-weight: 500;
  color: var(--medical-text-secondary);
}

.edit-button-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 24px;
  margin-bottom: 10px;
}

.edit-btn {
  width: 200px;
  height: 40px;
  font-size: 16px;
  border-radius: 20px;
}

.edit-form {
  padding: 0 20px;
}
</style>