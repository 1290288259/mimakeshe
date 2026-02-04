<template>
  <div class="data-container">
    <el-scrollbar>
      <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 20px;">
        <el-input v-model="searchKeyword" placeholder="请输入用户ID或数据ID" style="width: 200px; margin-right: 10px;"/>
        <el-button type="primary" @click="fetchDataByKeyword" style="width: 100px; margin-right: 10px;">查询</el-button>
        <el-button type="success" @click="fetchAllData" style="width: 100px; margin-right: 30px;">查看全部</el-button>

        <!-- 密钥操作区域 -->
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
import { ElMessage, ElMessageBox } from 'element-plus';

export default {
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
</style>