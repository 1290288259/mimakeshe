<script setup>
import { ref } from 'vue';  // 确保引入 ref


const tableData = ref([
  { date: '2021-01-01', name: 'Tom', address: 'No. 1198, 100 Feet Road, Chaoyang District, Beijing' },

]);
</script>

<template>
<div>
  <el-scrollbar>
    <el-table :data="tableData">
      <el-table-column prop="date" label="Date" width="140" />
      <el-table-column prop="name" label="Name" width="120" />
      <el-table-column prop="address" label="Address" />
    </el-table>
  </el-scrollbar>
</div>
</template>

<style scoped>

</style>