<template>
  <div class="form-container">
    <el-form :model="form" label-width="120px">
      <el-form-item label="肝硬化">
        <el-input v-model="form.cirrhosis" placeholder="请输入肝硬化值" />
      </el-form-item>
      <el-form-item label="年龄">
        <el-input v-model="form.age" placeholder="请输入年龄" />
      </el-form-item>
      <el-form-item label="性别">
        <el-select v-model="form.sex" placeholder="请选择性别">
          <el-option label="男" value="1" />
          <el-option label="女" value="0" />
        </el-select>
      </el-form-item>
      <el-form-item label="胆固醇">
        <el-input v-model="form.cholesterol" placeholder="请输入胆固醇值" />
      </el-form-item>
      <el-form-item label="甘油三酯">
        <el-input v-model="form.triglyceride" placeholder="请输入甘油三酯值" />
      </el-form-item>
      <el-form-item label="高密度脂蛋白">
        <el-input v-model="form.HDL" placeholder="请输入高密度脂蛋白值" />
      </el-form-item>
      <el-form-item label="低密度脂蛋白">
        <el-input v-model="form.LDL" placeholder="请输入低密度脂蛋白值" />
      </el-form-item>
      <el-form-item label="病理诊断编号">
        <el-input v-model="form.PathDiagNum" placeholder="请输入病理诊断编号" />
      </el-form-item>
      <el-form-item label="体重指数">
        <el-input v-model="form.BMI" placeholder="请输入体重指数" />
      </el-form-item>
      <el-form-item label="谷丙转氨酶">
        <el-input v-model="form.ALT" placeholder="请输入谷丙转氨酶值" />
      </el-form-item>
      <el-form-item label="谷草转氨酶">
        <el-input v-model="form.AST" placeholder="请输入谷草转氨酶值" />
      </el-form-item>
      <el-form-item label="血糖">
        <el-input v-model="form.glucose" placeholder="请输入血糖值" />
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
      }
    };
  },
  methods: {
    onSubmit() {
      // 提交表单逻辑
      console.log('提交数据:', this.form);
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