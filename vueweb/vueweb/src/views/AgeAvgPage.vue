<template>
  <!-- 外层容器，设置样式 -->
  <div class="data-container">
    <!-- 标题 -->
    <h2 class="center-title">年龄段数据分析</h2>

    <!-- 字段选择按钮组 -->
    <div class="button-group">
      <el-button
        v-for="(name, field) in fieldNames"
        :key="field"
        :type="currentField === field ? 'primary' : 'default'"
        @click="changeField(field)"
        :loading="isLoading && currentField === field"
      >
        {{ name }}
      </el-button>
    </div>

    <!-- 显示数据时间信息 -->
    <div v-if="latestDataTimestamp" class="timestamp-display">
      数据更新时间: {{ latestDataTimestamp }}
    </div>

    <!-- 计算最新平均值的按钮，单独放置并居中 -->
    <div class="calculate-button-container">
      <el-button
        type="success"
        @click="calculateLatestAvg"
        :loading="isCalculating"
      >
        计算最新平均值
      </el-button>
    </div>

    <!-- 折线图容器 -->
    <div ref="chartRef" class="chart-box"></div>
  </div>
</template>

<script>
// 引入axios用于发送HTTP请求
import axios from 'axios';
// 引入element-plus的消息提示组件
import { ElMessage } from 'element-plus';
// 引入echarts，确保在main.js中已全局注册或在此处按需引入
// import * as echarts from 'echarts'; // 如果未全局注册，需要在此处引入

