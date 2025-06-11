<template>
  <div class="data-container">
    <el-scrollbar>
      <div style="display: flex; margin-bottom: 20px;">
        <el-input v-model="userId" placeholder="请输入用户ID" style="width: 140px; margin-right: 10px;"/>
        <el-input v-model="dataId" placeholder="请输入数据ID" style="width: 140px; margin-right: 10px;"/>
        <div style="width: 500px;">
          <el-button type="primary" @click="fetchDataById" style="width: 100px; margin-right: 10px;">查询</el-button>
          <el-button type="success" @click="fetchAllData" style="width: 100px;">查看全部</el-button>
        </div>
      </div>

      <!-- 密钥操作区域 -->
      <div style="display: flex; align-items: center; margin-bottom: 20px;">
        <!-- 选择已有密钥 -->
        <el-select v-model="selectedKeyIndex" placeholder="选择密钥" style="width: 140px; margin-right: 10px;">
          <el-option
            v-for="keypair in keypairNames"
            :key="keypair.id" 
            :label="keypair.label" 
            :value="keypair.id">
          </el-option>
        </el-select>
        <el-button type="warning" @click="selectKeypair" style="margin-right: 20px;">选择密钥</el-button>

        <!-- 新增密钥 -->
        <el-select v-model="newKeyIndexToAdd" placeholder="选择新增密钥索引" style="width: 180px; margin-right: 10px;">
          <el-option
            v-for="item in availableNewKeyIndexes"
            :key="item.id"
            :label="item.label"
            :value="item.id">
          </el-option>
        </el-select>
        <el-button type="success" @click="generateNewKeypair">新增密钥</el-button>
      </div>

      <el-table :data="tableData" style="width: 100%" border>
        <el-table-column prop="id" label="ID" width="120" />
        <el-table-column prop="user_id" label="用户ID" width="100" />
        <el-table-column prop="cirrhosis" label="肝硬化" width="80" />
        <el-table-column prop="age" label="年龄" width="80" />
        <el-table-column prop="sex" label="性别" width="80" :formatter="formatSex" /> <!-- 添加 formatter 属性 -->
        <el-table-column prop="cholesterol" label="胆固醇" width="100" />
        <el-table-column prop="triglyceride" label="甘油三酯" width="100" />
        <el-table-column prop="HDL" label="高密度脂蛋白" width="110" />
        <el-table-column prop="LDL" label="低密度脂蛋白" width="110" />
        <el-table-column prop="PathDiagNum" label="病理诊断编号" width="140" />
        <el-table-column prop="BMI" label="体重指数" width="100" />
        <el-table-column prop="ALT" label="谷丙转氨酶" width="100" />
        <el-table-column prop="AST" label="谷草转氨酶" width="100" />
        <el-table-column prop="glucose" label="血糖" width="100" />
        <!-- 新增操作列 -->
        <el-table-column label="操作" width="140">
          <template #default="scope">
            <el-button type="primary" size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button type="danger" size="small" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <!-- 编辑弹窗 -->
      <el-dialog
        v-model="editDialogVisible"
        title="编辑数据"
        width="600px"
      >
        <!-- 编辑表单，绑定editForm对象 -->
        <el-form :model="editForm" label-width="120px">
          <el-form-item label="ID">
            <el-input v-model="editForm.id" disabled />
          </el-form-item>
          <el-form-item label="用户ID">
            <el-input v-model="editForm.user_id" />
          </el-form-item>
          <el-form-item label="肝硬化">
            <el-input v-model="editForm.cirrhosis" />
          </el-form-item>
          <el-form-item label="年龄">
            <el-input v-model="editForm.age" />
          </el-form-item>
          <el-form-item label="性别">
            <el-radio-group v-model="editForm.sex"> <!-- 将el-input替换为el-radio-group -->
              <el-radio :label="1">男性</el-radio>
              <el-radio :label="2">女性</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="胆固醇">
            <el-input v-model="editForm.cholesterol" />
          </el-form-item>
          <el-form-item label="甘油三酯">
            <el-input v-model="editForm.triglyceride" />
          </el-form-item>
          <el-form-item label="高密度脂蛋白">
            <el-input v-model="editForm.HDL" />
          </el-form-item>
          <el-form-item label="低密度脂蛋白">
            <el-input v-model="editForm.LDL" />
          </el-form-item>
          <el-form-item label="病理诊断编号">
            <el-input v-model="editForm.PathDiagNum" />
          </el-form-item>
          <el-form-item label="体重指数">
            <el-input v-model="editForm.BMI" />
          </el-form-item>
          <el-form-item label="谷丙转氨酶">
            <el-input v-model="editForm.ALT" />
          </el-form-item>
          <el-form-item label="谷草转氨酶">
            <el-input v-model="editForm.AST" />
          </el-form-item>
          <el-form-item label="血糖">
            <el-input v-model="editForm.glucose" />
          </el-form-item>
        </el-form>
        <template #footer>
          <div class="dialog-footer">
            <el-button @click="editDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="submitEdit">提交</el-button>
          </div>
        </template>
      </el-dialog>

      <el-pagination
        v-if="total > 0"
        :current-page="currentPage"
        :page-size="pageSize"
        :total="total"
        layout="total, prev, pager, next"
        @current-change="handleCurrentChange"
        style="margin-top: 20px; text-align: center;"
      />
    </el-scrollbar>
  </div>
