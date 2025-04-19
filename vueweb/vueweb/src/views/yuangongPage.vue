<script>
import axios from 'axios';
import { ElMessage } from 'element-plus';

export default {
  data() {
    return {
      // 定义一个普通变量来存储后端传过来的数据
      tableData: [],
      // 定义一个弹出框的状态
      dialogVisible1: false,
      dialogVisible2: false,
      // 定义一个表单对象
      form: {
        userId: '',
        userName: '',
        userPassword: '',
        permissionId: '',
        name: '',
        userAddress: '',
        userPhone: ''
      },
      //定义userid
      userId:''
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        const res = await axios.get("/user/getall");
        if (res.data.code === 200) {
          // 直接修改数组（如果是数组类型数据）来更新数据
          if (Array.isArray(res.data.data.userAllList)) {
            this.tableData = res.data.data.userAllList;
          }
          console.log('请求成功');
          console.log(this.tableData);
        } else {
          console.log('请求失败');
          ElMessage.error('请求失败，原因：' + (res.data.msg || '无详细原因'));
        }
      } catch (error) {
        console.error('请求错误', error);
        ElMessage.error('请求失败，请稍后重试，错误信息：' + error.message);
      }
    },
    handleEditClick(row) {
      console.log('编辑按钮被点击', row);
      this.dialogVisible1 = true;
      this.form.userId = row.userId;
      this.form.userName = row.userName;
      this.form.userPassword = row.userPassword;
      this.form.permissionId = row.permissionId;
      this.form.name = row.name;
      this.form.userAddress = row.userAddress;
      this.form.userPhone = row.userPhone;
    },
    //编辑提交
    frompost(){
      console.log('提交按钮被点击', this.form);
      this.dialogVisible1 = false;
      // 发送请求
      axios.post('/user/update', this.form).then(res => {
        if (res.data.code === 200) {
          ElMessage.success('修改成功');
          this.fetchData();
        } else {
          ElMessage.error('修改失败，原因：' + (res.data.msg || '无详细原因'));
        }
      }).catch(error => {
        ElMessage.error('修改失败，请稍后重试，错误信息：' + error.message);
      });
    },
    insertData() {
      console.log('新增按钮被点击');
      this.dialogVisible2 = true;
      this.form.userName = '';
      this.form.userPassword = '';
      this.form.permissionId = 2;
      this.form.name = '';
      this.form.userAddress = '';
      this.form.userPhone = '';
    },
    //新增提交
    addpost(){
      console.log('提交按钮被点击', this.form);
      this.dialogVisible2 = false;
      // 发送请求
      axios.post('/user/add', this.form).then(res => {
        if (res.data.code === 200) {
          ElMessage.success('新增成功');
          this.fetchData();
        } else {
          ElMessage.error('新增失败，原因：' + (res.data.msg || '无详细原因'));
        }
      }).catch(error => {
        ElMessage.error('新增失败，请稍后重试，错误信息：' + error.message);
      });
    },
    deleteData(id) {
      console.log('删除按钮被点击', id);
      axios.get(`/user/delete?userId=${id}` )
          .then(res => {
            if (res.data.code === 200) {
              ElMessage.success('删除成功');
              this.fetchData();
            } else {
              ElMessage.error('删除失败，原因：' + (res.data.msg || '无详细原因'));
            }
          })

    },

    selectuser(){
        console.log('查询按钮被点击');
        axios.get('/user/getuserbyid?userId='+ this.userId).then(res => {
          if (res.data.code === 200) {
            this.tableData = res.data.data.UserAllList;
            console.log(this.tableData);
            ElMessage.success('查询成功');
          } else {
            ElMessage.error('查询失败，原因：' + (res.data.msg || '无详细原因'));
          }
        }).catch(error => {
          ElMessage.error('查询失败，请稍后重试，错误信息：' + error.message);
        });
    }




  }
}
</script>

