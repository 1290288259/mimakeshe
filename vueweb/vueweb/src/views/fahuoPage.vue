<script>
import axios from 'axios';
import { ElMessage } from 'element-plus';

export default {
  data() {
    return {
      // 定义一个普通变量来存储后端传过来的数据
      tableData: [],
      orderDetailsList: [],
      // 定义一个弹出框的状态
      dialogVisible1: false,
      dialogVisible2: false,
      // 定义一个表单对象
      //定义userid
      orderId:'',
      tkNum:'',
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        const res = await axios.get("/orders/selectAll");
        if (res.data.code === 200) {
          // 直接修改数组（如果是数组类型数据）来更新数据
          if (Array.isArray(res.data.data.ordersList)) {
            this.tableData = res.data.data.ordersList;
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

   //查询
    select(){
      console.log('查询按钮被点击');
      axios.get('/orders/select?orderId='+ this.orderId).then(res => {
        if (res.data.code === 200) {
          this.tableData = res.data.data.ordersList;
          console.log(this.tableData);
          ElMessage.success('查询成功');
        } else {
          ElMessage.error('查询失败，原因：' + (res.data.msg || '无详细原因'));
        }
      }).catch(error => {
        ElMessage.error('查询失败，请稍后重试，错误信息：' + error.message);
      });
    },
    //订单详细
    Details(orderId) {
      this.orderId = orderId;
      console.log('订单详细按钮被点击');
      this.dialogVisible1 = true;
      axios.get('/order-details/select?orderId='+ orderId).then(res => {
        if (res.data.code === 200) {
          this.orderDetailsList = res.data.data.orderDetailsList;
          console.log(this.orderDetailsList);
          ElMessage.success('订单详细查询成功');
        } else {
          ElMessage.error('订单详细查询失败，原因：' + (res.data.msg || '无详细原因'));
        }
        })
    },
    //发货
    fahuo(orderId,tkNum){
      console.log('发货按钮被点击');
      axios.post('/orders/fahuo',{orderId:orderId,tkNum:tkNum}).then(res => {
        if (res.data.code === 200) {
          ElMessage.success('发货成功');
        } else {
          ElMessage.error('发货失败，原因：' + (res.data.msg || '无详细原因'));
        }
      });
      this.dialogVisible1 = false;
      this.fetchData();

    }




  }
}
</script>

<template>
  <div>
    <el-scrollbar>
      <div style="display: flex;">
        <el-input v-model="this.orderId"  placeholder="请输入订单号" style="width: 140px; margin-right: 2px;"/>

        <div style="width: 500px; margin-right: 2px;">
          <el-button type="primary" @click = "select" style="width: 100px; margin: 2px;">查询</el-button>
        </div>


      </div>

      <el-table :data="tableData">
        <!-- 每一列的 'prop' 属性对应实际数据中的字段 -->
        <el-table-column prop="orderId" label="订单号" width="140" />
        <el-table-column prop="orderTime" label="下单时间" width="200" />
        <el-table-column prop="userId" label="用户编号" width="200" />
        <el-table-column prop="name" label="名字" width="200" />
        <el-table-column prop="userAddress" label="住址" width="200" />
        <el-table-column prop="userPhone" label="电话" width="200" />



        <!-- 添加操作列 -->
        <el-table-column label="操作" width="300">
          <template v-slot="scope">
            <!-- 编辑按钮 -->
            <el-button type="primary" size="small" @click="Details(scope.row.orderId)">订单详细</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-scrollbar>
    <!-- 订单详细弹出框 -->
    <el-dialog
        v-model="this.dialogVisible1"
        title="Tips"
        width="500"
        :before-close="handleClose"
    >
      <el-table :data="orderDetailsList">
        <!-- 每一列的 'prop' 属性对应实际数据中的字段 -->

        <el-table-column prop="productId" label="商品编号" width="140" />
        <el-table-column prop="productName" label="商品名称" width="200" />
        <el-table-column prop="quantity" label="商品数量" width="200" />
      </el-table>
      <el-input v-model="this.tkNum"  placeholder="快递号" style="width: 140px; margin-right: 2px;"/>
      <el-button type="primary" @click = "fahuo(this.orderId,this.tkNum)">发货</el-button>




    </el-dialog>


  </div>
</template>

<style scoped>
/* 可以根据需要添加样式 */
</style>