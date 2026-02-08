<template>
  <div class="head-container">
    <div class="nav-wrapper">
      <el-radio-group v-model="currentRoute" size="large" @change="handleNavChange">
        <el-radio-button label="/index/datast/avg">
          <el-icon class="btn-icon"><DataLine /></el-icon> 指标平均值
        </el-radio-button>
        <el-radio-button label="/index/datast/agedbt">
          <el-icon class="btn-icon"><PieChart /></el-icon> 年龄分布
        </el-radio-button>
        <el-radio-button label="/index/datast/ageavg">
          <el-icon class="btn-icon"><TrendCharts /></el-icon> 年龄趋势
        </el-radio-button>
      </el-radio-group>
    </div>
  </div>
</template>

<script>
import { DataLine, PieChart, TrendCharts } from '@element-plus/icons-vue'

export default {
  name: "DataStHead",
  components: {
    DataLine,
    PieChart,
    TrendCharts
  },
  data() {
    return {
      currentRoute: this.$route.path
    }
  },
  watch: {
    '$route.path'(val) {
      this.currentRoute = val;
    }
  },
  methods: {
    handleNavChange(val) {
      this.$router.push(val);
    }
  }
}
</script>

<style scoped>
.head-container {
  background: #fff;
  padding: 16px 24px;
  border-radius: 8px;
  box-shadow: var(--medical-card-shadow);
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.nav-wrapper {
  display: flex;
  gap: 16px;
}

.btn-icon {
  margin-right: 6px;
  vertical-align: middle;
}

:deep(.el-radio-button__inner) {
  border-radius: 4px !important;
  margin: 0 4px;
  border: 1px solid #dcdfe6;
  padding: 10px 24px;
  font-weight: 500;
  box-shadow: none !important;
}

:deep(.el-radio-button__original-radio:checked + .el-radio-button__inner) {
  background-color: var(--medical-primary);
  border-color: var(--medical-primary);
  box-shadow: none !important;
  color: #fff;
}

:deep(.el-radio-button:first-child .el-radio-button__inner),
:deep(.el-radio-button:last-child .el-radio-button__inner) {
  border-radius: 4px !important;
}
</style>