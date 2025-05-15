<template>
  <!-- 外层容器，设置样式 -->
  <div class="data-container">
    <!-- 标题，动态显示 created_at 时间 -->
    <h2 class="center-title">
      平均值分析统计
      <span v-if="createdAt" style="font-size:16px;color:#888;">（数据时间：{{ createdAt }}）</span>
    </h2>
    
    <!-- 切换按钮组 -->
    <div class="switch-container">
      <el-radio-group v-model="dataType" @change="switchDataType">
        <el-radio-button label="encrypted">密文平均值</el-radio-button>
        <el-radio-button label="plain">明文平均值</el-radio-button>
      </el-radio-group>
    </div>
    
    <!-- 新增flex容器，使表格和柱状图左右排列 -->
    <div class="flex-row">
      <!-- 表格区域，设置固定宽度和高度 -->
      <el-table :data="averagesData" class="table-box" height="300">
        <el-table-column prop="field" label="指标" width="150" />
        <el-table-column prop="value" label="平均值" width="150" />
      </el-table>
      <!-- 柱状图容器，设置与表格同高 -->
      <div ref="chartRef" class="chart-box"></div>
    </div>
    
    <!-- 新增：计算最新平均值按钮 -->
    <div class="button-container">
      <el-button 
        type="primary" 
        :loading="isCalculating" 
        @click="calculateNewAverage"
      >
        {{ isCalculating ? '计算中...' : '计算最新平均值' }}
      </el-button>
    </div>
  </div>
</template>

<script>
// 引入axios用于发送HTTP请求
import axios from 'axios';
// 引入element-plus的消息提示组件
import { ElMessage } from 'element-plus';

