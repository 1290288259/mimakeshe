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
    
    <!-- 折线图容器 -->
    <div ref="chartRef" class="chart-box"></div>
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
      // 当前选中的字段
      currentField: 'cholesterol',
      // 是否正在加载数据
      isLoading: false,
      // 存储从后端获取的数据
      chartData: {},
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
        this.fetchData(field);
      }
    },
    
    // 从后端获取数据
    async fetchData(fieldName) {
      this.isLoading = true;
      
      try {
        // 发送GET请求到后端接口，传递字段名称参数
        const res = await axios.get('/data/get_avg_by_age_group', {
          params: {
            field_name: fieldName
          }
        });
        
        // 判断后端返回的状态码
        if (res.data.code === 200) {
          // 保存数据
          this.chartData = res.data.data;
          // 渲染图表
          this.renderChart();
        } else {
          // 如果后端返回错误，弹出错误提示
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
          formatter: '{b}: {c}'
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
          nameGap: 40
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
                // 保留两位小数
                return params.value !== null ? Number(params.value).toFixed(2) : 'N/A';
              }
            },
            // 区域填充
            areaStyle: {
              color: {
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
  margin-bottom: 30px;
}

/* 折线图容器样式 */
.chart-box {
  width: 100%;
  height: 500px;
  margin: 0 auto;
}
</style>