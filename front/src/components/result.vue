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
        const response = await axios.get("/search_insect", {
            params: {
              name: this.searchQuery
            }
        })
        this.insectData = response.data; // 存储后端返回的数据
        console.log(this.insectData.image_url);
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
<!--      <el-descriptions v-if="insectData" class="margin-top" title="this信息" :column="1">-->
<!--        <el-descriptions-item label="中文名：">{{ insectData.chinese_name }}</el-descriptions-item>-->
<!--        <el-descriptions-item label="拉丁名：">{{ insectData.latin_name }}</el-descriptions-item>-->
<!--        <el-descriptions-item label="俗名：">{{ insectData.common_name }}</el-descriptions-item>-->
<!--        <el-descriptions-item label="别名：">{{ insectData.aliases }}</el-descriptions-item>-->
<!--        <el-descriptions-item label="外观：">{{ insectData.appearance }}</el-descriptions-item>-->
<!--        <el-descriptions-item label="习性：">{{ insectData.habits }}</el-descriptions-item>-->
<!--        <el-descriptions-item label="近亲：">{{ insectData.relatives }}</el-descriptions-item>-->
<!--        <el-descriptions-item label="分布：">{{ insectData.distribution }}</el-descriptions-item>-->
<!--      </el-descriptions>-->
<!--      <el-row class="image-row">-->
<!--        <el-col :span="12">-->
<!--          <el-image v-if="insectData.image_url" :src="insectData.image_url" fit="contain" class="insect-image"/>-->
<!--        </el-col>-->
<!--      </el-row>-->
      <el-row class="margin-top">
        <!-- 左侧部分：信息显示 -->
        <el-col :span="16">
          <el-descriptions v-if="insectData" class="margin-top" title="详情" :column="1">
            <el-descriptions-item label="中文名：">{{ insectData.chinese_name }}</el-descriptions-item>
            <el-descriptions-item label="拉丁名：">{{ insectData.latin_name }}</el-descriptions-item>
            <el-descriptions-item label="俗名：">{{ insectData.common_name }}</el-descriptions-item>
            <el-descriptions-item label="别名：">{{ insectData.aliases }}</el-descriptions-item>
            <el-descriptions-item label="外观：">{{ insectData.appearance }}</el-descriptions-item>
            <el-descriptions-item label="习性：">{{ insectData.habits }}</el-descriptions-item>
            <el-descriptions-item label="近亲：">{{ insectData.relatives }}</el-descriptions-item>
            <el-descriptions-item label="分布：">{{ insectData.distribution }}</el-descriptions-item>

            <el-descriptions-item label="分类 (Taxonomy)">
              <div v-if="insectData.taxonomy">
                <div v-for="(value, key) in insectData.taxonomy" :key="key" >
                  <div :style="{ marginLeft: '20px' }"><strong>{{ key }}:</strong> {{ value }}</div>
                </div>
              </div>
            </el-descriptions-item>
          </el-descriptions>
        </el-col>

        <!-- 右侧部分：图片显示 -->
        <el-col :span="5">
          <el-row class="image-row">
            <el-col :span="24">
              <el-image v-if="insectData && insectData.image_url" :src="insectData.image_url" fit="contain" class="insect-image"/>
            </el-col>
          </el-row>
        </el-col>
      </el-row>

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