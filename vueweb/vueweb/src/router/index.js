import { createRouter, createWebHistory } from 'vue-router';

import IndexPage from '@/views/IndexPage.vue';
import LoginPage from '@/views/LoginPage.vue';
import MainPage from '@/views/MainPage.vue';
import yuangongPage from '@/views/yuangongPage.vue'
import userPage from '@/views/userPage.vue';
import huowuPage from '@/views/huowuPage.vue';
import goumaiPage from '@/views/goumaiPage.vue';
import cartPage from "@/views/cartPage.vue";
import fahuoPage from "@/views/fahuoPage.vue";
import dingdanPage from "@/views/dingdanPage.vue";
import dataupPage from "@/views/dataupPage.vue";
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
                path: 'yonghu',  // 子路由的路径是相对于父路由的，省略前面的 '/index2'
                name: 'yonghu',
                component: yuangongPage,  // 对应的组件
            },
            {
                path: 'user',  // 子路由的路径是相对于父路由的，省略前面的 '/index2'
                name: 'user',
                component: userPage,  // 对应的组件
            },
            {
                path: 'huowu',  // 子路由的路径是相对于父路由的，省略前面的 '/index2'
                name: 'huowu',
                component: huowuPage,  // 对应的组件
            },
            {
                path: 'goumai',  // 子路由的路径是相对于父路由的，省略前面的 '/index2'
                name: 'goumai',
                component: goumaiPage,  // 对应的组件
            },
            {
                path: 'cart',  // 子路由的路径是相对于父路由的，省略前面的 '/index2'
                name: 'cart',
                component: cartPage,  // 对应的组件
            },
            {
                path: 'fahuo',  // 子路由的路径是相对于父路由的，省略前面的 '/index2'
                name: 'fahuo',
                component: fahuoPage,  // 对应的组件
            },
            {
                path: 'dingdan',  // 子路由的路径是相对于父路由的，省略前面的 '/index2'
                name: 'dingdan',
                component: dingdanPage,  // 对应的组件
            },
            {
                path: 'dataup',  // 子路由的路径是相对于父路由的，省略前面的 '/index2'
                name: 'dataup',
                component: dataupPage,  // 对应的组件
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
