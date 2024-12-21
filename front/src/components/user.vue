<script>
import {HomeFilled, List, UserFilled} from "@element-plus/icons-vue";
import axios from "axios";
import wikipedia from "wikipedia";
import {ElMessage} from "element-plus"; // 引入wikipedia模块

export default {
  components: {List, UserFilled, HomeFilled},
  data() {
    return {
      //账号id
      account: '',
      //搜索框的输入
      searchQuery: '',
      //搜索的类型，比如学名搜索，描述搜索等,S代表标准（学名搜索），I代表图片搜索，A代表AI搜索
      searchType: 'exact',
      searchStatus: {
        S: "S",
        I: "I",
        A: "A",
      },
      searchResult: "", // 原始搜索结果
      truncatedResult: "", // 截取后的搜索结果
      user:{
        account:'Emdiso717',
        email:'111111111@email.com'
      },
    }
  },
  created() {
    this.account = this.$route.query.account;
    this.get_em();
    wikipedia.setLang("zh");
  },

  methods: {
    get_em(){
      axios.post("/get_account",
          {
            account:this.account,
          }).then(response => {
        this.user = response.data;
      })
    },
    changeRoute(path) {
      const currentRoute = this.$route;
      this.$router.push({
        path: path,
        query: currentRoute.query
      });
    },

    //搜索
    async Search() {
      try {
        if (!this.searchQuery) {
          this.searchResult = "请输入搜索关键词！";
          this.truncatedResult = "";
          return;
        }

        // 调用 API 并获取数据
        const response = await wikipedia.page(this.searchQuery);
        const summary = await response.summary();
        this.searchResult = summary.extract; // 原始结果
        this.truncatedResult = this.getFirstLines(summary.extract, 3); // 截取前三行
      } catch (error) {
        if (error.name === "PageError") {
          this.searchResult = "未找到相关内容，请尝试其他关键词。";
        } else if (error.name === "DisambiguationError") {
          this.searchResult = "关键词过于模糊，请尝试更具体的搜索内容。";
        } else {
          this.searchResult = `搜索失败：${error.message}`;
        }
        this.truncatedResult = ""; // 确保失败时不显示内容
      }
    },
    //截取前三行
    getFirstLines(text, numLines) {
      return text
          .split("\n") // 按换行符分割
          .slice(0, numLines) // 截取前 numLines 行
          .join("\n"); // 再拼接回字符串
    },
    goToDetailPage(item) {
      // 跳转到详情页面
      this.$router.push({
        path: '/result',
        query: {searchQuery: this.searchQuery},
      });
    },
    quit(){
      this.$router.push({
        path: '/login',
      });
    }
  },

}
</script>

<template>
  <el-container class="all">
    <el-header class="header">
      <p class="title">Insert Lens</p>
    </el-header>
    <el-aside class="aside">
      <el-menu default-active="1" class="el-menu-vertical-demo" :router="true">
        <el-menu-item @click="changeRoute('/main')" index="1" class="icon">
          <el-icon style="color: #244a31">
            <HomeFilled/>
          </el-icon>
          <template #title>搜索</template>
        </el-menu-item>
        <el-menu-item @click="changeRoute('/tree')" index="2" class="icon">
          <el-icon style="color: #244a31">
            <List/>
          </el-icon>
          <template #title>昆虫树状图</template>
        </el-menu-item>
        <el-menu-item @click="changeRoute('/user')" index="3" class="icon">
          <el-icon style="color: #244a31">
            <UserFilled/>
          </el-icon>
          <template #title>个人信息</template>
        </el-menu-item>
      </el-menu>
    </el-aside>
   <el-main class="main">
<!--      <img class="background" src="./icons/cool-background%20.svg" alt="Description" />-->
      <div class="card">
        <p class="font">Userinfo</p>
        <el-avatar
            src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png" class="avatar"
        />
        <p class="form_font po1">用户名：{{user.account}}</p>
        <p class="form_font po1 po2">用户名：{{user.email}}</p>
        <el-divider class="divider" />
        <div class="down" >
          <el-scrollbar >
          <div class="down2"  >

          </div>
          </el-scrollbar>
          <p class="text mat">注册时间：{{user.date_joined}}</p>
          <el-button  class="card_button" @click="quit()">
            <span class="text_button">退出登录</span>
          </el-button>
        </div>
      </div>
    </el-main>
  </el-container>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet');
.form_font{
  font-family: 'Montserrat', sans-serif;
  color: #000000;
  font-size: 20px;
  font-style: italic;
  font-weight: 900;
  letter-spacing: 2px;
}
  .mat{
    margin-top: 10px;
  }
.text{
  font-family: 'Montserrat', sans-serif;
  color: #000000;
  font-size: 13px;
  font-style: italic;
  font-weight: 600;
  letter-spacing: 2px;
}
.down{
  position: relative;

  top:-70px;
  width: 80%;
  margin-left: 10%;
  height: 58%;
}
.down2{
  margin-top: 10px;
}
.divider{
  position: relative;
  top:-80px;
  margin-left: 10%;
  width: 80%;
}
.po1{
  position: relative;
  top:-80px;
  left: 200px;
}
.po2{
  margin-top: 10px;
}

.avatar{
  margin-left: 60px;
  margin-top: 30px;
  height: 80px;
  width: auto;
}
.all {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: #ffffff;
}

.header {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 8vh;
  background-image: url("./icons/low-poly-grid-haikei.svg");
}

.title {
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

.aside {
  position: absolute;
  top: 8vh;
  left: 0;
  height: 92vh;
  width: 7vw;
}

.el-menu-vertical-demo {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;

}

.icon {
  margin-top: 20%;
  margin-left: -10px;
  color: #429561 !important;
  font-weight: bolder;
}

.main {
  position: absolute;
  top: 8vh;
  left: 7vw;
  width: 93%;
  height: 92%;
}

.main > div {
  margin-bottom: 20px;
}

.card{
  position:relative;
  margin-left: 10%;
  width: 80%;
  height: 100%;
  transition: box-shadow 0.3s ease-in-out;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
  z-index: 1;
  background-color: rgba(255, 255, 255, 0.5);
}
.card:hover {
  box-shadow: 0 16px 32px rgba(0, 0, 0, 0.4);
}

.font{
  font-family: 'Montserrat', sans-serif;
  color: #36714a;
  font-size: 30px;
  font-style: italic;
  font-weight: 900;
  letter-spacing: 2px;
  text-align: center;
}
.card_button {
  background-color: #244a31;
  width: 80px;
  margin-top: 10px;
  border-radius: 8px;
  border: 1px solid #36714a;
  box-shadow: 0 2px 10px rgb(10, 64, 165,0.2);
  transition: .2s;
  color: #f5f7f8;
  margin-left: 1000px;
}
.card_button:active,
.card_button:focus,
.card_button:hover {
  background-color: #ffffff;
  transition: box-shadow 0.3s ease;
  color: #3f6a53;
  border-color: #429561;
  box-shadow: 0 4px 16px rgb(94, 159, 116);
  border-width: 3px;
}
.text_button{
  font-family: 'Montserrat', sans-serif;
  font-size: 14px;
  font-style: italic;
  font-weight: 900;
  letter-spacing: 2px;
}
</style>
