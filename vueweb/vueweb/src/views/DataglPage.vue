<template>
  <div class="data-container">
    <el-card class="medical-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <div class="header-title">
            <el-icon class="header-icon"><Files /></el-icon>
            <h3>加密数据管理</h3>
          </div>
          <div class="header-actions">
             <!-- 密钥操作区域 -->
             <el-select v-model="selectedKeyIndex" placeholder="选择密钥" style="width: 180px; margin-right: 10px;" size="default">
              <template #prefix>
                <el-icon><Key /></el-icon>
              </template>
              <el-option
                v-for="keypair in keypairNames"
                :key="keypair.id" 
                :label="keypair.label" 
                :value="keypair.id">
              </el-option>
            </el-select>
            <el-button type="warning" plain @click="selectKeypair" style="margin-right: 10px;">
              <el-icon><Switch /></el-icon> 切换密钥
            </el-button>
            <el-button type="success" plain @click="generateNewKeypair">
              <el-icon><Plus /></el-icon> 新增密钥
            </el-button>
          </div>
        </div>
      </template>

      <div class="filter-section">
        <el-input 
          v-model="searchKeyword" 
          placeholder="请输入用户ID或数据ID" 
          style="width: 250px; margin-right: 10px;"
          clearable
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <el-button type="primary" @click="fetchDataByKeyword">
          <el-icon><Search /></el-icon> 查询
        </el-button>
        <el-button @click="fetchAllData">
          <el-icon><Refresh /></el-icon> 重置/全部
        </el-button>
      </div>

      <el-table 
        :data="tableData" 
        style="width: 100%" 
        border 
        stripe
        :header-cell-style="{ background: 'var(--medical-secondary)', color: 'var(--medical-primary)', fontWeight: 'bold' }"
      >
        <el-table-column prop="id" label="ID" width="80" align="center" fixed />
        <el-table-column prop="user_id" label="用户ID" width="100" align="center" />
        <el-table-column prop="cirrhosis" label="肝硬化" width="80" align="center">
           <template #default="scope">
            <el-tag :type="scope.row.cirrhosis == 1 ? 'danger' : 'success'" size="small">
              {{ scope.row.cirrhosis == 1 ? '有' : '无' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="age" label="年龄" width="80" align="center" />
        <el-table-column prop="sex" label="性别" width="80" align="center" :formatter="formatSex">
          <template #default="scope">
             <span v-if="scope.row.sex === 1"><el-icon><Male /></el-icon> 男</span>
             <span v-else-if="scope.row.sex === 2"><el-icon><Female /></el-icon> 女</span>
             <span v-else>未知</span>
          </template>
        </el-table-column>
        <el-table-column prop="cholesterol" label="胆固醇" width="100" align="center" />
        <el-table-column prop="triglyceride" label="甘油三酯" width="100" align="center" />
        <el-table-column prop="HDL" label="HDL" width="100" align="center" />
        <el-table-column prop="LDL" label="LDL" width="100" align="center" />
        <el-table-column prop="PathDiagNum" label="病理诊断" width="120" align="center" />
        <el-table-column prop="BMI" label="BMI" width="100" align="center" />
        <el-table-column prop="ALT" label="ALT" width="100" align="center" />
        <el-table-column prop="AST" label="AST" width="100" align="center" />
        <el-table-column prop="glucose" label="血糖" width="100" align="center" />
        <el-table-column label="操作" width="180" fixed="right" align="center">
          <template #default="scope">
            <el-button type="primary" link size="small" @click="handleEdit(scope.row)">
              <el-icon><Edit /></el-icon> 编辑
            </el-button>
            <el-button type="danger" link size="small" @click="handleDelete(scope.row)">
              <el-icon><Delete /></el-icon> 删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination
          v-if="total > 0"
          :current-page="currentPage"
          :page-size="pageSize"
          :total="total"
          layout="total, prev, pager, next, jumper"
          @current-change="handleCurrentChange"
          background
        />
      </div>
    </el-card>

    <!-- 编辑弹窗 -->
    <el-dialog
      v-model="editDialogVisible"
      title="编辑临床数据"
      width="700px"
      destroy-on-close
      center
    >
      <el-form :model="editForm" label-width="120px" class="edit-form" :inline="true">
        <el-divider content-position="left">基本信息</el-divider>
        <el-form-item label="ID">
          <el-input v-model="editForm.id" disabled style="width: 180px"/>
        </el-form-item>
        <el-form-item label="用户ID">
          <el-input v-model="editForm.user_id" style="width: 180px"/>
        </el-form-item>
        <el-form-item label="年龄">
          <el-input v-model="editForm.age" style="width: 180px"/>
        </el-form-item>
        <el-form-item label="性别">
          <el-radio-group v-model="editForm.sex">
            <el-radio :label="1">男</el-radio>
            <el-radio :label="2">女</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-divider content-position="left">生理指标</el-divider>
        <el-form-item label="肝硬化">
          <el-input v-model="editForm.cirrhosis" style="width: 180px"/>
        </el-form-item>
        <el-form-item label="BMI">
          <el-input v-model="editForm.BMI" style="width: 180px"/>
        </el-form-item>
        <el-form-item label="血糖">
          <el-input v-model="editForm.glucose" style="width: 180px"/>
        </el-form-item>
        <el-form-item label="病理诊断">
          <el-input v-model="editForm.PathDiagNum" style="width: 180px"/>
        </el-form-item>

        <el-divider content-position="left">血脂与肝功</el-divider>
        <el-form-item label="胆固醇">
          <el-input v-model="editForm.cholesterol" style="width: 180px"/>
        </el-form-item>
        <el-form-item label="甘油三酯">
          <el-input v-model="editForm.triglyceride" style="width: 180px"/>
        </el-form-item>
        <el-form-item label="HDL">
          <el-input v-model="editForm.HDL" style="width: 180px"/>
        </el-form-item>
        <el-form-item label="LDL">
          <el-input v-model="editForm.LDL" style="width: 180px"/>
        </el-form-item>
        <el-form-item label="ALT">
          <el-input v-model="editForm.ALT" style="width: 180px"/>
        </el-form-item>
        <el-form-item label="AST">
          <el-input v-model="editForm.AST" style="width: 180px"/>
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="editDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitEdit">保存修改</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Search, Refresh, Edit, Delete, Files, Key, Plus, Switch, Male, Female } from '@element-plus/icons-vue';

export default {
  components: { Search, Refresh, Edit, Delete, Files, Key, Plus, Switch, Male, Female },
  data() {
    return {
      tableData: [], // 存储数据列表
      searchKeyword: '', // 搜索关键字
      currentPage: 1, // 当前页码
      pageSize: 10, // 每页显示条数
      total: 0, // 总数据量
      isSearchMode: false, // 是否为搜索模式
      editDialogVisible: false, // 编辑弹窗显示控制
      editForm: { // 编辑表单对象
        id: '',
        user_id: '',
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
      selectedKeyIndex: 1, // 当前选择的密钥索引，默认为1
      keypairNames: [], // 存储密钥对名称的数组
      groupId: 1 // 新增：用于存储当前的分组ID，默认为1
    };
  },
  created() {
    // 页面创建时加载所有数据，默认使用groupId: 1
    this.fetchAllData();
    // 页面创建时获取密钥对名称
    this.fetchKeypairNames();
  },
  methods: {
    // 获取所有加密数据
    async fetchAllData() {
      try {
        this.isSearchMode = false;
        // 修改API调用，增加 group_id 参数
        const res = await axios.get(`/data/getAllEncryptedData?page=${this.currentPage}&page_size=${this.pageSize}&group_id=${this.groupId}`);
        if (res.data.code === 200) {
          this.tableData = res.data.data;
          this.total = res.data.total;
          ElMessage.success(`数据加载成功 (密钥: ${this.selectedKeyIndex}, 分组: ${this.groupId})`);
        } else {
          ElMessage.error('数据加载失败: ' + res.data.msg);
        }
      } catch (error) {
        ElMessage.error('数据加载失败: ' + error.message);
      }
    },
    // 根据关键字查询（用户ID或数据ID）
    async fetchDataByKeyword() {
      try {
        this.isSearchMode = true;
        let url = `/data/getEncryptedData?page=${this.currentPage}&page_size=${this.pageSize}`;
        if (this.searchKeyword) {
          url += `&keyword=${this.searchKeyword}`;
        }
        
        if (!this.searchKeyword) {
          ElMessage.warning('请输入查询关键字');
          return;
        }
        
        const res = await axios.get(url);
        if (res.data.code === 200) {
          this.tableData = res.data.data;
          this.total = res.data.total;
          if (this.tableData.length === 0) {
            ElMessage.warning('未找到匹配的数据');
          } else {
            ElMessage.success('查询成功');
          }
        } else {
          ElMessage.error('查询失败: ' + res.data.msg);
        }
      } catch (error) {
        ElMessage.error('查询失败: ' + error.message);
      }
    },
    // 处理页码变化
    handleCurrentChange(val) {
      this.currentPage = val;
      if (this.isSearchMode) {
        this.fetchDataByKeyword();
      } else {
        this.fetchAllData();
      }
    }, // 这里加上逗号
    // 格式化性别显示
    formatSex(row, column, cellValue) {
      if (cellValue === 1) {
        return '男性';
      } else if (cellValue === 2) {
        return '女性';
      } else {
        return ''; // 或者其他默认值
      }
    },
    // 编辑按钮事件，弹出编辑框并填充表单
    handleEdit(row) {
      this.editForm = { ...row }; // 将当前行数据赋值到表单
      this.editDialogVisible = true; // 显示弹窗
    },
    // 编辑弹窗提交事件
    async submitEdit() {
      try {
        // 发送编辑请求到后端
        const res = await axios.post('/data/editEncryptedData', this.editForm);
        if (res.data.code === 200) {
          this.$message.success('编辑成功');
          this.editDialogVisible = false; // 关闭弹窗
          this.fetchAllData(); // 刷新数据
        } else {
          this.$message.error('编辑失败: ' + res.data.msg);
        }
      } catch (error) {
        this.$message.error('编辑失败: ' + error.message);
      }
    },
    // 删除按钮事件
    async handleDelete(row) {
      try {
        // 可加确认弹窗
        if (!confirm('确定要删除该数据吗？')) return;
        // 发送删除请求到后端
        const res = await axios.get('/data/deleteEncryptedData', { params: { id: row.id } });
        if (res.data.code === 200) {
          this.$message.success('删除成功');
          this.fetchAllData(); // 刷新数据
        } else {
          this.$message.error('删除失败: ' + res.data.msg);
        }
      } catch (error) {
        this.$message.error('删除失败: ' + error.message);
      }
    },
    // 新增：获取密钥对名称列表的方法
    async fetchKeypairNames() {
      try {
        const res = await axios.get('/get_keypair_names');
        if (res.data.code === 200) {
          this.keypairNames = res.data.data.map(item => {
            return {
              id: item.id,
              label: `密钥组 ${item.id} - ${item.hospital_name}`
            };
          });
          ElMessage.success('密钥对名称加载成功');
        } else {
          ElMessage.error('密钥对名称加载失败: ' + res.data.msg);
        }
      } catch (error) {
        ElMessage.error('密钥对名称加载失败: ' + error.message);
      }
    },

    // 新增：选择密钥对的方法
    async selectKeypair() {
      try {
        // 根据选择的密钥更新groupId
        this.groupId = this.selectedKeyIndex;

        const res = await axios.get(`/select_keypair?key_index=${this.selectedKeyIndex}`);
        if (res.data.code === 200) {
          ElMessage.success(`成功切换至：${this.keypairNames.find(k => k.id === this.selectedKeyIndex)?.label || '未知密钥'}`);
          // 密钥切换成功后，使用新的groupId刷新数据
          this.fetchAllData();
        } else {
          ElMessage.error('选择密钥失败: ' + res.data.msg);
        }
      } catch (error) {
        ElMessage.error('选择密钥失败: ' + error.message);
      }
    },
    // 新增：生成新的密钥对的方法
    async generateNewKeypair() {
      try {
        // 弹出输入框要求输入医院名称
        const { value: hospitalName } = await ElMessageBox.prompt('请输入该密钥对应的医院名称', '新增密钥', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          inputPlaceholder: '如：第一人民医院',
          inputPattern: /.+/,
          inputErrorMessage: '医院名称不能为空'
        });

        if (!hospitalName) return;

        // 调用后端接口生成新的密钥对，增加hospital_name参数
        // 不再传递 key_index，由后端自动分配
        const res = await axios.get(`/generate_new_keypair?hospital_name=${hospitalName}`);
        if (res.data.code === 200) {
          // 使用后端返回的消息，其中包含了自动分配的索引
          ElMessage.success(res.data.msg);
          // 密钥生成成功后，重新获取密钥列表以更新下拉框
          this.fetchKeypairNames(); 
        } else if (res.data.code === 409) { 
          ElMessage.error('新增密钥失败: ' + res.data.msg);
          this.fetchKeypairNames(); 
        } else {
          ElMessage.error('新增密钥失败: ' + res.data.msg);
        }
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('操作已取消或发生错误');
        }
      }
    }
  }
};
</script>

<style scoped>
.data-container {
  padding: 20px;
  max-width: 1700px;
  margin: 0 auto;
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
  border-radius: 50%;
}

.header-actions {
  display: flex;
  align-items: center;
}

.filter-section {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 6px;
  border-left: 4px solid var(--medical-primary);
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

:deep(.el-table) {
  border-radius: 4px;
  overflow: hidden;
}

:deep(.el-button--primary) {
  background-color: var(--medical-primary);
  border-color: var(--medical-primary);
}

:deep(.el-button--primary:hover) {
  background-color: var(--medical-hover);
  border-color: var(--medical-hover);
}

:deep(.el-tag--success) {
  background-color: rgba(0, 150, 57, 0.1);
  border-color: rgba(0, 150, 57, 0.2);
  color: #009639;
}

:deep(.el-tag--danger) {
  background-color: rgba(218, 41, 28, 0.1);
  border-color: rgba(218, 41, 28, 0.2);
  color: #DA291C;
}
</style>