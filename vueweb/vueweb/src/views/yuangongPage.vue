<template>
  <div class="user-container">
    <el-card class="medical-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <div class="header-title">
            <el-icon class="header-icon"><UserFilled /></el-icon>
            <h3>人员权限管理</h3>
          </div>
          <el-button type="primary" @click="insertData" class="add-btn">
            <el-icon><Plus /></el-icon> 新增用户
          </el-button>
        </div>
      </template>

      <div class="filter-section">
        <el-input 
          v-model="userId" 
          placeholder="请输入用户编号查询" 
          style="width: 250px; margin-right: 10px;"
          clearable
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <el-button type="primary" @click="selectuser">
          <el-icon><Search /></el-icon> 查询
        </el-button>
        <el-button @click="fetchData">
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
        <el-table-column prop="userId" label="用户编号" width="140" align="center" fixed />
        <el-table-column prop="userName" label="账户名" width="180" align="center" />
        <el-table-column prop="permissionId" label="角色权限" width="150" align="center">
          <template #default="scope">
            <el-tag :type="scope.row.permissionId === 1 ? 'danger' : 'success'" effect="light">
              {{ scope.row.permissionId === 1 ? '管理员' : '普通用户' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="name" label="姓名" width="150" align="center" />
        <el-table-column prop="userPhone" label="联系电话" width="180" align="center" />
        <el-table-column prop="userAddress" label="联系地址" min-width="200" align="center" />
        <el-table-column label="操作" width="180" fixed="right" align="center">
          <template #default="scope">
            <el-button type="primary" link size="small" @click="handleEditClick(scope.row)">
              <el-icon><Edit /></el-icon> 编辑
            </el-button>
            <el-button type="danger" link size="small" @click="deleteData(scope.row.userId)">
              <el-icon><Delete /></el-icon> 删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 编辑弹出框 -->
    <el-dialog
        v-model="dialogVisible1"
        title="编辑用户信息"
        width="500px"
        center
        destroy-on-close
    >
      <el-form :model="form" label-width="80px" class="user-form">
        <el-form-item label="账户">
          <el-input v-model="form.userName" disabled />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.userPassword" show-password />
        </el-form-item>
        <el-form-item label="权限">
          <el-radio-group v-model="form.permissionId">
            <el-radio :label="1" border>管理员</el-radio>
            <el-radio :label="2" border>普通用户</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="姓名">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="电话">
          <el-input v-model="form.userPhone" />
        </el-form-item>
        <el-form-item label="地址">
          <el-input v-model="form.userAddress" type="textarea" :rows="2" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible1 = false">取消</el-button>
          <el-button type="primary" @click="frompost">保存修改</el-button>
        </div>
      </template>
    </el-dialog>


    <!-- 新增弹出框 -->
    <el-dialog
        v-model="dialogVisible2"
        title="新增用户"
        width="500px"
        center
        destroy-on-close
    >
      <el-form :model="form" label-width="80px" class="user-form">
        <el-form-item label="账户">
          <el-input v-model="form.userName" placeholder="请输入登录账户名" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.userPassword" show-password placeholder="请输入登录密码" />
        </el-form-item>
        <el-form-item label="权限">
          <el-radio-group v-model="form.permissionId">
            <el-radio :label="1" border>管理员</el-radio>
            <el-radio :label="2" border>普通用户</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="姓名">
          <el-input v-model="form.name" placeholder="请输入真实姓名" />
        </el-form-item>
        <el-form-item label="电话">
          <el-input v-model="form.userPhone" placeholder="请输入联系电话" />
        </el-form-item>
        <el-form-item label="地址">
          <el-input v-model="form.userAddress" type="textarea" :rows="2" placeholder="请输入联系地址" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible2 = false">取消</el-button>
          <el-button type="primary" @click="addpost">确认新增</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Search, Refresh, Plus, Edit, Delete, UserFilled } from '@element-plus/icons-vue';

export default {
  components: { Search, Refresh, Plus, Edit, Delete, UserFilled },
  data() {
    return {
      tableData: [],
      dialogVisible1: false,
      dialogVisible2: false,
      form: {
        userId: '',
        userName: '',
        userPassword: '',
        permissionId: 2,
        name: '',
        userAddress: '',
        userPhone: ''
      },
      userId: ''
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    // 获取所有用户
    async fetchData() {
      try {
        const res = await axios.get('/user/getall');
        if (res.data.code === 200) {
          // 根据后端返回结构调整
          this.tableData = res.data.data.userAllList;
          ElMessage.success('用户列表加载成功');
        } else {
          ElMessage.error('获取数据失败: ' + res.data.msg);
        }
      } catch (error) {
        ElMessage.error('获取数据失败: ' + error.message);
      }
    },
    // 根据ID查询用户
    async selectuser() {
      if (!this.userId) {
        ElMessage.warning('请输入用户编号');
        return;
      }
      try {
        const res = await axios.get(`/user/getuserbyid?userId=${this.userId}`);
        if (res.data.code === 200) {
          this.tableData = res.data.data.UserAllList;
          if (this.tableData.length === 0) {
             ElMessage.warning('未找到该用户');
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
    // 显示新增弹窗
    insertData() {
      this.form = {
        userName: '',
        userPassword: '',
        permissionId: 2,
        name: '',
        userAddress: '',
        userPhone: ''
      };
      this.dialogVisible2 = true;
    },
    // 提交新增
    async addpost() {
      if(!this.form.userName || !this.form.userPassword) {
          ElMessage.warning('账户名和密码为必填项');
          return;
      }
      try {
        const res = await axios.post('/user/add', this.form);
        if (res.data.code === 200) {
          ElMessage.success('新增成功');
          this.dialogVisible2 = false;
          this.fetchData();
        } else {
          ElMessage.error('新增失败: ' + res.data.msg);
        }
      } catch (error) {
        ElMessage.error('新增失败: ' + error.message);
      }
    },
    // 显示编辑弹窗
    handleEditClick(row) {
      this.form = { ...row };
      this.dialogVisible1 = true;
    },
    // 提交编辑
    async frompost() {
      try {
        const res = await axios.post('/user/update', this.form);
        if (res.data.code === 200) {
          ElMessage.success('修改成功');
          this.dialogVisible1 = false;
          this.fetchData();
        } else {
          ElMessage.error('修改失败: ' + res.data.msg);
        }
      } catch (error) {
        ElMessage.error('修改失败: ' + error.message);
      }
    },
    // 删除用户
    async deleteData(userId) {
      try {
        await ElMessageBox.confirm('确认删除该用户吗？此操作不可恢复。', '警告', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
        });
        
        const res = await axios.get(`/user/delete?userId=${userId}`);
        if (res.data.code === 200) {
          ElMessage.success('删除成功');
          this.fetchData();
        } else {
          ElMessage.error('删除失败: ' + res.data.msg);
        }
      } catch (error) {
        if (error !== 'cancel') {
             ElMessage.error('删除失败: ' + error.message);
        }
      }
    }
  }
};
</script>

<style scoped>
.user-container {
  padding: 20px;
  max-width: 1400px;
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

.filter-section {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 6px;
  border-left: 4px solid var(--medical-primary);
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