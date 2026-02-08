<template>
  <div class="data-page-container">
    <el-card class="medical-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <div class="header-title">
            <span class="dot primary"></span>
            <h3>平均值分析统计</h3>
          </div>
          <div class="header-meta" v-if="createdAt">
            <el-tag type="info" size="small" effect="plain">
              <el-icon><Clock /></el-icon> 数据时间：{{ createdAt }}
            </el-tag>
          </div>
        </div>
      </template>

      <!-- 密钥选择与操作区 -->
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
            type="primary" 
            :loading="isCalculating" 
            @click="calculateNewAverage"
            icon="Refresh"
            round
          >
            {{ isCalculating ? '正在计算...' : '计算最新平均值' }}
          </el-button>
        </div>
      </div>

      <!-- 内容区：表格与图表 -->
      <div class="content-layout">
        <div class="table-section">
          <div class="section-label">指标列表</div>
          <el-table 
            :data="averagesData" 
            style="width: 100%" 
            border 
            stripe
            :header-cell-style="{background: '#f5f7fa', color: '#606266', fontWeight: 'bold'}"
            height="450"
          >
            <el-table-column prop="field" label="检测指标" width="140" align="center">
              <template #default="scope">
                <span class="field-name">{{ scope.row.field }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="value" label="平均数值" align="center">
              <template #default="scope">
                <span class="value-text">{{ scope.row.value }}</span>
              </template>
            </el-table-column>
          </el-table>
        </div>

        <div class="chart-section">
          <div class="section-label">可视化分析</div>
          <div ref="chartRef" class="chart-box"></div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios';
import { ElMessage } from 'element-plus';
import { Clock, Refresh } from '@element-plus/icons-vue';

export default {
  name: 'DataAvgPage',
  components: {
    Clock,
    Refresh
  },
  data() {
    return {
      averagesData: [],
      rawAverages: {},
      createdAt: '',
      isCalculating: false,
      keypairNames: [],
      selectedKeyIndex: null,
      echartsInstance: null
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
    if (this.echartsInstance) {
      this.echartsInstance.dispose();
    }
    window.removeEventListener('resize', this.handleResize);
  },
  methods: {
    handleResize() {
      if (this.echartsInstance) {
        this.echartsInstance.resize();
      }
    },
    async fetchKeypairNames() {
      try {
        const res = await axios.get('/get_keypair_names');
        if (res.data.code === 200) {
          this.keypairNames = res.data.data;
          if (this.keypairNames.length > 0) {
            this.selectedKeyIndex = this.keypairNames[0].id;
            this.fetchAverages();
          }
        }
      } catch (error) {
        ElMessage.error('获取密钥列表失败');
      }
    },
    handleKeyChange() {
      this.fetchAverages();
    },
    async fetchAverages() {
      if (!this.selectedKeyIndex) return;
      
      try {
        let url = `/data/get_avg?group_id=${this.selectedKeyIndex}`;
        const res = await axios.get(url);
        if (res.data.code === 200) {
          this.createdAt = res.data.data.created_at || '';
          const pureData = { ...res.data.data };
          delete pureData.created_at;
          delete pureData.cirrhosis; // Remove unused field
          
          this.rawAverages = pureData;
          this.averagesData = Object.entries(pureData).map(([field, value]) => ({
            field: this.getFieldName(field),
            value: value
          }));
          
          this.$nextTick(() => {
            this.renderChart();
          });
        } else {
          ElMessage.error('获取平均值失败: ' + res.data.msg);
        }
      } catch (error) {
        ElMessage.error('获取平均值失败: ' + error.message);
      }
    },
    async calculateNewAverage() {
      if (!this.selectedKeyIndex) {
        ElMessage.warning('请先选择密钥组');
        return;
      }

      this.isCalculating = true;
      try {
        let url = `/data/calculate_avg?group_id=${this.selectedKeyIndex}`;
        const calcRes = await axios.get(url);
        
        if (calcRes.data.code === 200) {
          ElMessage.success('计算成功，正在更新数据...');
          await this.fetchAverages();
        } else {
          ElMessage.error('计算失败: ' + calcRes.data.msg);
        }
      } catch (error) {
        ElMessage.error('请求失败: ' + error.message);
      } finally {
        this.isCalculating = false;
      }
    },
    getFieldName(field) {
      const fieldNames = {
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
      return fieldNames[field] || field;
    },
    initChart() {
      this.echartsInstance = this.$echarts.init(this.$refs.chartRef);
    },
    renderChart() {
      if (!this.echartsInstance) {
        this.initChart();
      }
      const xData = [];
      const yData = [];
      for (const [field, value] of Object.entries(this.rawAverages)) {
        xData.push(this.getFieldName(field));
        yData.push(typeof value === 'string' ? parseFloat(value) : value);
      }

      const option = {
        title: {
          show: false
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: { type: 'shadow' }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '10%',
          top: '10%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: xData,
          axisLine: { lineStyle: { color: '#ccc' } },
          axisLabel: { color: '#606266', interval: 0, rotate: 30 }
        },
        yAxis: {
          type: 'value',
          splitLine: { lineStyle: { type: 'dashed', color: '#eee' } }
        },
        series: [
          {
            name: '平均值',
            type: 'bar',
            data: yData,
            barWidth: '40%',
            itemStyle: {
              color: {
                type: 'linear',
                x: 0, y: 0, x2: 0, y2: 1,
                colorStops: [
                  { offset: 0, color: '#005EB8' }, // NHS Blue
                  { offset: 1, color: '#41B6E6' }  // Light Blue
                ]
              },
              borderRadius: [4, 4, 0, 0]
            },
            label: {
              show: true,
              position: 'top',
              formatter: (params) => Number(params.value).toFixed(2),
              color: '#005EB8',
              fontWeight: 'bold'
            }
          }
        ]
      };
      this.echartsInstance.setOption(option);
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

.dot.primary {
  background-color: var(--medical-primary);
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

.content-layout {
  display: flex;
  gap: 24px;
  height: 500px;
}

.table-section {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.chart-section {
  flex: 2;
  display: flex;
  flex-direction: column;
  background-color: #fcfcfc;
  border-radius: 8px;
  border: 1px solid #ebeef5;
  padding: 16px;
}

.section-label {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 12px;
  border-left: 3px solid var(--medical-secondary);
  padding-left: 8px;
}

.chart-box {
  width: 100%;
  flex: 1;
}

.field-name {
  font-weight: 500;
}

.value-text {
  font-family: monospace;
  color: var(--medical-primary);
  font-weight: bold;
}
</style>