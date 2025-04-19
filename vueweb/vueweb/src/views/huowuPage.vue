<script>
import axios from 'axios';
import { ElMessage } from 'element-plus';

export default {
  data() {
    return {

      // 定义一个普通变量来存储后端传过来的数据
      tableData: [],
      productTypesList:[],
      // 定义一个弹出框的状态
      dialogVisible1: false,
      dialogVisible2: false,
      // 定义一个表单对象
      form: {
        productId: '',
        productName: '',
        price: '',
        stockQuantity:'',
        typeId: '',
      },
      form2: {
        userId: '',
        userName: '',
        userPassword: '',
        permissionId:'',
      },
      //定义userid
      productId2:'',
    };
  },
  //刷新数据
  created() {
    this.fetchData();
  },
  methods: {
    // 获取货物数据
    async fetchData() {
      try {
        const res = await axios.get("/products/getAll");
        if (res.data.code === 200) {
          // 直接修改数组（如果是数组类型数据）来更新数据
          if (Array.isArray(res.data.data.productsList)) {
            this.tableData = res.data.data.productsList;
            this.productTypesList = res.data.data.productTypesList;
          }
          console.log('请求成功');
          console.log(this.tableData);
          console.log(this.productTypesList);
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
      this.form.productId = row.productId;
      this.form.productName = row.productName;
      this.form.price = row.price;
      this.form.stockQuantity = row.stockQuantity;
      this.form.typeId = row.typeId;
    },
    //编辑提交
    frompost(){
      console.log('提交按钮被点击', this.form);
      this.dialogVisible1 = false;
      // 发送请求
      axios.post('/products/update', this.form).then(res => {
        if (res.data.code === 200) {
          ElMessage.success('修改成功');
          console.log(res.data.code);
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
      this.form.productName = '';
      this.form.price = '';
      this.form.stockQuantity = '';
      this.form.typeId = '';
    },
    //新增提交
    addpost(){
      console.log('提交按钮被点击', this.form);
      this.dialogVisible2 = false;
      // 发送请求
      axios.post('/products/insert', this.form).then(res => {
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
    //删除函数
    deleteData(id) {
      console.log('删除按钮被点击', id);
      axios.get(`/products/delete?productId=${id}` )
          .then(res => {
            if (res.data.code === 200) {
              ElMessage.success('删除成功');
              this.fetchData();
            } else {
              ElMessage.error('删除失败，原因：' + (res.data.msg || '无详细原因'));
            }
          })


    },

    select(){
      console.log('查询按钮被点击');
      axios.get('/products/select?productId='+ this.productId2).then(res => {
        if (res.data.code === 200) {
          this.tableData = res.data.data.productsList;
          console.log(this.productsList);
          ElMessage.success('查询成功');
        } else {
          ElMessage.error('查询失败，原因：' + (res.data.msg || '无详细原因'));
        }
      }).catch(error => {
        ElMessage.error('查询失败，请稍后重试，错误信息：' + error.message);
      });
    },
    selectproductbytype(typeid){
      console.log('查询按钮被点击');
      axios.get('/products/selectByTypeId?typeId='+ typeid).then(res => {
        if (res.data.code === 200) {
          this.tableData = res.data.data.productsList;
          console.log(this.productsList);
          ElMessage.success('查询成功');
        } else {
          ElMessage.error('查询失败，原因：' + (res.data.msg || '无详细原因'));
        }
      }).catch(error => {
        ElMessage.error('查询失败，请稍后重试，错误信息：' + error.message);
      });
    },






  }
}
</script>

<template>
  <div>
    <el-scrollbar>
      <div style="display: flex;">
        <el-input v-model="this.productId2"  placeholder="请输入商品编号" style="width: 140px; margin-right: 2px;"/>
          <select v-model="selectedOption" style="width: 140px; margin-right: 2px;">
            <option v-for="item in productTypesList" :key="item.typeId" :value="item.typeId" @click="selectproductbytype(item.typeId)">{{ item.typeName }}</option>
          </select>
        <div style="width: 500px; margin-right: 2px;">
          <el-button type="primary" @click = "select" style="width: 100px; margin: 2px;">查询</el-button>
          <el-button type="success" @click="insertData" style="width: 100px; margin: 2px;">新增</el-button>
        </div>


      </div>


      <el-table :data="tableData">
        <!-- 每一列的 'prop' 属性对应实际数据中的字段 -->
        <el-table-column prop="productId" label="货物编号" width="140" />
        <el-table-column prop="productName" label="货物名称" width="200" />
        <el-table-column prop="typeName" label="商品分类" width="200" />
        <el-table-column prop="stockQuantity" label="存货数量" width="200" />
        <el-table-column prop="price" label="商品单价" width="200" />





        <!-- 添加操作列 -->
        <el-table-column label="操作" width="150">
          <template v-slot="scope">
            <!-- 编辑按钮 -->
            <el-button type="primary" size="small" @click="handleEditClick(scope.row)">编辑</el-button>
            <!-- 删除按钮 -->
            <el-button type="danger" size="small" @click = "deleteData(scope.row.productId)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-scrollbar>
    <!-- 编辑弹出框 -->
    <!-- 编辑弹出框 -->
    <el-dialog
        v-model="this.dialogVisible1"
        title="Tips"
        width="500"
        :before-close="handleClose"
    >
      <el-form :model="form" label-width="auto" style="max-width: 600px">
        <el-form-item label="货物名称">
          <el-input v-model="this.form.productName" />
        </el-form-item>
        <el-form-item label="货物存量">
          <el-input v-model="this.form.stockQuantity" />
        </el-form-item>
        <el-form-item label="商品分类">
          <el-select v-model="this.form.typeId" placeholder="请选择商品分类">
            <el-option
                v-for="item in productTypesList"
                :key="item.typeId"
                :label="item.typeName"
                :value="item.typeId"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="商品单价">
          <el-input v-model="this.form.price" />
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
        <el-form-item label="货物名称">
          <el-input v-model="this.form.productName" />
        </el-form-item>
        <el-form-item label="货物存量">
          <el-input v-model="this.form.stockQuantity" />
        </el-form-item>
        <el-form-item label="商品分类">
          <el-select v-model="this.form.typeId" placeholder="请选择商品分类">
            <el-option
                v-for="item in productTypesList"
                :key="item.typeId"
                :label="item.typeName"
                :value="item.typeId"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="商品单价">
          <el-input v-model="this.form.price" />
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