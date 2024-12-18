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
    }
  },
  created() {
    this.searchQuery = this.$route.query.searchQuery;
    this.fetchFullContent();
  },
  methods: {
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
      }catch (error) {
        if (error.response) {
          // 后端返回了错误信息
          this.error = error.response.data.error || "未知错误";
        } else {
          // 网络错误或请求配置错误
          this.error = "请求失败，请检查网络连接";
        }
      }
    },
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
      <el-list>
        <template v-if="insectData">
          <div>
            <!-- 每行只显示一个卡片，设置 el-col 的 span 为 24 -->
            <el-row>
              <el-col :span="20" v-for="(item, index) in insectData" :key="index">
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


.image-row {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

.insect-image {
  width: 100%;          /* 使图片宽度充满父容器 */
  height: auto;         /* 高度自动调整，保持宽高比 */
}

</style>