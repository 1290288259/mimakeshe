<template>
  <div class="data-page-container">
    <el-card class="medical-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <div class="header-title">
            <span class="dot success"></span>
            <h3>年龄分布统计</h3>
          </div>
          <div class="header-meta" v-if="createdAt">
            <el-tag type="info" size="small" effect="plain">
              <el-icon><Clock /></el-icon> 数据时间：{{ createdAt }}
            </el-tag>
          </div>
        </div>
      </template>

      <!-- 操作栏 -->
      <div class="operation-bar">
        <div class="left-ops">
          <span class="label-text">密钥组选择：</span>
          <el-select v-model="selectedKeyIndex" placeholder="请选择密钥组" class="key-select" @change="handleKeyChange">
            <el-option
              v-for="item in keypairNames"
              :key="item.id"
              :label="item.hospital_name"
              :value="item.id">
            </el-option>
          </el-select>
        </div>
        <div class="right-ops">
          <el-button 
            type="success" 
            :loading="isCalculating" 
            @click="calculateNewDistribution"
            icon="PieChart"
            round
          >
            {{ isCalculating ? '计算中...' : '计算最新分布' }}
          </el-button>
        </div>
      </div>

      <!-- 图表容器 -->
      <div class="chart-container">
        <div ref="pieChartRef" class="pie-chart"></div>
      </div>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios';
import { ElMessage } from 'element-plus';
import { Clock, PieChart } from '@element-plus/icons-vue';

export default {
  name: 'AgeDbtPage',
  components: {
    Clock,
    PieChart
  },
  data() {
    return {
      ageDistribution: {},
      keypairNames: [],
      selectedKeyIndex: null,
      isCalculating: false,
      createdAt: '',
      pieChartInstance: null
    };
  },
  created() {
    this.fetchKeypairNames();
  },
  mounted() {
    this.initChart();
    window.addEventListener('resize', this.handleResize);
  },
  beforeUnmount() {
    if (this.pieChartInstance) {
      this.pieChartInstance.dispose();
    }
    window.removeEventListener('resize', this.handleResize);
  },
  methods: {
    handleResize() {
      if (this.pieChartInstance) {
        this.pieChartInstance.resize();
      }
    },
    async fetchKeypairNames() {
      try {
        const res = await axios.get('/get_keypair_names');
        if (res.data.code === 200) {
          this.keypairNames = res.data.data;
          if (this.keypairNames.length > 0) {
            this.selectedKeyIndex = this.keypairNames[0].id;
            this.fetchData();
          }
        }
      } catch (error) {
        ElMessage.error('获取密钥列表失败');
      }
    },
    handleKeyChange() {
      this.fetchData();
    },
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
    async fetchData() {
      if (!this.selectedKeyIndex) return;

      try {
        const res = await axios.get('/data/get_age_distribution', {
          params: { group_id: this.selectedKeyIndex }
        });
        
        if (res.data.code === 200) {
          const data = res.data.data;
          this.createdAt = data.created_at || '';
          
          const distData = { ...data };
          delete distData.created_at;
          
          this.ageDistribution = distData;
          
          this.$nextTick(() => {
            this.renderPieChart();
          });
        } else {
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
        ElMessage.error('获取数据失败: ' + error.message);
      }
    },
    initChart() {
      this.pieChartInstance = this.$echarts.init(this.$refs.pieChartRef);
    },
    renderPieChart() {
      if (!this.pieChartInstance) {
        this.initChart();
      }
      
      const pieData = Object.entries(this.ageDistribution).map(([name, value]) => {
        return { name, value };
      });
      
      const option = {
        title: {
          show: false
        },
        tooltip: {
          trigger: 'item',
          formatter: '{b}: {c} ({d}%)'
        },
        legend: {
          orient: 'vertical',
          left: 'left',
          top: 'center'
        },
        series: [
          {
            name: '年龄分布',
            type: 'pie',
            radius: ['40%', '70%'],
            center: ['50%', '50%'],
            avoidLabelOverlap: true,
            itemStyle: {
              borderRadius: 10,
              borderColor: '#fff',
              borderWidth: 2
            },
            label: {
              show: true,
              formatter: '{b}: {c}人'
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
            color: [
              '#005EB8', // NHS Blue
              '#41B6E6', // Light Blue
              '#009639', // NHS Green
              '#78BE20', // Lime
              '#FFB81C', // Amber
              '#DA291C', // Red
              '#8A1538', // Dark Red
              '#AE2573'  // Magenta
            ]
          }
        ]
      };
      
      this.pieChartInstance.setOption(option);
    }
  }
};
</script>

<style scoped>
.data-page-container {
  max-width: 100%;
}

.medical-card {
  border-radius: 8px;
  border: none;
  box-shadow: var(--medical-card-shadow);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.dot {
  width: 6px;
  height: 24px;
  border-radius: 3px;
}

.dot.success {
  background-color: var(--medical-success);
}

.header-title h3 {
  margin: 0;
  font-size: 18px;
  color: var(--medical-text);
  font-weight: 600;
}

.operation-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  background-color: #f8f9fa;
  padding: 16px;
  border-radius: 6px;
}

.left-ops {
  display: flex;
  align-items: center;
  gap: 10px;
}

.label-text {
  font-size: 14px;
  color: #606266;
}

.key-select {
  width: 240px;
}

.chart-container {
  display: flex;
  justify-content: center;
  padding: 20px 0;
  background-color: #fcfcfc;
  border-radius: 8px;
  border: 1px solid #ebeef5;
}

.pie-chart {
  width: 100%;
  max-width: 900px;
  height: 500px;
}
</style>