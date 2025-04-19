<script>
import axios from 'axios';
import { ElMessage } from 'element-plus';

export default {
  data() {
    return {
      // 定义一个普通变量来存储后端传过来的数据
      tableData: [],
      productTypesList: [],
      // 定义一个弹出框的状态
      dialogVisible1: false,
      dialogVisible2: false,
      // 定义一个表单对象
      form: {
        productId: '',
        productName: '',
        price: '',
        stockQuantity: '',
        typeId: '',
      },
      productId: '',
      // 新增，用于存储购物车数据的数组（从localStorage读取或初始化）
      cartData: JSON.parse(localStorage.getItem('cartData')) || []
    };
  },
  //刷新数据
  created() {
    this.fetchData();
    this.tableData.forEach(row => {
      row.quantity = '';
    });
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
    //选择商品
    selectbyId() {
      console.log('查询按钮被点击');
      axios.get('/products/select?productId=' + this.productId).then(res => {
        if (res.data.code === 200) {
          this.tableData = res.data.data.productsList;
          console.log(this.tableData);
          ElMessage.success('查询成功');
        } else {
          ElMessage.error('查询失败，原因：' + (res.data.msg || '无详细原因'));
        }
      }).catch(error => {
        ElMessage.error('查询失败，请稍后重试，错误信息：' + error.message);
      });
    },
    // 处理点击选择按钮，将商品信息加入购物车会话（这里使用localStorage模拟）
    useproduct(productId, quantity, price,productName) {
      if (!productId ||!quantity) {
        ElMessage.warning('请输入商品编号和数量');
        return;
      }
      const itemToAdd = {
        productId: productId,
        quantity: quantity,
        price : price,
        productName: productName

      };
      // 将新商品信息添加到购物车数据数组
      this.cartData.push(itemToAdd);
      // 把更新后的购物车数据存储回localStorage
      localStorage.setItem('cartData', JSON.stringify(this.cartData));
      ElMessage.success('已成功加入购物车');
    }
  }
}
</script>

<template>
  <div>
    <el-scrollbar>
      <div style="display: flex;">
        <el-input v-model="this.productId" placeholder="请输入商品编号" style="width: 140px; margin-right: 2px;"/>
        <div style="width: 500px; margin-right: 2px;">
          <el-button type="primary" @click="selectbyId" style="width: 100px; margin: 2px;">查询</el-button>

        </div>


      </div>


      <el-table :data="tableData">
        <!-- 每一列的 'prop' 属性对应实际数据中的字段 -->
        <el-table-column prop="productId" label="货物编号" width="140"/>
        <el-table-column prop="productName" label="货物名称" width="200"/>
        <el-table-column prop="typeName" label="商品分类" width="200"/>
        <el-table-column prop="stockQuantity" label="存货数量" width="200"/>
        <el-table-column prop="price" label="商品单价" width="200"/>
        <!-- 添加数量列，添加v-if判断 -->
        <el-table-column label="数量" width="120">
          <template v-slot="scope">
            <template v-if="scope.row">
              <el-input v-model="scope.row.quantity" placeholder="请输入数量" style="width: 80px; margin-right: 5px;"></el-input>
            </template>
          </template>
        </el-table-column>
        <!-- 添加操作列 -->
        <el-table-column label="操作" width="150">
          <template v-slot="scope">
            <template v-if="scope.row">
              <el-button type="danger" size="small" @click="useproduct(scope.row.productId, scope.row.quantity ,scope.row.price,scope.row.productName)">选择</el-button>
            </template>
          </template>
        </el-table-column>
      </el-table>
    </el-scrollbar>






  </div>
</template>

<style scoped>
/* 可以根据需要添加样式 */
</style>