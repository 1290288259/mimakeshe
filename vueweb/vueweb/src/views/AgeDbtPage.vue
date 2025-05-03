<template>
  <!-- 外层容器，设置样式 -->
  <div class="data-container">
    <!-- 标题 -->
    <h2 class="center-title">年龄分布统计</h2>
    <!-- 图表容器 -->
    <div class="chart-container">
      <!-- 饼图容器 -->
      <div ref="pieChartRef" class="pie-chart"></div>
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
      // 存储从后端获取的数据
      rawData: [],
      // 存储处理后的年龄分布数据
      ageDistribution: {}
    };
  },
  // 组件创建时自动调用fetchData方法获取数据
  created() {
    this.fetchData();
  },
  mounted() {
    // 组件挂载后初始化echarts实例
    this.initChart();
  },
  methods: {
    // 异步方法：从后端获取数据
    async fetchData() {
      try {
        // 发送GET请求到后端接口获取所有年龄数据
        const res = await axios.get('/data/getallavg');
        // 判断后端返回的状态码
        if (res.data.code === 200) {
          // 保存原始数据 - 将数据转换为对象数组格式以便处理
          this.rawData = res.data.data.map((age, index) => {
            return { id: index + 1, age: age };
          });
          // 处理数据，计算年龄分布
          this.processAgeData();
          // 数据获取后绘制图表
          this.$nextTick(() => {
            this.renderPieChart();
          });
        } else {
          // 如果后端返回错误，弹出错误提示
          ElMessage.error('获取数据失败: ' + res.data.msg);
        }
      } catch (error) {
        // 如果请求异常，弹出错误提示
        ElMessage.error('获取数据失败: ' + error.message);
      }
    },
    
    // 处理年龄数据，按10岁为单位分组
    processAgeData() {
      // 初始化年龄分布对象
      const ageGroups = {
        '0-9岁': 0,
        '10-19岁': 0,
        '20-29岁': 0,
        '30-39岁': 0,
        '40-49岁': 0,
        '50-59岁': 0,
        '60-69岁': 0,
        '70-79岁': 0,
        '80岁以上': 0
      };
      
      // 遍历原始数据，统计各年龄段人数
      this.rawData.forEach(item => {
        // 获取年龄值
        const age = parseFloat(item.age);
        
        // 根据年龄值分配到对应的年龄组
        if (age < 10) {
          ageGroups['0-9岁']++;
        } else if (age < 20) {
          ageGroups['10-19岁']++;
        } else if (age < 30) {
          ageGroups['20-29岁']++;
        } else if (age < 40) {
          ageGroups['30-39岁']++;
        } else if (age < 50) {
          ageGroups['40-49岁']++;
        } else if (age < 60) {
          ageGroups['50-59岁']++;
        } else if (age < 70) {
          ageGroups['60-69岁']++;
        } else if (age < 80) {
          ageGroups['70-79岁']++;
        } else {
          ageGroups['80岁以上']++;
        }
      });
      
      // 保存处理后的年龄分布数据
      this.ageDistribution = ageGroups;
    },
    
    // 初始化echarts实例
    initChart() {
      // 获取echarts实例（已在main.js全局挂载）
      this.pieChartInstance = this.$echarts.init(this.$refs.pieChartRef);
    },
    
    // 渲染饼图
    renderPieChart() {
      if (!this.pieChartInstance) {
        this.initChart();
      }
      
      // 准备饼图数据
      const pieData = Object.entries(this.ageDistribution).map(([name, value]) => {
        return { name, value };
      });
      
      // 配置echarts的option
      const option = {
        title: {
          text: '年龄分布饼图',
          left: 'center'
        },
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b}: {c} ({d}%)' // 显示名称、数值和百分比
        },
        legend: {
          orient: 'vertical', // 垂直布局
          left: 'left',       // 位于左侧
          data: Object.keys(this.ageDistribution)
        },
        series: [
          {
            name: '年龄分布',
            type: 'pie',
            radius: ['40%', '70%'], // 环形饼图的内外半径
            avoidLabelOverlap: true,
            itemStyle: {
              borderRadius: 10, // 圆角
              borderColor: '#fff',
              borderWidth: 2
            },
            label: {
              show: true,
              formatter: '{b}: {c} ({d}%)' // 显示名称、数值和百分比
            },
            emphasis: {
              label: {
                show: true,
                fontSize: '16',
                fontWeight: 'bold'
              }
            },
            labelLine: {
              show: true
            },
            data: pieData,
            // 设置不同年龄段的颜色
            color: [
              '#5470c6', '#91cc75', '#fac858', '#ee6666', 
              '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc'
            ]
          }
        ]
      };
      
      // 设置option并渲染
      this.pieChartInstance.setOption(option);
      
      // 添加窗口大小变化的监听，自动调整图表大小
      window.addEventListener('resize', () => {
        this.pieChartInstance.resize();
      });
    }
  },
  // 组件销毁前移除事件监听
  beforeUnmount() {
    window.removeEventListener('resize', this.pieChartInstance.resize);
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

/* 图表容器样式 */
.chart-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

/* 饼图容器样式 */
.pie-chart {
  width: 800px;
  height: 500px;
  margin: 0 auto;
}

/* 居中标题样式 */
.center-title {
  text-align: center;
  margin-bottom: 30px;
}
</style>