export default {
  data() {
    return {
      // 存储从后端获取的平均值数据，供表格展示
      averagesData: [],
      // 存储原始平均值对象，便于绘制图表
      rawAverages: {},
      // 存储 created_at 时间
      createdAt: '',
      // 新增：标记是否正在计算平均值
      isCalculating: false,
      // 新增：数据类型（密文/明文）
      dataType: 'encrypted'
    };
  },
  // 组件创建时自动调用fetchAverages方法获取数据
  created() {
    this.fetchAverages();
  },
  mounted() {
    // 组件挂载后初始化echarts实例
    this.initChart();
  },
  methods: {
    // 切换数据类型（密文/明文）
    switchDataType() {
      // 清空当前数据
      this.averagesData = [];
      this.rawAverages = {};
      // 重新获取数据
      this.fetchAverages();
    },
    
    // 异步方法：从后端获取平均值数据
    async fetchAverages() {
      try {
        // 根据当前数据类型选择不同的接口
        const url = this.dataType === 'encrypted' ? '/data/get_avg' : '/data/get_plain_avg';
        
        // 发送GET请求到后端接口
        const res = await axios.get(url);
        // 判断后端返回的状态码
        if (res.data.code === 200) {
          // 提取 created_at 字段
          this.createdAt = res.data.data.created_at || '';
          // 移除 created_at 字段，仅保留用于图表和表格的指标数据
          const pureData = { ...res.data.data };
          delete pureData.created_at; // 删除 created_at 字段，避免未使用变量警告
          
          // 删除 cirrhosis 字段，不在前端显示
          delete pureData.cirrhosis;
          
          // 保存原始数据用于图表
          this.rawAverages = pureData;
          // 将后端返回的对象转为适合表格展示的数组格式
          this.averagesData = Object.entries(pureData).map(([field, value]) => ({
            field: this.getFieldName(field), // 字段名转中文
            value: this.formatValue(value)   // 格式化数值
          }));
          // 数据获取后绘制图表
          this.$nextTick(() => {
            this.renderChart();
          });
        } else {
          // 如果后端返回错误，弹出错误提示
          ElMessage.error('获取平均值失败: ' + res.data.msg);
        }
      } catch (error) {
        // 如果请求异常，弹出错误提示
        ElMessage.error('获取平均值失败: ' + error.message);
      }
    },
    
    // 格式化数值（对于明文数据保留两位小数）
    formatValue(value) {
      if (this.dataType === 'plain' && typeof value === 'number') {
        return Number(value).toFixed(2);
      }
      return value;
    },
    
    // 新增：计算最新平均值方法
    async calculateNewAverage() {
      // 设置计算状态为true
      this.isCalculating = true;
      
      try {
        // 根据当前数据类型选择不同的接口
        const url = this.dataType === 'encrypted' ? '/data/calculate_avg' : '/data/calculate_plain_avg';
        
        // 调用后端计算平均值接口
        const calcRes = await axios.get(url);
        
        if (calcRes.data.code === 200) {
          // 计算成功，显示成功消息
          ElMessage.success('平均值计算成功，正在获取最新数据...');
          // 重新获取最新的平均值数据
          await this.fetchAverages();
          ElMessage.success('数据已更新');
        } else {
          // 计算失败，显示错误消息
          ElMessage.error('计算平均值失败: ' + calcRes.data.msg);
        }
      } catch (error) {
        // 请求异常，显示错误消息
        ElMessage.error('计算平均值请求失败: ' + error.message);
      } finally {
        // 无论成功失败，都将计算状态设为false
        this.isCalculating = false;
      }
    },
    
    // 将字段英文名转换为中文名，便于表格展示
    getFieldName(field) {
      const fieldNames = {
        // 已移除 cirrhosis 字段
        age: '年龄',
        cholesterol: '胆固醇',
        triglyceride: '甘油三酯',
        HDL: '高密度脂蛋白',
        LDL: '低密度脂蛋白',
        BMI: '体重指数',
        ALT: '谷丙转氨酶',
        AST: '谷草转氨酶',
        glucose: '血糖'
      };
      // 如果找不到对应中文名，则返回原英文名
      return fieldNames[field] || field;
    },
    // 初始化echarts实例
    initChart() {
      // 获取echarts实例（已在main.js全局挂载）
      this.echartsInstance = this.$echarts.init(this.$refs.chartRef);
    },
    // 渲染柱状图
    renderChart() {
      if (!this.echartsInstance) {
        this.initChart();
      }
      // 构造x轴和y轴数据（不包含 created_at 字段）
      const xData = [];
      const yData = [];
      for (const [field, value] of Object.entries(this.rawAverages)) {
        xData.push(this.getFieldName(field)); // 横坐标为中文指标名
        yData.push(typeof value === 'string' ? parseFloat(value) : value); // 纵坐标为对应数值，确保是数字类型
      }
      // 配置echarts的option
      const option = {
        title: {
          text: this.dataType === 'encrypted' ? '密文各项指标平均值柱状图' : '明文各项指标平均值柱状图'
        },
        tooltip: {},
        xAxis: {
          type: 'category',
          data: xData,
          axisLabel: {
            interval: 0,        // 强制显示所有标签
            rotate: 0,          // 不旋转标签
            fontSize: 12,       // 字体大小
            margin: 8,          // 与轴线距离
            align: 'center',    // 对齐方式
            hideOverlap: false  // 不隐藏重叠标签
          }
        },
        yAxis: {
          type: 'value'
        },
        grid: {
          left: '3%',           // 左边距
          right: '4%',          // 右边距
          bottom: '10%',        // 底部边距
          containLabel: true    // 包含标签在内
        },
        series: [
          {
            name: '平均值',
            type: 'bar',
            data: yData,
            barWidth: '30%',    // 减小柱子宽度，留更多空间给标签
            itemStyle: {
              color: this.dataType === 'encrypted' ? '#409EFF' : '#67C23A' // 密文蓝色，明文绿色
            },
            // 在柱顶显示数值，保留两位小数
            label: {
              show: true,       // 显示标签
              position: 'top',  // 标签显示在柱顶
              formatter: function(params) {
                // params.value 是当前柱子的数值，保留两位小数
                return Number(params.value).toFixed(2);
              },
              fontSize: 14      // 字体大小
            }
          }
        ]
      };
      // 设置option并渲染
      this.echartsInstance.setOption(option);
    }
  },
  watch: {
    // 监听数据变化，自动刷新图表
    rawAverages() {
      this.$nextTick(() => {
        this.renderChart();
      });
    }
  }
};
</script>

<style scoped>
/* 外层容器样式，居中并设置最大宽度 */
.data-container {
  padding: 20px;
  max-width: 1600px;
  margin: 0 auto;
}

/* 新增切换按钮组样式 */
.switch-container {
  display: flex;
  justify-content: center;
  margin: 20px 0;
}

/* 新增flex布局，使表格和柱状图左右排列 */
.flex-row {
  display: flex; /* 启用flex布局 */
  flex-direction: row; /* 横向排列 */
  align-items: flex-start; /* 顶部对齐 */
  gap: 30px; /* 两侧间距 */
}

/* 表格区域样式，缩小宽度并固定高度 */
.table-box {
  width: 250px; /* 减小表格宽度 */
  min-width: 200px; /* 最小宽度也减小 */
  height: 400px;
  box-sizing: border-box;
}

/* 柱状图区域样式，填满剩余空间，高度与表格一致 */
.chart-box {
  flex: 2; /* 增加flex权重使柱状图更宽 */
  height: 400px;
  min-width: 0;
}

/* 居中标题样式 */
.center-title {
  text-align: center;
}

/* 新增：按钮容器样式 */
.button-container {
  display: flex;
  justify-content: center;
  margin-top: 30px;
}
</style>