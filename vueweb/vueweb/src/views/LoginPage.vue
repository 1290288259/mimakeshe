<template>
  <div class="login-page">
    <div class="background-overlay"></div>
    
    <!-- 登录卡片 -->
    <div class="login-container" @keyup.enter="handleEnter">
      <div class="brand-section">
        <div class="logo-circle">
          <el-icon :size="40" color="#fff"><FirstAidKit /></el-icon>
        </div>
        <h2 class="system-title">医疗数据分析系统</h2>
        <p class="system-subtitle">Medical Data Analysis System</p>
      </div>
      
      <div class="form-section">
        <h3 class="login-title">用户登录</h3>
        <el-form class="login-form" size="large">
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
            <el-button type="primary" @click="login" class="login-button" :loading="loading">
              登录系统
            </el-button>
            <el-button text class="register-button" @click="zhuce">
              注册新账号
            </el-button>
          </div>
        </el-form>
      </div>
    </div>

    <!-- 注册弹窗 -->
    <el-dialog 
      v-model="dialogVisible" 
      title="用户注册" 
      width="450px" 
      align-center
      class="custom-dialog"
      :close-on-click-modal="false"
      destroy-on-close
    >
      <el-form :model="form" label-width="80px" class="register-form" size="large">
        <el-form-item label="账号">
          <el-input v-model="form.userName" placeholder="设置您的账号" :prefix-icon="User" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.userPassword" show-password placeholder="设置您的密码" :prefix-icon="Lock" />
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
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="register">提交注册</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock, FirstAidKit } from '@element-plus/icons-vue'
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

const handleEnter = () => {
  login()
}

const login = () => {
  if (!username.value || !password.value) {
    ElMessage.warning('请输入账号和密码')
    return
  }

  loading.value = true
  axios.post('/user/login', {
    userName: username.value,
    userPassword: password.value
  })
  .then(res => {
    if (res.data.code === 200) {
      ElMessage.success('登录成功')
      sessionStorage.setItem("User", JSON.stringify(res.data.data.user))
      sessionStorage.setItem("ModuleList", JSON.stringify(res.data.data.moduleList))
      router.push('/index/home')
    } else {
      ElMessage.error(res.data.msg || '登录失败')
    }
  })
  .catch(err => {
    ElMessage.error('登录服务连接失败: ' + err.message)
  })
  .finally(() => {
    loading.value = false
  })
}

const zhuce = () => {
  dialogVisible.value = true
}

const register = () => {
  if (!form.userName || !form.userPassword) {
    ElMessage.warning('请填写完整的注册信息')
    return
  }
  
  axios.post('/user/register', {
    userName: form.userName,
    userPassword: form.userPassword,
    name: form.name,
    userAddress: form.userAddress,
    userPhone: form.userPhone
  })
  .then(res => {
    if (res.data.code === 200) {
      ElMessage.success('注册成功，请登录')
      dialogVisible.value = false
      // 清空表单
      Object.keys(form).forEach(key => form[key] = '')
    } else {
      ElMessage.error(res.data.msg || '注册失败')
    }
  })
  .catch(err => {
    ElMessage.error('注册服务连接失败: ' + err.message)
  })
}
</script>

<style scoped>
.login-page {
  height: 100vh;
  width: 100vw;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  overflow: hidden;
}

/* 医疗风格背景装饰 */
.background-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    radial-gradient(circle at 10% 20%, rgba(0, 94, 184, 0.05) 0%, transparent 20%),
    radial-gradient(circle at 90% 80%, rgba(65, 182, 230, 0.1) 0%, transparent 25%);
  z-index: 0;
}

.login-container {
  display: flex;
  width: 800px;
  height: 480px;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  z-index: 1;
}

/* 左侧品牌区 */
.brand-section {
  flex: 1;
  background: linear-gradient(135deg, var(--medical-primary) 0%, #004b93 100%);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: #fff;
  padding: 40px;
  text-align: center;
}

.logo-circle {
  width: 80px;
  height: 80px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 24px;
  backdrop-filter: blur(5px);
}

.system-title {
  font-size: 28px;
  font-weight: 600;
  margin: 0 0 10px 0;
  letter-spacing: 1px;
}

.system-subtitle {
  font-size: 14px;
  opacity: 0.8;
  margin: 0;
  font-weight: 300;
  letter-spacing: 0.5px;
}

/* 右侧表单区 */
.form-section {
  flex: 1.2;
  padding: 40px 50px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.login-title {
  font-size: 22px;
  color: var(--medical-text);
  margin-bottom: 30px;
  font-weight: 500;
  text-align: left;
}

.login-form {
  width: 100%;
}

.input-field :deep(.el-input__wrapper) {
  background-color: #f7f9fc;
  box-shadow: none !important;
  border: 1px solid #e0e6ed;
  transition: all 0.3s;
}

.input-field :deep(.el-input__wrapper.is-focus) {
  background-color: #fff;
  border-color: var(--medical-primary);
  box-shadow: 0 0 0 1px var(--medical-primary) !important;
}

.button-group {
  margin-top: 30px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.login-button {
  width: 100%;
  height: 44px;
  font-size: 16px;
  letter-spacing: 2px;
  font-weight: 500;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.login-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 94, 184, 0.3);
}

.register-button {
  width: 100%;
  color: var(--medical-text-secondary);
}

.register-button:hover {
  color: var(--medical-primary);
}

/* 响应式调整 */
@media (max-width: 850px) {
  .login-container {
    width: 90%;
    height: auto;
    flex-direction: column;
  }
  
  .brand-section {
    padding: 30px;
  }
  
  .form-section {
    padding: 30px;
  }
}
</style>