<template>
  <div>
    <el-scrollbar>
      <div style="display: flex;">
        <el-input v-model="this.userId"  placeholder="请输入用户编号" style="width: 140px; margin-right: 2px;"/>

        <div style="width: 500px; margin-right: 2px;">
          <el-button type="primary" @click = "selectuser" style="width: 100px; margin: 2px;">查询</el-button>
          <el-button type="success" @click="insertData" style="width: 100px; margin: 2px;">新增</el-button>
        </div>


      </div>


      <el-table :data="tableData">
        <!-- 每一列的 'prop' 属性对应实际数据中的字段 -->
        <el-table-column prop="userId" label="用户编号" width="140" />
        <el-table-column prop="userName" label="账户" width="200" />
        <el-table-column prop="userPassword" label="密码" width="200" />
          <el-table-column prop="permissionId" label="权限" width="200">
            <template #default="scope">
              <span v-if="scope.row.permissionId === 1">管理员</span>
              <span v-if="scope.row.permissionId === 2">普通用户</span>
            </template>
          </el-table-column>
        <el-table-column prop="name" label="名字" width="200" />
        <el-table-column prop="userAddress" label="住址" width="200" />
        <el-table-column prop="userPhone" label="电话" width="200" />

        <!-- 添加操作列 -->
        <el-table-column label="操作" width="150">
          <template v-slot="scope">
            <!-- 编辑按钮 -->
            <el-button type="primary" size="small" @click="handleEditClick(scope.row)">编辑</el-button>
            <!-- 删除按钮 -->
            <el-button type="danger" size="small" @click = "deleteData(scope.row.userId)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-scrollbar>
    <!-- 编辑弹出框 -->
    <el-dialog
        v-model="this.dialogVisible1"
        title="Tips"
        width="500"
        :before-close="handleClose"
    >
      <el-form :model="form" label-width="auto" style="max-width: 600px">
        <el-form-item label="账号：">
          <el-input v-model="this.form.userName" />
        </el-form-item>
        <el-form-item label="密码：">
          <el-input v-model="this.form.userPassword" />
          </el-form-item>
        <el-form-item label="权限：">
          <el-radio-group v-model="this.form.permissionId">
            <el-radio value=1 size="large">管理员</el-radio>
            <el-radio value=2 size="large">普通用户</el-radio>
          </el-radio-group>
          </el-form-item>
        <el-form-item label="名字：">
          <el-input v-model="this.form.name" />
        </el-form-item>
        <el-form-item label="住址：">
          <el-input v-model="this.form.userAddress" />
        </el-form-item>
        <el-form-item label="电话：">
          <el-input v-model="this.form.userPhone" />
        </el-form-item>


      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="this.dialogVisible1 = false">取消</el-button>
          <el-button type="primary" @click="frompost">
            提交
          </el-button>
        </div>
      </template>
    </el-dialog>


    <!-- 新增弹出框 -->
    <el-dialog
        v-model="this.dialogVisible2"
        title="Tips"
        width="500"
        :before-close="handleClose"
    >
      <el-form :model="form" label-width="auto" style="max-width: 600px">
        <el-form-item label="账号：">
          <el-input v-model="this.form.userName" />
        </el-form-item>
        <el-form-item label="密码：">
          <el-input v-model="this.form.userPassword" />
        </el-form-item>
        <el-form-item label="权限：">
          <el-radio-group v-model="form.permissionId">
            <el-radio value=1 size="large">管理员</el-radio>
            <el-radio value=2 size="large">普通用户</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="名字：">
          <el-input v-model="this.form.name" />
        </el-form-item>
        <el-form-item label="住址：">
          <el-input v-model="this.form.userAddress" />
        </el-form-item>
        <el-form-item label="电话：">
          <el-input v-model="this.form.userPhone" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="this.dialogVisible2 = false">取消</el-button>
          <el-button type="primary" @click="addpost">
            提交
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
/* 可以根据需要添加样式 */
</style>