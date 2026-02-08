<template>
  <div class="form-container">
    <el-card class="medical-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <div class="header-title">
            <el-icon class="header-icon"><UploadFilled /></el-icon>
            <h3>临床数据上报</h3>
          </div>
          <el-tag type="info">加密传输</el-tag>
        </div>
      </template>

      <el-form :model="form" label-width="180px" label-position="right" class="medical-form">
        <!-- 密钥选择 -->
        <div class="form-section">
          <div class="section-title">
            <el-icon><Key /></el-icon> 加密配置
          </div>
          <el-form-item label="加密密钥组 (group_id)">
            <el-select v-model="groupId" placeholder="请选择密钥组" style="width: 100%">
              <el-option
                v-for="keypair in keypairNames"
                :key="keypair.id"
                :label="keypair.label"
                :value="keypair.id">
              </el-option>
            </el-select>
          </el-form-item>
        </div>

        <el-divider border-style="dashed" />

        <!-- 基本信息 -->
        <div class="form-section">
          <div class="section-title">
            <el-icon><User /></el-icon> 患者基本信息
          </div>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="年龄 (Age)">
                <el-input v-model="form.age" placeholder="请输入年龄" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="性别 (Sex)">
                <el-select v-model="form.sex" placeholder="请选择性别" style="width: 100%">
                  <el-option label="男" value="1" />
                  <el-option label="女" value="2" />
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="体重指数 (BMI)">
                <el-input v-model="form.BMI" placeholder="保留一位小数" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="病理诊断 (PathDiagNum)">
                <el-input v-model="form.PathDiagNum" placeholder="诊断编号" />
              </el-form-item>
            </el-col>
          </el-row>
        </div>

        <el-divider border-style="dashed" />

        <!-- 生理指标 -->
        <div class="form-section">
          <div class="section-title">
            <el-icon><Monitor /></el-icon> 生理生化指标
          </div>
          
          <div class="subsection-label">肝脏功能</div>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="肝硬化 (Cirrhosis)">
                <el-select v-model="form.cirrhosis" placeholder="请选择" style="width: 100%">
                  <el-option label="无肝硬化 (0)" value="0" />
                  <el-option label="有肝硬化 (1)" value="1" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="血糖 (Glucose)">
                <el-input v-model="form.glucose" placeholder="mg/dL" />
              </el-form-item>
            </el-col>
          </el-row>
          <el-row :gutter="20">
             <el-col :span="12">
              <el-form-item label="谷丙转氨酶 (ALT)">
                <el-input v-model="form.ALT" placeholder="U/L" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="谷草转氨酶 (AST)">
                <el-input v-model="form.AST" placeholder="U/L" />
              </el-form-item>
            </el-col>
          </el-row>

          <div class="subsection-label">血脂指标</div>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="胆固醇 (Cholesterol)">
                <el-input v-model="form.cholesterol" placeholder="mg/dL" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="甘油三酯 (Triglyceride)">
                <el-input v-model="form.triglyceride" placeholder="mg/dL" />
              </el-form-item>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="高密度脂蛋白 (HDL)">
                <el-input v-model="form.HDL" placeholder="mg/dL" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="低密度脂蛋白 (LDL)">
                <el-input v-model="form.LDL" placeholder="mg/dL" />
              </el-form-item>
            </el-col>
          </el-row>
        </div>

        <div class="button-container">
          <el-button type="primary" @click="onSubmit" size="large" class="submit-btn">
            <el-icon><Upload /></el-icon> 提交数据
          </el-button>
          <el-button @click="onReset" size="large">
            <el-icon><RefreshRight /></el-icon> 重置表单
          </el-button>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios';
import { ElMessage } from 'element-plus';
import { UploadFilled, Key, User, Monitor, Upload, RefreshRight } from '@element-plus/icons-vue';

export default {
  components: { UploadFilled, Key, User, Monitor, Upload, RefreshRight },
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
          this.keypairNames = res.data.data.map(item => {
            return {
              id: item.id,
              label: `密钥组 ${item.id} - ${item.hospital_name}`
            };
          });
          if (this.keypairNames.length > 0 && !this.keypairNames.find(k => k.id === this.groupId)) {
            // 如果当前的 groupId 不在列表中，默认选中第一个
            this.groupId = this.keypairNames[0].id;
          }
        } else {
          console.error('获取密钥名称失败:', res.data.msg);
        }
      } catch (error) {
        console.error('获取密钥名称失败:', error);
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
  max-width: 900px;
  margin: 20px auto;
  padding: 0 20px;
}

.medical-card {
  border-radius: 8px;
  border: none;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-title {
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--medical-primary);
}

.header-title h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.header-icon {
  font-size: 20px;
  background-color: var(--medical-secondary);
  padding: 8px;
  border-radius: 8px;
}

.form-section {
  margin-bottom: 20px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.section-title .el-icon {
  color: var(--medical-primary);
}

.subsection-label {
  font-size: 14px;
  color: #666;
  margin: 10px 0 15px 0;
  padding-left: 10px;
  border-left: 3px solid #ccc;
}

.button-container {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.submit-btn {
  background-color: var(--medical-primary);
  border-color: var(--medical-primary);
  width: 150px;
}

.submit-btn:hover {
  background-color: var(--medical-hover);
  border-color: var(--medical-hover);
}

:deep(.el-form-item__label) {
  font-weight: 500;
}

:deep(.el-input__wrapper) {
  box-shadow: 0 0 0 1px #dcdfe6 inset;
}

:deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px var(--medical-primary) inset;
}
</style>