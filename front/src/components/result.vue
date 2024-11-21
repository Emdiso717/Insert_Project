<script >
import {HomeFilled, List, UserFilled} from "@element-plus/icons-vue";
import axios from "axios";
export default {
  components: {List,  UserFilled, HomeFilled},
  data(){
    return{
      account:'',
    }

  },
  created() {
    this.account = this.$route.query.account;
  },
  methods: {
    changeRoute(path) {
      const currentRoute = this.$route;
      this.$router.push({
        path: path,
        query: currentRoute.query
      });
    },
  },

}
</script>

<template>
    <el-container class="all">
      <el-header class="header">
        <p class="title">Insert Lens</p>
      </el-header>
      <el-aside  class="aside" >
        <el-menu default-active="1" class="el-menu-vertical-demo" :router="true">
          <el-menu-item  @click="changeRoute('/main')" index="1" class="icon">
            <el-icon style="color: #244a31"><HomeFilled /></el-icon>
            <template #title>搜索</template>
          </el-menu-item>
          <el-menu-item @click="changeRoute('/tree')" index="2" class="icon">
            <el-icon style="color: #244a31"><List /></el-icon>
            <template #title>昆虫树状图</template>
          </el-menu-item>
          <el-menu-item @click="changeRoute('/user')" index="3" class="icon">
            <el-icon style="color: #244a31"><UserFilled /></el-icon>
            <template #title>个人信息</template>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-main class="main">
        <!--   TODO     代码添加在这里-->


      </el-main>
    </el-container>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet');
.all{
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
.header{
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 8vh;
  background-image: url("./icons/low-poly-grid-haikei.svg");
}
.title{
  font-family: 'Montserrat', sans-serif;
  color: #ffffff;
  font-size: 330%;
  margin-left: 700px;
  font-style: italic;
  font-weight: 900;
  letter-spacing: 2px;
  margin-bottom: 1%;
  margin-top: -10px;
}
.aside{
  position: absolute;
  top: 8vh;
  left: 0;
  height: 92vh;
  width: 7vw;
}
.el-menu-vertical-demo{
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;

}
.icon{
  margin-top: 20%;
  margin-left: -10px;
  color: #429561 !important;
  font-weight: bolder;
}
.main{
  position: absolute;
  top: 8vh;
  left: 7vw;
  width: 93%;
  height: 92%;
}


</style>