<template>
  <!-- 外层容器，设置样式 -->
  <div class="data-container">
    <!-- 标题 -->
    <h2 class="center-title">
      年龄分布统计
      <span v-if="createdAt" style="font-size:16px;color:#888;">（数据时间：{{ createdAt }}）</span>
    </h2>
    
    <!-- 操作栏：密钥组选择和计算按钮 -->
    <div class="operation-bar">
      <el-select v-model="selectedKeyIndex" placeholder="选择密钥组" style="width: 200px; margin-right: 20px;" @change="handleKeyChange">
        <el-option
          v-for="item in keypairNames"
          :key="item.id"
          :label="item.hospital_name"
          :value="item.id">
        </el-option>
      </el-select>
      
      <el-button 
        type="primary" 
        :loading="isCalculating" 
        @click="calculateNewDistribution"
      >
        {{ isCalculating ? '计算中...' : '计算最新分布' }}
      </el-button>
    </div>

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
      // 存储处理后的年龄分布数据
      ageDistribution: {},
      // 密钥组列表
      keypairNames: [],
      // 当前选中的密钥组索引
      selectedKeyIndex: null,
      // 是否正在计算
      isCalculating: false,
      // 数据创建时间
      createdAt: '',
      // echarts实例
      pieChartInstance: null
    };
  },
  // 组件创建时获取密钥列表
  created() {
    this.fetchKeypairNames();
  },
  mounted() {
    // 组件挂载后初始化echarts实例
    this.initChart();
  },
  methods: {
    // 获取密钥组列表
    async fetchKeypairNames() {
      try {
        const res = await axios.get('/get_keypair_names');
        if (res.data.code === 200) {
          this.keypairNames = res.data.data;
          // 默认选中第一个
          if (this.keypairNames.length > 0) {
            this.selectedKeyIndex = this.keypairNames[0].id;
            this.fetchData(); // 选中后再获取数据
          }
        }
      } catch (error) {
        ElMessage.error('获取密钥列表失败');
      }
    },

    // 处理密钥切换
    handleKeyChange() {
      this.fetchData();
    },

    // 计算最新分布
    async calculateNewDistribution() {
      if (!this.selectedKeyIndex) {
        ElMessage.warning('请先选择密钥组');
        return;
      }
      
      this.isCalculating = true;
      try {
        const res = await axios.get('/data/calculate_age_distribution', {
          params: { group_id: this.selectedKeyIndex }
        });
        
        if (res.data.code === 200) {
          ElMessage.success('计算成功，正在获取最新数据...');
          await this.fetchData();
        } else {
          ElMessage.error('计算失败: ' + res.data.msg);
        }
      } catch (error) {
        ElMessage.error('请求失败: ' + error.message);
      } finally {
        this.isCalculating = false;
      }
    },

    // 异步方法：从后端获取数据
    async fetchData() {
      if (!this.selectedKeyIndex) return;

      try {
        // 发送GET请求到后端接口获取年龄分布数据
        const res = await axios.get('/data/get_age_distribution', {
          params: { group_id: this.selectedKeyIndex }
        });
        
        // 判断后端返回的状态码
        if (res.data.code === 200) {
          const data = res.data.data;
          this.createdAt = data.created_at || '';
          
          // 移除 created_at 字段，保留分布数据
          const distData = { ...data };
          delete distData.created_at;
          
          this.ageDistribution = distData;
          
          // 数据获取后绘制图表
          this.$nextTick(() => {
            this.renderPieChart();
          });
        } else {
          // 如果是404，说明还没有数据
          if (res.data.code === 404) {
             ElMessage.info('暂无该组数据，请点击计算最新分布');
             this.ageDistribution = {};
             this.createdAt = '';
             this.renderPieChart();
          } else {
             ElMessage.error('获取数据失败: ' + res.data.msg);
          }
        }
      } catch (error) {
        // 如果请求异常，弹出错误提示
        ElMessage.error('获取数据失败: ' + error.message);
      }
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
    if (this.pieChartInstance) {
      window.removeEventListener('resize', this.pieChartInstance.resize);
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

/* 操作栏样式 */
.operation-bar {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 30px;
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