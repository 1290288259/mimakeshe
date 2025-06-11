<template>
  <div class="form-container">
    <el-form :model="form" label-width="210px">
      <!-- 新增：选择密钥对 (group_id) -->
      <el-form-item label="选择加密密钥组 (group_id)">
        <el-select v-model="groupId" placeholder="请选择密钥组">
          <el-option
            v-for="keypair in keypairNames"
            :key="keypair.id"
            :label="keypair.label"
            :value="keypair.id">
          </el-option>
        </el-select>
      </el-form-item>

      <el-form-item label="肝硬化（cirrhosis）">
        <el-input v-model="form.cirrhosis" placeholder="无肝硬化：0，有肝硬化：1" />
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
      userId: '', // 用户ID
      groupId: 1, // 新增：选择的密钥组ID，默认为1
      keypairNames: [] // 新增：存储密钥对名称的数组
    };
  },
  created() {
    // 从会话中取出User
    const userStr = sessionStorage.getItem('User');
    if (userStr) {
      let user = JSON.parse(userStr);
      this.userId = user.user_id; // 设置userId
    }
    this.fetchKeypairNames(); // 新增：页面创建时获取密钥对名称
  },
  methods: {
    // 新增：获取密钥对名称列表的方法
    async fetchKeypairNames() {
      try {
        const res = await axios.get('/get_keypair_names'); // 调用ShowData.py中的接口
        if (res.data.code === 200) {
          this.keypairNames = res.data.data.map(name => {
            const match = name.match(/\d+/); // 从文件名中提取数字作为ID，例如 private_key1.pkl -> 1
            const id = match ? parseInt(match[0], 10) : name;
            return {
              id: id,
              label: `密钥组 ${id}` // 显示为 "密钥组 X"
            };
          });
          if (this.keypairNames.length > 0 && !this.keypairNames.find(k => k.id === this.groupId)) {
            // 如果默认的groupId不在获取到的列表中，则选择第一个可用的
            this.groupId = this.keypairNames[0].id;
          }
          ElMessage.success('密钥对名称加载成功');
        } else {
          ElMessage.error('密钥对名称加载失败: ' + res.data.msg);
        }
      } catch (error) {
        ElMessage.error('密钥对名称加载失败: ' + error.message);
        // 如果加载失败，可以提供一个默认的选项，或者禁用提交
        this.keypairNames = [{ id: 1, label: '密钥组 1 (默认)'}, {id: 2, label: '密钥组 2'}]; // 示例默认值
        if (!this.keypairNames.find(k => k.id === this.groupId)) {
            this.groupId = 1;
        }
      }
    },
    onSubmit() {
      // 提交表单逻辑，包含userId和groupId
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
        user_id: this.userId,
        group_id: this.groupId // 新增：添加groupId到提交数据
      };
      axios.post('/updata', data) // 接口名称与后端updata.py对应
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
      // this.groupId = 1; // 重置时也可以考虑重置groupId，如果需要的话
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