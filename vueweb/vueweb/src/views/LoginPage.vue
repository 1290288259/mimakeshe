<template>
  <div class="login-page">
    <!-- 登录卡片 -->
    <div class="login-container" @keyup.enter="handleEnter">
      <div class="login-header">
        <h2>欢迎登录</h2>
        <p class="subtitle">医疗数据分析系统</p>
      </div>
      
      <el-form class="login-form">
        <el-form-item class="form-item">
          <el-input 
            v-model="username" 
            placeholder="请输入账号" 
            class="input-field"
            :prefix-icon="User"
          />
        </el-form-item>
        
        <el-form-item class="form-item">
          <el-input 
            v-model="password" 
            show-password 
            placeholder="请输入密码" 
            class="input-field"
            :prefix-icon="Lock"
          />
        </el-form-item>

        <div class="button-group">
          <el-button type="primary" @click="login" class="login-button" :loading="loading" round>
            登录系统
          </el-button>
          <el-button text bg @click="zhuce" class="register-button" round>
            注册账号
          </el-button>
        </div>
      </el-form>
    </div>

    <!-- 注册弹窗 -->
    <el-dialog 
      v-model="dialogVisible" 
      title="用户注册" 
      width="420px" 
      align-center
      class="register-dialog custom-dialog"
      :show-close="false"
      destroy-on-close
    >
      <el-form :model="form" label-width="70px" class="register-form">
        <el-form-item label="账号">
          <el-input v-model="form.userName" placeholder="请输入账号" :prefix-icon="User" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.userPassword" show-password placeholder="请输入密码" :prefix-icon="Lock" />
        </el-form-item>
        <el-form-item label="姓名">
          <el-input v-model="form.name" placeholder="请输入真实姓名" />
        </el-form-item>
        <el-form-item label="地址">
          <el-input v-model="form.userAddress" placeholder="请输入联系地址" />
        </el-form-item>
        <el-form-item label="手机号">
          <el-input v-model="form.userPhone" placeholder="请输入手机号码" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false" class="cancel-btn">取消</el-button>
          <el-button type="primary" @click="register" class="submit-btn">立即注册</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import axios from 'axios'

const router = useRouter()

// 状态定义
const username = ref('')
const password = ref('')
const loading = ref(false)
const dialogVisible = ref(false)

const form = reactive({
  userName: '',
  userPassword: '',
  name: '',
  userAddress: '',
  userPhone: '',
})

// 背景设置逻辑
const setBackground = () => {
  document.documentElement.style.height = '100%';
  document.body.style.height = '100%';
  document.body.style.margin = '0';
  document.body.style.padding = '0';
  document.body.style.backgroundImage = "url('" + require('@/assets/beijing.png') + "')";
  document.body.style.backgroundSize = 'cover';
  document.body.style.backgroundPosition = 'center';
  document.body.style.backgroundRepeat = 'no-repeat';
  document.body.style.backgroundAttachment = 'fixed';
}

const clearBackground = () => {
  document.documentElement.style.height = '';
  document.body.style.height = '';
  document.body.style.margin = '';
  document.body.style.padding = '';
  document.body.style.backgroundImage = '';
  document.body.style.backgroundSize = '';
  document.body.style.backgroundPosition = '';
  document.body.style.backgroundRepeat = '';
  document.body.style.backgroundAttachment = '';
}

// 生命周期钩子
onMounted(() => {
  setBackground()
})

onBeforeUnmount(() => {
  clearBackground()
})

// 登录逻辑
const login = () => {
  if (!username.value || !password.value) {
    ElMessage.warning('请输入账号和密码')
    return
  }

  loading.value = true
  
  axios.post("/user/login", { userName: username.value, userPassword: password.value })
      .then(res => res.data)
      .then(res => {
        loading.value = false
        if (res.code == 200) {
          ElMessage.success('登录成功')
          sessionStorage.setItem('User', JSON.stringify(res.data.user))
          sessionStorage.setItem('ModuleList', JSON.stringify(res.data.moduleList))
          router.replace('/Index/home')
        } else if (res.code == 401) {
          ElMessage.error(res.msg)
        } else {
          ElMessage.error('登录失败')
        }
      })
      .catch(error => {
        loading.value = false
        console.error('登录请求发生错误', error)
        ElMessage.error('登录请求失败，请稍后重试')
      })
}

