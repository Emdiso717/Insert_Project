<script>
import { HomeFilled, List, UserFilled } from "@element-plus/icons-vue";
import wikipedia from "wikipedia"; // 引入wikipedia模块

export default {
  components: { List, UserFilled, HomeFilled },
  data() {
    return {
      account: "",
      searchQuery: "", // 用户输入的搜索内容
      searchType: "exact", // 搜索类型，默认为精准搜索
      searchResult: "", // 原始搜索结果
      truncatedResult: "", // 截取后的搜索结果
    };
  },
  created() {
    this.account = this.$route.query.account;
    wikipedia.setLang("zh");
  },
  methods: {
    // 切换路由
    changeRoute(path) {
      const currentRoute = this.$route;
      this.$router.push({
        path: path,
        query: currentRoute.query,
      });
    },
    // 执行搜索
    async performSearch() {
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
    // 截取前三行文本的函数
    getFirstLines(text, numLines) {
      return text
        .split("\n") // 按换行符分割
        .slice(0, numLines) // 截取前 numLines 行
        .join("\n"); // 再拼接回字符串
    },
    // 跳转到详情页面
    viewFullResult() {
      this.$router.push({
        path: "/details",
        query: { searchQuery: this.searchQuery },
      });
    },
  },
};
</script>

<template>
  <el-container class="all">
    <el-header class="header">
      <p class="title">Insert Lens</p>
    </el-header>
    <el-aside class="aside">
      <el-menu default-active="1" class="el-menu-vertical-demo" :router="true">
        <el-menu-item @click="changeRoute('/searching')" index="1" class="icon">
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
      <!-- 搜索框 -->
      <div>
        <el-input
          v-model="searchQuery"
          placeholder="请输入搜索内容"
          style="width: 300px; margin-right: 10px;"
        />
        <el-select v-model="searchType" placeholder="搜索类型" style="width: 150px;">
          <el-option label="精准搜索" value="exact" />
          <el-option label="模糊搜索" value="fuzzy" />
        </el-select>
        <el-button type="primary" @click="performSearch">搜索</el-button>
      </div>
      <!-- 搜索结果展示 -->
      <div v-if="searchResult" style="margin-top: 20px;">
        <h3>搜索结果：</h3>
        <p>
          <a
            href="javascript:void(0);"
            style="text-decoration: underline; color: blue;"
            @click="viewFullResult"
          >
            {{ searchQuery }}
          </a>
        </p>
        <p style="color: #000000;">{{ truncatedResult }}</p>
      </div>

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
  background-color: #ffffff; /* 背景改为白色 */
  overflow: auto; /* 添加滚动条支持 */
  padding: 20px; /* 添加适当的内边距 */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 添加阴影提升视觉效果 */
  border-radius: 8px; /* 增加圆角设计 */
}

</style>
