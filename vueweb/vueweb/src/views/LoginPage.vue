<template>
  <router-view></router-view>
  <div class="login-container" @keyup.enter="handleEnter">
    <h2>登录</h2>
    <!-- 登录表单 -->
    <el-form label-position="top" class="login-form">
      <el-form-item class="form-item">
        <div class="label-text">账号</div>
        <el-input v-model="username" placeholder="请输入账号" class="input-field" />
      </el-form-item>
      <el-form-item class="form-item">
        <div class="label-text">密码</div>
        <el-input v-model="password" show-password placeholder="请输入密码" class="input-field" />
      </el-form-item>
    </el-form>
    <div class="button-group">
      <!-- 登录按钮 -->
      <el-button type="primary" @click="login" class="login-button">登录</el-button>
      <!-- 注册按钮 -->
      <el-button type="success" @click="zhuce" class="register-button">注册</el-button>
    </div>

    <!-- 注册框 -->
    <el-dialog v-model="dialogVisible" title="注册" width="500">
      <el-form :model="form" label-width="auto" class="register-form">
        <el-form-item label="账号：">
          <el-input v-model="form.userName" />
        </el-form-item>
        <el-form-item label="密码：">
          <el-input v-model="form.userPassword" />
        </el-form-item>
        <el-form-item label="姓名：">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="地址：">
          <el-input v-model="form.userAddress" />
        </el-form-item>
        <el-form-item label="手机号：">
          <el-input v-model="form.userPhone" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="register">提交</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>



<script>
export default {
  data() {
    return {
      // 用户名和密码
      username: '',
      password: '',
      form: {
        userName: '',
        userPassword: '',
        name: '',
        userAddress: '',
        userPhone: '',
      },
      dialogVisible: false,
    };
  },
  mounted() {
    // 组件挂载时，为html和body添加背景样式
    document.documentElement.style.height = '100%';
    document.body.style.height = '100%';
    document.body.style.margin = '0';
    document.body.style.padding = '0';
    document.body.style.backgroundImage = "url('" + require('@/assets/beijing.png') + "')";
    document.body.style.backgroundSize = 'cover';
    document.body.style.backgroundPosition = 'center';
    document.body.style.backgroundRepeat = 'no-repeat';
    document.body.style.backgroundAttachment = 'fixed';
  },
  beforeUnmount() {
    // 组件卸载前，移除html和body的背景样式
    document.documentElement.style.height = '';
    document.body.style.height = '';
    document.body.style.margin = '';
    document.body.style.padding = '';
    document.body.style.backgroundImage = '';
    document.body.style.backgroundSize = '';
    document.body.style.backgroundPosition = '';
    document.body.style.backgroundRepeat = '';
    document.body.style.backgroundAttachment = '';
  },
  methods: {
    // 登录方法
    login() {
      // 打印登录信息，用于调试
      console.log('登录')
      console.log(this.username) // 打印用户名
      console.log(this.password) // 打印密码

      // 使用 axios 发起 POST 请求，向后端发送登录请求
      this.$axios.post("/user/login", { userName: this.username, userPassword: this.password }).then(res => res.data) // 获取返回的响应数据
          .then(res => {
            // 判断登录是否成功（根据后端返回的 status code 或者自定义的 code）
            if (res.code == 200) {
              console.log('登录成功')  // 打印登录成功信息
              this.$message.success('登录成功')  // 显示成功提示框

              // 将用户信息存储到 sessionStorage 中
              sessionStorage.setItem('User', JSON.stringify(res.data.user))
              // 将模块信息存储到 sessionStorage 中
              sessionStorage.setItem('ModuleList', JSON.stringify(res.data.moduleList))

              // 登录成功后，重定向到主页（Index 页面）
              this.$router.replace('/Index/home')
            }
            else if (res.code == 401) {
              this.$message.error(res.msg)
            }
            else {
              console.log('登录失败')  // 打印登录失败信息
              this.$message.error('登录失败')  // 显示失败提示框
            }
          })
          .catch(error => {
            // 捕获并处理请求过程中发生的任何错误
            console.error('登录请求发生错误', error)
            this.$message.error('登录请求失败，请稍后重试')  // 显示网络请求失败的错误提示
          })
    },
    // 注册框触发
    zhuce(){
      this.dialogVisible = true;
      console.log('触发注册框')
      this.form.username = '';
      this.form.password = '';
      this.form.name = '';
      this.form.userAddress = '';
      this.form.userPhone = '';
    },

    // 注册方法（这里先只是一个占位，后续需根据实际注册逻辑完善）
    register() {
      console.log('触发注册操作，需完善具体注册逻辑')
      // 这里可以添加具体的注册逻辑，比如跳转到注册页面或者发起注册的 API 请求等
      this.$axios.post("/user/register" , this.form).then(res => res.data).then(res => {
          if (res.code == 200){
            console.log('注册成功')
            this.$message.success('注册成功')
            this.dialogVisible = false;
            // 注册成功后，重定向到登录页面
          }else {
            console.log('注册失败')
            this.$message.error('注册失败')
            this.dialogVisible = false;
          }
      })
    },

    // 回车键触发登录
    handleEnter() {
      console.log("回车键触发登录")
      this.login()
    },

}
};
</script>