</template>

<script>
import axios from 'axios';
import { ElMessage } from 'element-plus';

export default {
  data() {
    return {
      tableData: [], // 存储数据列表
      userId: '', // 用户ID输入框
      dataId: '', // 数据ID输入框
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
      newKeyIndexToAdd: null, // 新增：用于存储用户选择要新增的密钥的索引
      availableNewKeyIndexes: [], // 新增：存储可供选择创建的新密钥索引
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
    // 根据用户ID和数据ID查询
    async fetchDataById() {
      try {
        this.isSearchMode = true;
        let url = `/data/getEncryptedData?page=${this.currentPage}&page_size=${this.pageSize}`;
        if (this.userId) {
          url += `&user_id=${this.userId}`;
        }
        if (this.dataId) {
          url += `&data_id=${this.dataId}`;
        }
        
        if (!this.userId && !this.dataId) {
          ElMessage.warning('请至少输入一个查询条件');
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
        this.fetchDataById();
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
          const existingKeyIds = new Set(); // 用于存储已存在的密钥ID
          this.keypairNames = res.data.data.map(name => {
            const match = name.match(/\d+/);
            const id = match ? parseInt(match[0], 10) : name;
            existingKeyIds.add(id); // 将已存在的ID添加到Set中
            return {
              id: id,
              label: `密钥 ${id}`
            };
          });
          ElMessage.success('密钥对名称加载成功');

          // 生成可新增的密钥索引列表
          this.availableNewKeyIndexes = [];
          let count = 0;
          let potentialIndex = 1;
          while (count < 10) { // 最多生成10个可用的新密钥索引
            if (!existingKeyIds.has(potentialIndex)) {
              this.availableNewKeyIndexes.push({
                id: potentialIndex,
                label: `新增密钥 ${potentialIndex}`
              });
              count++;
            }
            potentialIndex++;
          }
          // 如果 availableNewKeyIndexes 为空，可以设置一个默认提示，或者让下拉框为空
          if (this.availableNewKeyIndexes.length > 0 && !this.newKeyIndexToAdd) {
             this.newKeyIndexToAdd = this.availableNewKeyIndexes[0].id; // 默认选中第一个可新增的
          }

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
        if (this.selectedKeyIndex === 1) {
          this.groupId = 1;
        } else if (this.selectedKeyIndex === 2) {
          this.groupId = 2;
        } else {
          // 对于其他密钥索引，可以设置默认的groupId或进行其他处理
          // this.groupId = 1; // 例如，默认回到分组1
          ElMessage.info(`当前选择了密钥 ${this.selectedKeyIndex}，groupId 逻辑未明确指定，将使用当前 groupId: ${this.groupId}`);
        }

        const res = await axios.get(`/select_keypair?key_index=${this.selectedKeyIndex}`);
        if (res.data.code === 200) {
          ElMessage.success(res.data.msg + `: 当前密钥信息 - ${JSON.stringify(res.data.data)}`);
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
      // 检查是否选择了要新增的密钥索引
      if (this.newKeyIndexToAdd === null || this.newKeyIndexToAdd === '') {
        ElMessage.warning('请选择一个要新增的密钥索引');
        return;
      }
      try {
        // 调用后端接口生成新的密钥对，使用GET请求并通过URL参数传递key_index
        const res = await axios.get(`/generate_new_keypair?key_index=${this.newKeyIndexToAdd}`);
        if (res.data.code === 200) {
          ElMessage.success(res.data.msg + ` 文件保存在: ${res.data.data.public_key_file} 和 ${res.data.data.private_key_file}`);
          // 密钥生成成功后，重新获取密钥列表以更新下拉框
          this.fetchKeypairNames(); 
          // 可以考虑将 selectedKeyIndex 自动切换到新生成的密钥，或者提示用户手动选择
          // this.selectedKeyIndex = this.newKeyIndexToAdd; // 例如，自动选中新生成的密钥
          // this.selectKeypair(); // 并加载它
        } else if (res.data.code === 409) { // 特别处理文件已存在的冲突情况
          ElMessage.error('新增密钥失败: ' + res.data.msg + '，请尝试其他索引。');
          // 文件已存在时，也刷新一下可选列表，因为可能在此期间其他操作改变了文件状态
          this.fetchKeypairNames(); 
        }else {
          ElMessage.error('新增密钥失败: ' + res.data.msg);
        }
      } catch (error) {
        ElMessage.error('新增密钥失败: ' + error.message);
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
</style>