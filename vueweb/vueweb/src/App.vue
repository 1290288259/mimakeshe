<template>
<login></login>
  <div id="app">

  <router-view></router-view> <!-- 渲染匹配的路由组件 -->
</div>
</template>

<script>


export default {
  name: 'App',

}
</script>

<style>
body {
  margin: 0;
  padding: 0;
  height: 100%;
  overflow: hidden; /* 防止body出现滚动条，交由内部容器滚动 */
}
#app {
  height: 100%;
}
</style>
