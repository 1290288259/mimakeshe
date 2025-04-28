<template>
  <div class="form-container">
    <el-form :model="form" label-width="210px">
      <el-form-item label="肝硬化（cirrhosis）">
        <el-input v-model="form.cirrhosis" placeholder="请输入肝硬化值" />
      </el-form-item>
      <el-form-item label="年龄（age）">
        <el-input v-model="form.age" placeholder="请输入年龄" />
      </el-form-item>
      <el-form-item label="性别（sex）">
        <el-select v-model="form.sex" placeholder="请选择性别">
          <el-option label="男" value="1" />
          <el-option label="女" value="2" />
        </el-select>
      </el-form-item>
      <el-form-item label="胆固醇（cholesterol）">
        <el-input v-model="form.cholesterol" placeholder="胆固醇值" />
      </el-form-item>
      <el-form-item label="甘油三酯（triglyceride）">
        <el-input v-model="form.triglyceride" placeholder="甘油三酯值" />
      </el-form-item>
      <el-form-item label="高密度脂蛋白（HDL）">
        <el-input v-model="form.HDL" placeholder="高密度脂蛋白值" />
      </el-form-item>
      <el-form-item label="低密度脂蛋白（LDL）">
        <el-input v-model="form.LDL" placeholder="低密度脂蛋白值（保留一位小数）" />
      </el-form-item>
      <el-form-item label="病理诊断编号（PathDiagNum）">
        <el-input v-model="form.PathDiagNum" placeholder="组织病理学: 0次穿刺活检和1次切除术" />
      </el-form-item>
      <el-form-item label="体重指数（BMI）">
        <el-input v-model="form.BMI" placeholder="体重指数（保留一位小数）" />
      </el-form-item>
      <el-form-item label="丙氨酸转氨酶水平（ALT）">
        <el-input v-model="form.ALT" placeholder="丙氨酸转氨酶水平" />
      </el-form-item>
      <el-form-item label="谷草转氨酶（AST）">
        <el-input v-model="form.AST" placeholder="谷草转氨酶值" />
      </el-form-item>
      <el-form-item label="血糖（glucose）">
        <el-input v-model="form.glucose" placeholder="血糖值" />
      </el-form-item>
      <el-form-item>
        <div class="button-container">
          <el-button type="primary" @click="onSubmit">提交</el-button>
          <el-button @click="onReset">重置</el-button>
        </div>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import axios from 'axios';
import { ElMessage } from 'element-plus';

export default {
  data() {
    return {
      form: {
        cirrhosis: '',
        age: '',
        sex: '',
        cholesterol: '',
        triglyceride: '',
        HDL: '',
        LDL: '',
        PathDiagNum: '',
        BMI: '',
        ALT: '',
        AST: '',
        glucose: ''
      },
      userId: '' // 新增userId字段
    };
  },
  created() {
    // 从会话中取出User
    const userStr = sessionStorage.getItem('User');
    if (userStr) {
      let user = JSON.parse(userStr);
      this.userId = user.user_id; // 设置userId
    }
  },
  methods: {
    onSubmit() {
      // 提交表单逻辑，包含userId
      const data = { 
        cirrhosis: this.form.cirrhosis.toString(),
        age: this.form.age.toString(),
        sex: this.form.sex.toString(),
        cholesterol: this.form.cholesterol.toString(),
        triglyceride: this.form.triglyceride.toString(),
        HDL: this.form.HDL.toString(),
        LDL: this.form.LDL.toString(),
        PathDiagNum: this.form.PathDiagNum.toString(),
        BMI: this.form.BMI.toString(),
        ALT: this.form.ALT.toString(),
        AST: this.form.AST.toString(),
        glucose: this.form.glucose.toString(),
        user_id: this.userId
      };
      axios.post('/updata', data)
        .then(response => {
          if (response.data.code === 200) {
            ElMessage.success('上传成功');
          } else {
            ElMessage.error('上传失败: ' + response.data.msg);
          }
        })
        .catch(error => {
          ElMessage.error('上传失败: ' + error.message);
        });
    },
    onReset() {
      // 重置表单逻辑
      this.form = {
        cirrhosis: '',
        age: '',
        sex: '',
        cholesterol: '',
        triglyceride: '',
        HDL: '',
        LDL: '',
        PathDiagNum: '',
        BMI: '',
        ALT: '',
        AST: '',
        glucose: ''
      };
    }
  }
};
</script>

<style scoped>
.form-container {
  max-width: 600px;
  margin: 20px auto;
  padding: 20px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.button-container {
  display: flex;
  justify-content: center;
}
</style>