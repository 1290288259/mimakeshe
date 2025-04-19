<template>
  <div class="cart-container">
    <!-- 购物车标题 -->
    <div class="cart-title">
      <h2>我的购物车</h2>
    </div>
    <!-- 购物车商品列表展示 -->
    <el-scrollbar class="cart-table-scroll">
      <el-table :data="cartData" border stripe style="width: 100%">
        <!-- 商品编号列 -->
        <el-table-column prop="productId" label="商品编号" width="120">
          <template v-slot="scope">
            <span class="table-content">{{ scope.row.productId }}</span>
          </template>
        </el-table-column>
        <!-- 商品名称列 -->
        <el-table-column prop="productName" label="商品名称" width="200">
          <template v-slot="scope">
            <span class="table-content">{{ scope.row.productName }}</span>
          </template>
        </el-table-column>
        <!-- 商品单价列 -->
        <el-table-column prop="price" label="单价" width="100">
          <template v-slot="scope">
            <span class="table-content price-text">{{ scope.row.price }}</span>
          </template>
        </el-table-column>
        <!-- 商品数量列 -->
        <el-table-column prop="quantity" label="数量" width="150">
          <template v-slot="scope">
            <el-input-number
                v-model="scope.row.quantity"
                :min="1"
                @change="updateQuantity(scope.row.productId, $event)"
                class="quantity-input"
            />
          </template>
        </el-table-column>
        <!-- 总价列（根据单价和数量计算得出） -->
        <el-table-column label="总价" width="100">
          <template v-slot="scope">
            <span class="table-content price-text">{{ scope.row.price * scope.row.quantity }}</span>
          </template>
        </el-table-column>
        <!-- 操作列（例如删除商品按钮） -->
        <el-table-column label="操作" width="120">
          <template v-slot="scope">
            <el-button
                type="danger"
                size="small"
                @click="removeFromCart(scope.row.productId)"
                icon="el-icon-delete"
                circle
            />

          </template>
        </el-table-column>
      </el-table>
    </el-scrollbar>
    <!-- 购物车总价统计 -->
    <div class="cart-total-container">
      <div class="cart-total-label">
        <span>购物车总价：</span>
      </div>
      <div class="cart-total-price">
        <span>{{ calculateTotalPrice() }}</span>
      </div>
    </div>
    <!-- 清空购物车按钮 -->
    <div class="clear-cart-container">
      <el-button
          type="danger"
          size="medium"
          @click="clearCart"
          icon="el-icon-trash"
      >清空购物车</el-button>
      <el-button type="primary" @click="submitCart">提交</el-button>
    </div>
  </div>
</template>

<script>
import { ElMessage } from 'element-plus';
import axios from 'axios';
export default {
  data() {
    return {
      // 存储购物车数据的数组
      cartData: [],
      userId: ''
    };
  },
  created() {
    this.initCartSession();
    let userString = sessionStorage.getItem('User');
    let user = JSON.parse(userString);
    this.userId = user.userId;
    console.log(this.userId);

  },
  methods: {
    // 初始化购物车会话，从localStorage获取数据
    initCartSession() {
      // 从localStorage获取购物车数据
      const storedCartData = localStorage.getItem('cartData');
      if (storedCartData) {
        this.cartData = JSON.parse(storedCartData);
        console.log(this.cartData);
      } else {
        this.cartData = [];
      }

    },
    // 计算购物车商品总价
    calculateTotalPrice() {
      let total = 0;
      this.cartData.forEach(item => {
        total += item.price * item.quantity;
      });
      return total;
    },
    // 从购物车中删除指定商品
    removeFromCart(productId) {
      this.cartData = this.cartData.filter(item => item.productId!== productId);
      localStorage.setItem('cartData', JSON.stringify(this.cartData));
      ElMessage.success('已成功从购物车中删除商品');
    },
    // 更新商品数量
    updateQuantity(productId, newQuantity) {
      this.cartData.forEach(item => {
        if (item.productId === productId) {
          item.quantity = newQuantity;
        }
      });
      localStorage.setItem('cartData', JSON.stringify(this.cartData));
      ElMessage.success('商品数量已更新');
    },
    // 清空购物车
    clearCart() {
      this.cartData = [];
      localStorage.setItem('cartData', JSON.stringify(this.cartData));
      ElMessage.success('购物车已清空');
    }
    ,
    // 提交购物车
    submitCart() {
      // 这里可以发起请求，将购物车数据提交到服务器
      axios.post("/orders/insert" ,this.cartData,
          {params: {
          userId: this.userId
        }}).then(res => {
        if (res.data.code === 200) {
          ElMessage.success('订单提交成功');
          this.clearCart();
        }else
        {
          ElMessage.error('订单提交失败');
        }
      })

    }
  }
}
</script>

<style scoped>
/* 整体购物车容器样式 */
.cart-container {
  width: 800px;
  margin: 20px auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

/* 购物车标题样式 */
.cart-title {
  text-align: center;
  margin-bottom: 20px;
}

/* 表格滚动条容器样式 */
.cart-table-scroll {
  max-height: 300px;
  overflow-y: auto;
}

/* 表格内容样式 */
.table-content {
  font-size: 14px;
  color: #333;
}

/* 价格文本样式 */
.price-text {
  color: #e91e63;
  font-weight: bold;
}

/* 数量输入框样式 */
.quantity-input {
  width: 100%;
}

/* 购物车总价容器样式 */
.cart-total-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #f3f3f3;
  border-radius: 4px;
}

/* 购物车总价标签样式 */
.cart-total-label {
  font-size: 16px;
  color: #666;
}

/* 购物车总价金额样式 */
.cart-total-price {
  font-size: 18px;
  color: #e91e63;
  font-weight: bold;
}

/* 清空购物车按钮容器样式 */
.clear-cart-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}
</style>