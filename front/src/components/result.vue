<script>
import {HomeFilled, List, UserFilled} from "@element-plus/icons-vue";
import axios from "axios";
import wikipedia from "wikipedia";
import {ElMessage} from "element-plus";

export default {
  components: {List, UserFilled, HomeFilled},
  data() {
    return {
      //账号id
      account: '',
      //搜索框的输入
      searchQuery: '',
      loading: true,  // 控制loading状态
      //搜索的类型，比如学名搜索，描述搜索等,S代表标准（学名搜索），I代表图片搜索，A代表AI搜索
      insectData: null, // 用来存储后端返回的数据
      // insectData=[
      //   {
      //     "descriptionInfo": {
      //       "refs": [
      //         "吴燕如, 2000. 中国动物志 昆虫纲 第二十卷 膜翅目 准蜂科 蜜蜂科. 北京: 科学出版社. 442 页，218 图，9 图版"
      //       ],
      //       "descontent": "鉴别特征： 意大利蜂与中华蜜蜂的工蜂形态上的主要区别为：1．唇基黑色，不具黄或黄褐色斑；2．体较大，为12—14mm；体色变化大，深灰褐色至黄或黄褐色；3．后翅中脉不分叉(图208：b)。",
      //       "destitle": "Apis mellifera的形态描述"
      //     },
      //     "descriptionType": "形态描述"
      //   },
      //   {
      //     "descriptionInfo": {
      //       "refs": [
      //         "吴燕如, 2000. 中国动物志 昆虫纲 第二十卷 膜翅目 准蜂科 蜜蜂科. 北京: 科学出版社. 442 页，218 图，9 图版"
      //       ],
      //       "descontent": "体较大，为12—14mm；",
      //       "destitle": "Apis mellifera的大小"
      //     },
      //     "descriptionType": "大小"
      //   }
      // ]
      error: null, // 用来存储错误信息
      fullInformation: {
        summary: "",
        content: "",
        categories: [],
        images: [],
      },
      errorMessage: "", // 错误信息
    }
  },
  created() {
    this.searchQuery = this.$route.query.searchQuery;
    this.loading = true;
    this.fetchFullContent();
    wikipedia.setLang("zh"); // 设置为中文维基百科
    this.fetchWikipediaData();
    // 结束后更新loading状态
  },
  methods: {
    changeRoute(path) {
      const currentRoute = this.$route;
      this.$router.push({
        path: path,
        query: currentRoute.query
      });
    },
    async fetchFullContent() {
      try {
        // const response = await axios.get(url, { params });
        const response = await axios.get('/search_detail', {
          params: {
            // name: 'Culex pipiens',
            name: this.searchQuery,
            dbaseName: '中国动物志数据库',
            // dbaseName: '云南蝴蝶分布数据库',
            apiKey: '4541b8322a174f75b368cc269ea2d8fd'
          }
        })
        this.insectData = response.data.data; // 存储后端返回的数据
        // console.log(this.insectData);
        // console.log(this.insectData[0]);
      } catch (error) {
        if (error.response) {
          // 后端返回了错误信息
          this.error = error.response.data.error || "未知错误";
        } else {
          // 网络错误或请求配置错误
          this.error = "请求失败，请检查网络连接";
        }
      }
      this.loading = false;
    },
    async fetchWikipediaData() {
      this.errorMessage = ""; // 清空错误信息
      this.fullInformation = {
        summary: "",
        content: "",
        categories: [],
        images: [],
      };

      if (!this.searchQuery) {
        this.errorMessage = "请输入搜索关键词！";
        return;
      }

      try {
        // 调用 Wikipedia API 获取页面信息
        const response = await wikipedia.page(this.searchQuery);

        // 获取摘要信息
        const summary = await response.summary();
        const content = await response.content();
        const categories = (await response.categories()).map((cat) =>
            cat.replace(/^Category:/, "") // 去掉分类前缀
        );

        // 获取图片
        const rawImages = await response.images(); // 替换成可以直接获取 imageinfo 的方法
        const images = rawImages
            .map((img) => {
              const url = img.imageinfo[0]?.url || "";
              const descriptionUrl = img.imageinfo[0]?.descriptionurl || "";

              // 仅保留图片链接中包含 .jpg, .jpeg, .png 的 URL，过滤掉包含 svg 的链接
              if (/\.(jpg|jpeg|png)$/i.test(url)) {
                return {
                  url,
                  descriptionUrl,
                };
              }
              return null; // 如果不符合条件，则返回 null
            })
            .filter((img) => img !== null); // 删除 null 值

        console.log("Filtered Images with URLs:", images);

        // 存储数据
        this.fullInformation = {
          summary: summary.extract,
          content,
          categories,
          images,
        };

        console.log(this.fullInformation)
      } catch (error) {
        console.error(error);
        if (error.name === "PageError") {
          this.errorMessage = "未找到相关内容，请尝试其他关键词。";
        } else if (error.name === "DisambiguationError") {
          this.errorMessage = "关键词过于模糊，请尝试更具体的搜索内容。";
        } else {
          this.errorMessage = `搜索失败：${error.message}`;
        }
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

      <p style="font-size: 24px; font-weight: bold; color: #429561; text-align: left; margin-left: 20px;margin-top: 20px;">
        {{ searchQuery }} 搜索结果：
      </p>

      <template v-if="fullInformation">
        <!-- 搜索结果 -->
        <el-row style="margin-top: 20px;" v-if="fullInformation.summary">
          <!-- 图片 -->
          <el-col :span="24" v-if="fullInformation.images.length > 0">
            <el-card class="card" shadow="hover">
              <div class="card-header">
                <h3>图片展示</h3>
              </div>

              <div v-if="fullInformation.images.length" class="card-body">
                <el-row :gutter="20">
                  <el-col
                      v-for="(img, index) in fullInformation.images"
                      :key="index"
                      :span="6"
                      style="text-align: center;"
                  >
                    <!-- 图片 -->
                    <el-image
                        :src="img.url"
                        style="margin: 10px; width: 100%; height: auto;"
                        lazy
                        fit="contain"
                    />
                    <!-- 描述链接 -->
                    <!--                    <p v-if="img.descriptionUrl">-->
                    <!--                      <a :href="img.descriptionUrl" target="_blank" style="color: blue;">-->
                    <!--                        查看图片详情-->
                    <!--                      </a>-->
                    <!--                    </p>-->
                  </el-col>
                </el-row>
              </div>
              <p v-else>没有找到相关图片</p>
              <div class="card-footer">
                <p class="italic">维基百科</p>
              </div>
            </el-card>

          </el-col>

          <!-- 摘要 -->
          <el-col :span="24">
            <el-card class="card" shadow="hover">
              <div class="card-header">
                <h3>摘要</h3>
              </div>
              <div class="card-body">
                <p>{{ fullInformation.summary }}</p>
              </div>
              <div class="card-footer">
                <p class="italic">维基百科</p>
              </div>
            </el-card>
          </el-col>

        </el-row>
      </template>

      <template v-if="insectData">
        <div>
          <!-- 每行只显示一个卡片，设置 el-col 的 span 为 24 -->
          <el-row>
            <el-col :span="24" v-for="(item, index) in insectData" :key="index">
              <el-card class="card" shadow="hover">
                <!-- 卡片顶部显示 descriptionType -->
                <div class="card-header">
                  <h3>{{ item.descriptionType }}</h3>
                </div>
                <!-- 卡片主体显示 descontent -->
                <div class="card-body">
                  <!--                    <p>{{ item.descriptionInfo.descontent }}</p>-->
                  <p v-html="item.descriptionInfo.descontent"></p>
                </div>
                <!-- 卡片底部显示 refs（斜体样式） -->
                <div class="card-footer">
                  <p class="italic">{{ item.descriptionInfo.refs.join(', ') }}</p>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </div>
      </template>

      <template v-if="fullInformation">
        <!-- 搜索结果 -->
        <el-row style="margin-top: 20px;" v-if="fullInformation.summary">

          <!-- 全部内容 -->
          <el-col :span="24">
            <el-card class="card" shadow="hover">
              <div class="card-header">
                <h3>百科全部内容</h3>
              </div>
              <div class="card-body">
                <p style="white-space: pre-wrap;">{{ fullInformation.content }}</p>
              </div>
              <div class="card-footer">
                <p class="italic">维基百科</p>
              </div>
            </el-card>
          </el-col>

          <!-- 分类 -->
          <el-col :span="24">
            <el-card class="card" shadow="hover">
              <div class="card-header">
                <h3>分类</h3>
              </div>
              <div class="card-body">
                <p>{{ fullInformation.categories.join(", ") }}</p>
              </div>
              <div class="card-footer">
                <p class="italic">维基百科</p>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </template>

      <div class="loader" v-if="loading">
        <img src="/loading.gif" alt="Loading" class="loading-image"/>
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

.card {
  margin-bottom: 20px;
  padding: 20px;
  background-color: #e0fffa;
}

.card-header h3 {
  font-family: 'Roboto', sans-serif;
  font-size: 1.2em;
  letter-spacing: 1px;
  color: #006400;
  margin-bottom: 10px;
  font-weight: bold;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

.card-body {
  margin-bottom: 10px;
}

.card-footer {
  font-size: 0.9em;
  text-align: right;
}

.italic {
  font-style: italic;
  color: #555;
}

.loader {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 80vh;
}

.loading-image {
  width: 70px; /* 设置为所需的宽度 */
  height: 70px; /* 设置为 'auto' 可以保持图像比例 */
}

.image-row {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

.insect-image {
  width: 100%; /* 使图片宽度充满父容器 */
  height: auto; /* 高度自动调整，保持宽高比 */
}

</style>