// 注册相关逻辑
const zhuce = () => {
  dialogVisible.value = true
  // 重置表单
  Object.assign(form, {
    userName: '',
    userPassword: '',
    name: '',
    userAddress: '',
    userPhone: '',
  })
}

const register = () => {
  if (!form.userName || !form.userPassword) {
    ElMessage.warning('请填写完整的注册信息')
    return
  }
  
  axios.post("/user/register", form).then(res => res.data).then(res => {
      if (res.code == 200){
        ElMessage.success('注册成功')
        dialogVisible.value = false
      } else {
        ElMessage.error(res.msg || '注册失败')
      }
  }).catch(() => {
    ElMessage.error('注册请求失败')
  })
}

const handleEnter = () => {
  login()
}
</script>

<style scoped>
.login-page {
  height: 100vh;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  /* 确保父容器背景透明，显示body背景 */
  background: transparent; 
}

/* 玻璃拟态卡片 */
.login-container {
  width: 400px;
  padding: 50px 40px;
  background: rgba(255, 255, 255, 0.15); /* 浅色半透明背景 */
  backdrop-filter: blur(20px); /* 毛玻璃效果 */
  -webkit-backdrop-filter: blur(20px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.3); /* 边框高亮 */
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.login-container:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

.login-header {
  text-align: center;
  margin-bottom: 40px;
  color: #1976D2;
}

.login-header h2 {
  font-size: 28px;
  margin-bottom: 10px;
  font-weight: 600;
  letter-spacing: 2px;
  text-shadow: 0 1px 2px rgba(255, 255, 255, 0.8);
}

.subtitle {
  font-size: 14px;
  opacity: 0.9;
  letter-spacing: 1px;
  font-weight: 500;
}

.login-form {
  width: 100%;
}

.form-item {
  margin-bottom: 25px;
}

/* 深度选择器修改Element Plus输入框样式 */
:deep(.input-field .el-input__wrapper) {
  background-color: rgba(255, 255, 255, 0.4) !important;
  box-shadow: none !important;
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 30px;
  padding: 8px 15px;
  transition: all 0.3s ease;
}

:deep(.input-field .el-input__wrapper.is-focus) {
  background-color: rgba(255, 255, 255, 0.6) !important;
  border-color: #1976D2;
  box-shadow: 0 0 10px rgba(25, 118, 210, 0.2) !important;
}

:deep(.input-field .el-input__inner) {
  color: #1976D2 !important;
  height: 40px;
  font-weight: 500;
}

:deep(.input-field .el-input__inner::placeholder) {
  color: rgba(25, 118, 210, 0.5);
}

:deep(.input-field .el-icon) {
  color: #1976D2;
}

.button-group {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-top: 10px;
  width: 100%;
  align-items: center;
}

.login-button {
  width: 100%;
  height: 45px;
  font-size: 16px;
  letter-spacing: 4px;
  background: linear-gradient(135deg, #409EFF 0%, #1976D2 100%);
  border: none;
  font-weight: bold;
  box-shadow: 0 4px 15px rgba(25, 118, 210, 0.3);
  transition: all 0.3s;
}

.login-button:hover {
  background: linear-gradient(135deg, #1976D2 0%, #409EFF 100%);
  transform: scale(1.02);
}

.register-button {
  width: 100%;
  height: 45px;
  color: #1976D2 !important;
  border: 1px solid rgba(25, 118, 210, 0.3) !important;
  background: rgba(255, 255, 255, 0.4) !important;
  font-weight: 600;
  letter-spacing: 2px;
}

.register-button:hover {
  background: rgba(255, 255, 255, 0.6) !important;
  border-color: #1976D2 !important;
}

/* 注册弹窗样式 */
:deep(.custom-dialog) {
  border-radius: 16px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.95);
}

:deep(.custom-dialog .el-dialog__header) {
  margin-right: 0;
  padding: 20px;
  border-bottom: 1px solid #eee;
  text-align: center;
}

:deep(.custom-dialog .el-dialog__title) {
  font-weight: 600;
  color: #333;
}

.register-form {
  padding: 10px 20px 0;
}

.dialog-footer {
  display: flex;
  justify-content: center;
  gap: 20px;
  padding-bottom: 10px;
}

.dialog-footer .el-button {
  padding: 10px 30px;
  border-radius: 20px;
}
</style>