<!-- 全局样式，不带scoped属性，作用于整个页面 -->
<style>
/* 设置html和body的高度为100%，确保背景覆盖整个页面 */
html,
body {
  height: 100%;
  margin: 0;
  padding: 0;
}


</style>

<style scoped>
.login-container {
  /* 移除 max-width，让其可以根据内容自适应或设置为100% */
  /* max-width: 400px; */
  width: 400px; /* 设置固定宽度，或者根据需要调整 */
  padding: 40px;
  background: rgba(8, 7, 105, 0.8); /* 半透明白色背景，让壁纸透出来 */
  border-radius: 12px; /* 圆角效果 */
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1); /* 添加阴影 */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: #eaeaf5; /* 将文字颜色改为深蓝色 */

  /* 实现全屏居中 */
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

h2 {
  font-size: 28px;
  font-weight: bold;
  color: #dddde0; /* 将文字颜色改为深蓝色 */
  margin-bottom: 30px;
  letter-spacing: 1px;
}

.login-form {
  width: 100%;
}

.form-item {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

.label-text {
  font-size: 20px;
  font-weight: bold;
  color: #fff; /* 文字颜色 */
  margin-right: 15px;
  flex-shrink: 0; /* 防止文字缩小 */
  white-space: nowrap;
}

.input-field {
  background-color: rgba(255, 255, 255, 0.8); /* 输入框背景色透明 */
  border-radius: 8px; /* 输入框圆角 */
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* 输入框阴影 */
  width: 100%;
  height: 40px;
}

.button-group {
  width: 100%;
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.login-button {
  width: 45%;
  height: 45px;
  border-radius: 30px;
  font-size: 16px;
}

.register-button {
  width: 45%;
  height: 45px;
  border-radius: 30px;
  font-size: 16px;
}

.el-button--primary {
  background-color: #2ecc71;
  border-color: #2ecc71;
  color: #fff;
}

.el-button--primary:hover {
  background-color: #27ae60;
}

.el-button--success {
  background-color: #f39c12;
  border-color: #f39c12;
  color: #fff;
}

.el-button--success:hover {
  background-color: #e67e22;
}

.dialog-footer {
  text-align: center;
}

.register-form .el-form-item {
  margin-bottom: 15px;
}

.register-form .el-input {
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.el-dialog__header {
  background-color: #8e44ad;
  color: white;
}

.el-dialog {
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
}

.el-input__inner:focus {
  border-color: #3498db !important;
  box-shadow: 0 0 8px rgba(52, 152, 219, 0.5);
}

</style>

