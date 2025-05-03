import { createApp } from 'vue'; // 导入Vue的createApp方法
import App from './App.vue'; // 导入根组件
import Axios from 'axios'; // 导入axios用于HTTP请求

// 设置 Axios 的默认基础 URL
Axios.defaults.baseURL = '/api'; // API 基础路径（根据需要修改）

// 引入 Vue Router
import router from './router';

// 引入 ElementPlus UI 库及样式
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

// 导入 ECharts 主模块
import * as echarts from 'echarts'; // 这里导入echarts

const app = createApp(App);

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}
// 全局注册 Axios
// 通过 app.config.globalProperties 将 Axios 注入到 Vue 实例中
app.config.globalProperties.$axios = Axios; // 这样就可以在任何组件中通过 this.$axios 访问 Axios 实例

// 全局注册 ECharts
app.config.globalProperties.$echarts = echarts; // 这样就可以在任何组件中通过 this.$echarts 访问 ECharts 实例

// 使用 Vue Router
app.use(router);

// 使用 ElementPlus 组件库
app.use(ElementPlus);

// 挂载 Vue 实例到页面上的 #app 元素
app.mount('#app');
