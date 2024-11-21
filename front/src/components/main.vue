<script>
import {HomeFilled, List, UserFilled} from "@element-plus/icons-vue";
import axios from "axios";

export default {
  components: {List, UserFilled, HomeFilled},
  data() {
    return {
      //账号id
      account: '',
      //搜索框的输入
      searchQuery: '',
      //搜索的类型，比如学名搜索，描述搜索等
      searchStatus: {
        S: 'S', //即学名搜索
        D: 'D'  //即描述搜索
      },
      //存储搜索结果
      searchResults: [
        {
          //俗名
          Common_name : "蟑螂",
          //中文学名
          Chinese_name : "蜚蠊",
          //拉丁文学名
          Latin_name : "Blattodea",
          //别名
          Alias_name : "黄嚓、曱甴、小强、黄婆娘、偷油婆、鞋板虫、油灶婆、滑虫",
          //界门纲目科属种依次：
          Kingdom : "",
          Phylum : "",
          Class : "",
          Order : "",
          Family : "",
          Genus : "",
          Species : "",
          othertax : [
            //   总/超，亚，次/下的各种分类，可有可无，总:super-;亚:sub;次/下:infra
            {
              tax : "六足亚门"
            },
//未完成
          ]
        },

      ]
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

    //标准搜索，即学名，拉丁文搜索
    async standardSearch(status) {
      try {
        const response = await axios.get('url', {
          params: {
            query: this.searchQuery,
            status: status
          }
        });
        this.searchResults = response.data.results; // 假定 API 返回结果在 data.results
      } catch (error) {
        console.error('搜索失败:', error);
      }
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
      <div>
        <el-input
            v-model="searchQuery"
            placeholder="输入关键词搜索昆虫"
            @keyup.enter.native="standardSearch(this.searchStatus.S)"
            clearable>
        </el-input>
        <el-button @click="standardSearch">搜索</el-button>
      </div>

      <el-list>
        <template v-for="(item, index) in searchResults" :key="index">
          <el-card>
            <h3>{{ item.name }}</h3>
            <p>{{ item.description }}</p>
            <!-- 假设 item 对象有 'name' 和 'description' 属性，可以根据实际数据结构修改 -->
          </el-card>
        </template>
      </el-list>

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

.el-input, .el-button {
  margin-right: 10px;
}

.el-card {
  margin-bottom: 20px;
}

</style>
