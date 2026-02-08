<template>
  <div class="data-page-container">
    <el-card class="medical-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <div class="header-title">
            <span class="dot warning"></span>
            <h3>年龄段指标趋势</h3>
          </div>
          <div class="header-meta" v-if="latestDataTimestamp">
            <el-tag type="info" size="small" effect="plain">
              <el-icon><Clock /></el-icon> 数据时间：{{ latestDataTimestamp }}
            </el-tag>
          </div>
        </div>
      </template>

      <!-- 操作区 -->
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
            type="warning" 
            :loading="isCalculating" 
            @click="calculateLatestAvg"
            icon="TrendCharts"
            round
            plain
          >
            {{ isCalculating ? '计算中...' : '计算最新趋势' }}
          </el-button>
        </div>
      </div>

      <!-- 指标切换 -->
      <div class="field-tabs">
        <el-radio-group v-model="currentField" @change="changeField" size="large">
          <el-radio-button 
            v-for="(name, field) in fieldNames"
            :key="field"
            :label="field"
          >
            {{ name }}
          </el-radio-button>
        </el-radio-group>
      </div>

      <!-- 图表容器 -->
      <div class="chart-container" v-loading="isLoading">
        <div ref="chartRef" class="chart-box"></div>
      </div>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios';
import { ElMessage } from 'element-plus';
import { Clock, TrendCharts } from '@element-plus/icons-vue';

export default {
  name: 'AgeAvgPage',
  components: {
    Clock,
    TrendCharts
  },
  data() {
    return {
      currentField: 'cholesterol',
      isLoading: false,
      isCalculating: false,
      chartData: {},
      latestDataTimestamp: null,
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
      chartInstance: null,
      keypairNames: [],
      selectedKeyIndex: null
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
    if (this.chartInstance) {
      this.chartInstance.dispose();
      this.chartInstance = null;
    }
    window.removeEventListener('resize', this.handleResize);
  },
  methods: {
    handleResize() {
      if (this.chartInstance) {
        this.chartInstance.resize();
      }
    },
    async fetchKeypairNames() {
      try {
        const res = await axios.get('/get_keypair_names');
        if (res.data.code === 200) {
          this.keypairNames = res.data.data;
          if (this.keypairNames.length > 0) {
            this.selectedKeyIndex = this.keypairNames[0].id;
            this.fetchData(this.currentField);
          }
        }
      } catch (error) {
        ElMessage.error('获取密钥列表失败');
      }
    },
    handleKeyChange() {
      this.fetchData(this.currentField);
    },
    initChart() {
      this.chartInstance = this.$echarts.init(this.$refs.chartRef);
    },
    changeField(field) {
      if (this.currentField !== field) {
        this.currentField = field;
        this.fetchData(field);
      }
    },
    async fetchData(fieldName) {
      if (!this.selectedKeyIndex) return;
      this.isLoading = true;

      try {
        const res = await axios.get('/data/get_age_group_avg_from_db', {
          params: {
            field_name: fieldName,
            group_id: this.selectedKeyIndex
          }
        });

        if (res.data.code === 200) {
          const { created_at, ...averages } = res.data.data;
          this.chartData = averages;
          this.latestDataTimestamp = created_at;
          this.renderChart();
        } else if (res.data.code === 404) {
           this.chartData = {};
           this.latestDataTimestamp = null;
           this.renderChart();
           ElMessage.warning('未找到该字段的年龄段平均值数据，请先计算');
        } else {
          ElMessage.error('获取数据失败: ' + res.data.msg);
        }
      } catch (error) {
        ElMessage.error('获取数据失败: ' + error.message);
      } finally {
        this.isLoading = false;
      }
    },
    async calculateLatestAvg() {
      if (!this.selectedKeyIndex) {
        ElMessage.warning('请先选择密钥组');
        return;
      }

      this.isCalculating = true;
      try {
        const res = await axios.get('/data/calculate_and_store_age_group_avg', {
           params: {
            field_name: this.currentField,
            group_id: this.selectedKeyIndex
          }
        });

        if (res.data.code === 200) {
          ElMessage.success('最新平均值计算并存储成功！');
          this.fetchData(this.currentField);
        } else {
          ElMessage.error('计算最新平均值失败: ' + res.data.msg);
        }
      } catch (error) {
        ElMessage.error('计算最新平均值失败: ' + error.message);
      } finally {
        this.isCalculating = false;
      }
    },
    renderChart() {
      if (!this.chartInstance) {
        this.initChart();
      }

      const xData = Object.keys(this.chartData);
      const yData = xData.map(key => this.chartData[key]);

      const option = {
        title: {
          show: false
        },
        tooltip: {
          trigger: 'axis',
          formatter: function(params) {
             const param = params[0];
             return param.name + ': ' + (param.value !== null ? Number(param.value).toFixed(2) : 'N/A');
          }
        },
        xAxis: {
          type: 'category',
          data: xData,
          name: '年龄段',
          nameLocation: 'end',
          nameGap: 10,
          axisLine: { lineStyle: { color: '#ccc' } },
          axisLabel: { color: '#606266', interval: 0 }
        },
        yAxis: {
          type: 'value',
          name: '平均值',
          splitLine: { lineStyle: { type: 'dashed', color: '#eee' } },
          min: 0
        },
        grid: {
          left: '3%',
          right: '5%',
          bottom: '5%',
          top: '10%',
          containLabel: true
        },
        series: [
          {
            name: this.fieldNames[this.currentField],
            type: 'line',
            data: yData,
            smooth: true,
            lineStyle: {
              width: 3,
              color: '#FFB81C' // Medical Warning Color (Amber) for trend
            },
            itemStyle: {
              color: '#FFB81C',
              borderWidth: 2,
              borderColor: '#fff'
            },
            label: {
              show: true,
              position: 'top',
              formatter: (params) => params.value !== null ? Number(params.value).toFixed(2) : 'N/A',
              color: '#FFB81C',
              fontWeight: 'bold'
            },
            areaStyle: {
              color: {
                type: 'linear',
                x: 0, y: 0, x2: 0, y2: 1,
                colorStops: [
                  { offset: 0, color: 'rgba(255, 184, 28, 0.4)' },
                  { offset: 1, color: 'rgba(255, 184, 28, 0.05)' }
                ]
              }
            }
          }
        ]
      };
      this.chartInstance.setOption(option);
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

.dot.warning {
  background-color: var(--medical-warning);
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

.field-tabs {
  margin-bottom: 24px;
  display: flex;
  justify-content: center;
}

.chart-container {
  padding: 20px 0;
  background-color: #fcfcfc;
  border-radius: 8px;
  border: 1px solid #ebeef5;
}

.chart-box {
  width: 100%;
  height: 500px;
}

/* Customize Radio Buttons to match theme */
:deep(.el-radio-button__inner) {
  border-radius: 4px !important;
  margin: 0 4px;
  border: 1px solid #dcdfe6;
  box-shadow: none !important;
}

:deep(.el-radio-button__original-radio:checked + .el-radio-button__inner) {
  background-color: var(--medical-warning);
  border-color: var(--medical-warning);
  color: #fff;
}
</style>