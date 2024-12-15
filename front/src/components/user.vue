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
    }
  },
  created() {
    this.account = this.$route.query.account;
    wikipedia.setLang("zh");
  },
  methods: {
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
      <!--   TODO     代码添加在这里-->

    </el-main>
  </el-container>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet');

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

</style>