export default {
  data() {
    return {
      // 当前选中的字段
      currentField: 'cholesterol',
      // 是否正在加载数据（从数据库获取）
      isLoading: false,
      // 是否正在计算最新平均值
      isCalculating: false,
      // 存储从后端获取的数据
      chartData: {},
      // 最新数据的时间戳
      latestDataTimestamp: null,
      // 字段名称映射（英文到中文）
      fieldNames: {
        cholesterol: '胆固醇',
        triglyceride: '甘油三酯',
        HDL: '高密度脂蛋白',
        LDL: '低密度脂蛋白',
        BMI: '体重指数',
        ALT: '谷丙转氨酶',
        AST: '谷草转氨酶',
        glucose: '血糖'
      },
      // echarts实例
      chartInstance: null
    };
  },
  // 组件创建时自动获取默认字段的数据
  created() {
    // 页面加载时，从数据库获取数据
    this.fetchData(this.currentField);
  },
  // 组件挂载后初始化echarts实例
  mounted() {
    this.initChart();
  },
  // 组件销毁前清理echarts实例
  beforeUnmount() {
    if (this.chartInstance) {
      this.chartInstance.dispose();
      this.chartInstance = null;
    }
    // 移除窗口大小变化的监听器
    window.removeEventListener('resize', this.handleResize);
  },
  methods: {
    // 初始化echarts实例
    initChart() {
      // 获取echarts实例（已在main.js全局挂载）
      // 如果未全局挂载，请使用: this.chartInstance = echarts.init(this.$refs.chartRef);
      this.chartInstance = this.$echarts.init(this.$refs.chartRef);

      // 添加窗口大小变化的监听，自动调整图表大小
      window.addEventListener('resize', this.handleResize);
    },

    // 处理窗口大小变化
    handleResize() {
      if (this.chartInstance) {
        this.chartInstance.resize();
      }
    },

    // 切换字段
    changeField(field) {
      if (this.currentField !== field) {
        this.currentField = field;
        // 切换字段时，从数据库获取数据
        this.fetchData(field);
      }
    },

    // 从后端获取数据 (从数据库获取)
    async fetchData(fieldName) {
      this.isLoading = true;

      try {
        // 发送GET请求到后端获取数据库中存储的平均值数据
        const res = await axios.get('/data/get_age_group_avg_from_db', {
          params: {
            field_name: fieldName
          }
        });

        // 判断后端返回的状态码
        if (res.data.code === 200) {
          // 从后端返回的data中分离出created_at和年龄段平均值
          const { created_at, ...averages } = res.data.data;
          this.chartData = averages; // 保存年龄段平均值数据
          this.latestDataTimestamp = created_at; // 保存时间戳
          // 渲染图表
          this.renderChart();
          ElMessage.success('成功获取数据');
        } else if (res.data.code === 404) {
           // 如果未找到数据，清空图表并提示
           this.chartData = {};
           this.latestDataTimestamp = null; // 清空时间戳
           this.renderChart(); // 渲染空图表
           ElMessage.warning('未找到该字段的年龄段平均值数据，请先计算');
        } else {
          // 如果后端返回其他错误，弹出错误提示
          ElMessage.error('获取数据失败: ' + res.data.msg);
        }
      } catch (error) {
        // 如果请求异常，弹出错误提示
        ElMessage.error('获取数据失败: ' + error.message);
      } finally {
        // 无论成功失败，都将加载状态设为false
        this.isLoading = false;
      }
    },

    // 计算最新平均值并存储到数据库
    async calculateLatestAvg() {
      this.isCalculating = true;
      ElMessage.info('正在计算最新平均值...');

      try {
        // 发送GET请求到后端触发计算和存储操作
        const res = await axios.get('/data/calculate_and_store_age_group_avg', {
           params: {
            field_name: this.currentField // 传递当前选中的字段
          }
        });

        // 判断后端返回的状态码
        if (res.data.code === 200) { // 假设后端计算成功返回200
          ElMessage.success('最新平均值计算并存储成功！');
          // 计算成功后，重新从数据库获取最新数据并更新图表
          this.fetchData(this.currentField);
        } else {
          // 如果后端返回错误，弹出错误提示
          ElMessage.error('计算最新平均值失败: ' + res.data.msg);
        }
      } catch (error) {
        // 如果请求异常，弹出错误提示
        ElMessage.error('计算最新平均值失败: ' + error.message);
      } finally {
        // 无论成功失败，都将计算状态设为false
        this.isCalculating = false;
      }
    },

    // 渲染折线图
    renderChart() {
      if (!this.chartInstance) {
        this.initChart();
      }

      // 准备x轴数据（年龄段）
      const xData = Object.keys(this.chartData);

      // 准备y轴数据（平均值）
      const yData = xData.map(key => this.chartData[key]);

      // 配置echarts的option
      const option = {
        title: {
          text: `各年龄段${this.fieldNames[this.currentField]}平均值`,
          left: 'center'
        },
        tooltip: {
          trigger: 'axis',
          // 格式化tooltip显示，处理可能为null的值
          formatter: function(params) {
             const param = params[0];
             return param.name + ': ' + (param.value !== null ? Number(param.value).toFixed(2) : 'N/A');
          }
        },
        xAxis: {
          type: 'category',
          data: xData,
          name: '年龄段',
          nameLocation: 'middle',
          nameGap: 30,
          axisLabel: {
            interval: 0  // 强制显示所有标签
          }
        },
        yAxis: {
          type: 'value',
          name: '平均值',
          nameLocation: 'middle',
          nameGap: 40,
           // 确保y轴从0开始，避免数据波动看起来过大
          min: 0
        },
        grid: {
          left: '5%',
          right: '5%',
          bottom: '10%',
          top: '15%',
          containLabel: true
        },
        series: [
          {
            name: this.fieldNames[this.currentField],
            type: 'line',
            data: yData,
            smooth: true,  // 平滑曲线
            lineStyle: {
              width: 3  // 线条粗细
            },
            itemStyle: {
              color: '#409EFF'  // 数据点颜色
            },
            // 在数据点显示数值
            label: {
              show: true,
              position: 'top',
              formatter: function(params) {
                // 保留两位小数，处理可能为null的值
                return params.value !== null ? Number(params.value).toFixed(2) : 'N/A';
              }
            },
            // 区域填充
            areaStyle: {
              color: { // 渐变色
                type: 'linear',
                x: 0,
                y: 0,
                x2: 0,
                y2: 1,
                colorStops: [
                  {
                    offset: 0,
                    color: 'rgba(64, 158, 255, 0.5)'  // 渐变起始颜色
                  },
                  {
                    offset: 1,
                    color: 'rgba(64, 158, 255, 0.1)'  // 渐变结束颜色
                  }
                ]
              }
            }
          }
        ]
      };

      // 设置option并渲染
      this.chartInstance.setOption(option);
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

/* 居中标题样式 */
.center-title {
  text-align: center;
  margin-bottom: 20px;
}

/* 按钮组样式 */
.button-group {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
  margin-bottom: 20px; /* 调整间距 */
}

/* 数据时间显示样式 */
.timestamp-display {
  text-align: center;
  margin-bottom: 20px;
  font-size: 0.9em;
  color: #606266;
}

/* 计算按钮容器样式，用于居中 */
.calculate-button-container {
  display: flex;
  justify-content: center;
  margin-bottom: 30px;
}

/* 折线图容器样式 */
.chart-box {
  width: 100%;
  height: 500px;
  margin: 0 auto;
}
</style>