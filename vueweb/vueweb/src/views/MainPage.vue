<template>
  <div class="user-center">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>个人中心</span>
        </div>
      </template>
      <el-collapse accordion>
        <el-collapse-item v-for="(value, key) in filteredUser" :key="key" :name="key">
          <template #title>
            <span>{{ key }}</span>
          </template>
          <div class="user-info-item">{{ value }}</div>
        </el-collapse-item>
      </el-collapse>
      <div class="edit-button-wrapper">
        <el-button type="primary" @click="updateProfile">编辑资料</el-button>
      </div>
    </el-card>

    <el-dialog
        v-model="dialogVisible1"
        title="Tips"
        width="500"
        :before-close="handleClose"
    >
      <el-form
          :model="form"
          label-width="auto"
          style="max-width: 600px"
      >
        <el-form-item label="账号：">
          <el-input v-model="form.userName" />
        </el-form-item>
        <el-form-item label="密码：">
          <el-input v-model="form.userPassword" />
        </el-form-item>
        <el-form-item label="名字：">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="住址：">
          <el-input v-model="form.userAddress" />
        </el-form-item>
        <el-form-item label="电话：">
          <el-input v-model="form.userPhone" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible1 = false">取消</el-button>
          <el-button type="primary" @click="frompost">
            提交
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import {ElMessage} from "element-plus";
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
  width: 600px;
  margin: 50px auto;
}

.box-card {
  border: none;
}

.card-header {
  font-size: 20px;
  font-weight: bold;
  text-align: center;
}

.user-info-item {
  margin-left: 10px;
}

.edit-button-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 20px;
  margin-bottom: 20px;
}
</style>