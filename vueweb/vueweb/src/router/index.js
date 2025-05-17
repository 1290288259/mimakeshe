import { createRouter, createWebHistory } from 'vue-router';

import IndexPage from '@/views/IndexPage.vue';
import LoginPage from '@/views/LoginPage.vue';
import MainPage from '@/views/MainPage.vue';
import yuangongPage from '@/views/yuangongPage.vue'
import dataupPage from "@/views/dataupPage.vue";
import MyDataPage from '@/views/MyDataPage.vue';
import DataglPage from '@/views/DataglPage.vue';
import DataStPage from '@/views/DataStPage.vue';
import DataAvgPage from '@/views/DataAvgPage.vue'; // 已经引入
import AgeDbtPage from '@/views/AgeDbtPage.vue';
import AgeAvgPage from '@/views/AgeAvgPage.vue';
import DataAyPage from '@/views/DataAyPage.vue';
import TestPage from '@/views/TestPage.vue';

const routes = [
    {
        path: '/index',
        name: 'index',
        component: IndexPage,
        children: [
            {
                path: 'home',  // 子路由的路径是相对于父路由的，省略前面的 '/index2'
                name: 'home',
                component: MainPage,  // 对应的组件
            },
            {
                path: 'dataay',  // 子路由的路径是相对于父路由的，省略前面的 '/index2'
                name: 'dataay',
                component: DataAyPage,  // 对应的组件
            },
            {
                path: 'yonghu',  // 子路由的路径是相对于父路由的，省略前面的 '/index2'
                name: 'yonghu',
                component: yuangongPage,  // 对应的组件
            },
            {
                path: 'mydata',  // 子路由的路径是相对于父路由的，省略前面的 '/index2'
                name: 'mydata',
                component: MyDataPage,  // 对应的组件
            },
            {
                path: 'dataup',  // 子路由的路径是相对于父路由的，省略前面的 '/index2'
                name: 'dataup',
                component: dataupPage,  // 对应的组件
            },
            {
                path: 'datagl',  // 子路由的路径是相对于父路由的，省略前面的 '/index2'
                name: 'datagl',
                component: DataglPage,  // 对应的组件
            },
            {
                path: 'test',  // 子路由的路径是相对于父路由的，省略前面的 '/index2'
                name: 'test',
                component: TestPage,  // 对应的组件
            },
            {
                path: 'datast',  // 子路由的路径是相对于父路由的，省略前面的 '/index2'
                name: 'datast',
                component: DataStPage,  // 对应的组件
                children: [
                    {
                        path: 'avg', // 子路由路径 /index/datast/avg
                        name: 'dataavg',
                        component: DataAvgPage // 子页面组件
                    },
                    {
                        path: 'agedbt', // 子路由路径 /index/datast/avg
                        name: 'agedbt',
                        component: AgeDbtPage // 子页面组件
                    },
                    {
                        path: 'ageavg', // 子路由路径 /index/datast/avg
                        name: 'ageavg',
                        component: AgeAvgPage// 子页面组件
                    },
                ]
            },





        ]
    },
    {
        path: '/login',
        name: 'login',
        component: LoginPage
    },
    {
        path: '/',
        name: 'login',
        component: LoginPage
    },
    {
        path: '/main',
        name: 'main',
        component: MainPage,
    },
];

const router = createRouter({
    history: createWebHistory(), // 使用 HTML5 History 模式
    routes, // 路由配置
});

router.beforeEach((to, from, next) => {
    // 如果 URL 中没有更新标记（noUpdate），则进行正常导航
    if (to.query.noUpdate) {
        next(false)  // 阻止路由更新
    } else {
        next()  // 继续正常的路由导航
    }
});
// 全局前置守卫
router.beforeEach((to, from, next) => {
    // 如果访问的不是登录页面，并且 sessionStorage 中没有用户信息，重定向到登录页面
    const user = sessionStorage.getItem('User');

    if (to.name !== 'login' && !user) {
        next({ name: 'login' });  // 没有用户信息，跳转到登录页
    } else {
        next();  // 放行
    }
});

export default router;
