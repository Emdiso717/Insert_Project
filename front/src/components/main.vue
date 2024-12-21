<script xmlns="http://www.w3.org/1999/html">
import {
  Delete,
  Download,
  HomeFilled,
  List,
  Plus,
  Upload,
  UploadFilled,
  UserFilled,
  ZoomIn
} from "@element-plus/icons-vue";
import axios from "axios";
import wikipedia from "wikipedia";
import { ElUpload } from 'element-plus';
import {ElMessage} from "element-plus"; // 引入wikipedia模块


export default {
  components: {UploadFilled, Upload, Delete, Download, ZoomIn, Plus, List, UserFilled, HomeFilled},
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
      searchQuery_show: '',
      searchResult: "", // 原始搜索结果
      truncatedResult: "", // 截取后的搜索结果
      relativeResultArray: [],//对于搜索结果的相关昆虫结果
      image_search:false,
      image_input:true,
      imageBase64: null,
      image_result:[],
      loading : false,//搜索条目加载中？
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
        this.loading = true;
        this.searchQuery_show=this.searchQuery;
        this.relativeResultArray = [];
        // 调用 API 并获取数据
        const response = await wikipedia.page(this.searchQuery_show);
        const summary = await response.summary();
        this.searchResult = summary.extract; // 原始结果
        this.truncatedResult = this.getFirstLines(summary.extract, 3); // 截取前三行

        //调用后端api获得相关搜索结果
        const response1 = await axios.get('/search_relative_insect', {
          params: { name: this.searchQuery_show }
        })
        const relativeInsect = response1.data.data;
        console.log(relativeInsect)
        for (let i = 0; i < relativeInsect.length; i++) {
          // console.log(relativeInsect[i])
          // console.log(this.searchQuery)
          try{
            let response2 = await wikipedia.page(relativeInsect[i]);
            let summary2 = await response2.summary();
            this.relativeResultArray.push({
              name: relativeInsect[i], // 设置name属性
              res: this.getFirstLines(summary2.extract, 3) // 截取前三行 设置res属性
            });
          }catch(error){

          }
          // let response2 = await wikipedia.page(relativeInsect[i]);
          // let summary2 = await response2.summary();
          // this.relativeResultArray.push({
          //   name: relativeInsect[i], // 设置name属性
          //   res: this.getFirstLines(summary2.extract, 3) // 截取前三行 设置res属性
          // });
        }
      } catch (error) {
        if (error.name === "PageError") {
          this.searchResult = "未找到相关内容，请尝试其他关键词。";
        } else if (error.name === "DisambiguationError") {
          this.searchResult = "关键词过于模糊，请尝试更具体的搜索内容。";
        } else {
          this.searchResult = `搜索失败：${error.message}`;
        }
        console.log(error)
        this.truncatedResult = ""; // 确保失败时不显示内容
        this.relativeResultArray = [];
      }finally {
        this.loading = false; // 结束加载
      }
    },
    //截取前三行
    getFirstLines(text, numLines) {
      return text
          .split("\n") // 按换行符分割
          .slice(0, numLines) // 截取前 numLines 行
          .join("\n"); // 再拼接回字符串
    },
    goToDetailPage(Query) {
      // 跳转到详情页面
      this.$router.push({
        path: '/result',
        query: {
          searchQuery: Query,
          account:this.account
        },
      });
    },
    load_image(e) {
      const file = e.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (event) => {
          this.imageBase64 = event.target.result;
        };
        reader.readAsDataURL(file); // 读取文件并转换为Base64
        this.image_input = false;
      }
    },
    triggerFileInput() {
      // 触发原生的文件输入
      this.$refs.fileInput.click();
    },
    imagesearch(){
      axios.post("/imagesearch",
            {
              image:this.imageBase64
            }).then(response => {
        this.image_result = response.data.result
      })
    }
  }
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
      <div class="search-container">
        <input v-model="searchQuery" placeholder="输入关键词" @keyup.enter="Search" class = "search"/>
        <el-button class="search_button" @click="Search" style="margin-left: 1%"><p>搜索</p></el-button>
        <el-button class="search_button" @click="Search"><p>搜索</p></el-button>
        <el-button v-if="image_search" class="search_button" @click="image_search=!image_search"><p>收起</p></el-button>
        <el-button v-if="!image_search" class="search_button" @click="image_search=!image_search"><p>图像搜索</p></el-button>
      </div>
      <el-row v-if="image_search" style="height: 80%;width: 90%;margin-left: 10%;margin-top: 4%">
        <div class="image_search">
          <div v-if="image_input" class="image_upload" @click="triggerFileInput">
            <input type="file" @change="load_image" ref="fileInput" style="display: none;" />
            <el-icon style="font-size: 40px"><UploadFilled /></el-icon>
            <p>上传图片</p>
          </div>
          <div v-if="imageBase64" class="image_upload ">
            <img class="image_upload1" :src="imageBase64" alt="insert"/>
          </div>
          <div class="button-container">
            <el-button  style="margin-left: 10px" @click="imageBase64=null;image_input=true;"><p>删除图片</p></el-button>
            <el-button style="margin-top: 15px" @click="imagesearch"><p>图像搜索</p></el-button>
          </div>
        </div>
        <div class="image_result">
          <div style="text-align: center;color: #3f6a53;"><p style="font-size: 20px">Search Results</p></div>
          <div v-for="re in image_result" class="image_result_version">
            <p>{{re.name}}  :  {{re.score}}</p>
            <el-progress  :stroke-width="10" :percentage="parseFloat(re.score)*100" color="#3f6a53" :show-text="false"/>
          </div>
        </div>

      </el-row>
      <!-- 搜索结果展示 -->
        <div class="loader" v-if="loading">
          <img src="/loading.gif" alt="Loading" class="loading-image"/>
        </div>
      <el-list>
        <template v-if="searchResult">
          <el-card class="result-card" @click="goToDetailPage(searchQuery_show)">
            <div style="display: flex; align-items: center;">
              <div style="flex: 1;">
                <p>
                  <a
                      href="javascript:void(0);"
                      style="text-decoration: underline; color: blue;"
                      @click="goToDetailPage(searchResult)"
                  >
                    {{ searchQuery_show }}
                  </a>
                </p>
                <p style="color: #000000;">{{ truncatedResult }}</p>
              </div>
            </div>
          </el-card>
          <div v-for="(item, index) in relativeResultArray" :key="index">
            <el-card class="result-card" @click="goToDetailPage(item.name)">
              <div style="display: flex; align-items: center;">
                <div style="flex: 1;">
                  <p>
                    <a
                        href="javascript:void(0);"
                        style="text-decoration: underline; color: blue;"
                        @click="goToDetailPage(item.name)"
                    >
                      {{ item.name }}
                    </a>
                  </p>
                  <p style="color: #000000;">{{ item.res }}</p>
                </div>
              </div>
            </el-card>
          </div>
        </template>
      </el-list>
    </el-main>
  </el-container>
</template>


<style  scoped>
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

.el-button {
  margin-right: 10px;
}

.el-input {
  margin-right: 10px;
  width: 600px;
}

.search-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

p{
  font-family: 'Montserrat', sans-serif;
  font-weight: 800;
  font-size: 16px;
}

.el-button{
  background-color: #36714a;
  height: 45px;
  border-radius: 10px;
  border: 2px solid #36714a;
  box-shadow: 0 2px 8px rgb(29, 50, 37);
  transition: .2s;
  color: #f5f7f8;
}
.el-button:active,
.el-button:focus,
.el-button:hover {
  background-color: #ffffff;
  transition: box-shadow 0.3s ease;
  color: #1d3225;
  border-color: #326742;
  box-shadow: 0 4px 16px rgb(36, 74, 49);
  border-width: 3px;
}
.image_load{
  width: 100px;
  background-color: #36714a;
  margin-left: 1%;
  height: 45px;
  border-radius: 10px;
  border: 2px solid #36714a;
  box-shadow: 0 2px 8px rgb(29, 50, 37);
  transition: .2s;
  color: #f5f7f8;
}
.image_load:active,
.image_load:focus,
.image_load:hover {
  background-color: #ffffff;
  transition: box-shadow 0.3s ease;
  color: #1d3225;
  border-color: #326742;
  box-shadow: 0 4px 16px rgb(36, 74, 49);
  border-width: 3px;
}

.el-card {
  padding: 20px;
  margin-bottom: 20px;
  width: 60%;
  margin-left: auto;
  margin-right: auto;
}

.result-card {
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.result-card:hover {
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  transform: translateY(-5px);
}

.search {
  font-family: 'Montserrat', sans-serif;
  height: 45px;
  font-size: 16px;
  padding: 15px;
  font-weight: 800;
  width: 800px;
  border: 3px solid #5e9f74;
  transition: border-color 0.3s ease-in-out; /* 添加动画效果 */
  border-radius: 8px;
  outline: none !important;
}
.search:focus {
  border-color: #326742 !important;
}
.search:hover {
  border-color: #326742 !important;
}

.image_search{
  display: flex;
  justify-content:space-between;
  align-items: center;
  margin-left: 3%;
  height: 80%;
  width: 60%;
  background-color: rgba(218, 216, 216, 0.25);
  transition: transform 0.6s ease, box-shadow 0.6s ease;
}
.image_search:hover {
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
}
.image_result{
  display: grid;
  place-items: center;
  margin-left: 3%;
  height: 80%;
  width: 20%;
  background-color: rgba(218, 216, 216, 0.25);
  transition: transform 0.6s ease, box-shadow 0.6s ease;
}
.image_result:hover {
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
}

.button-container {
  display: flex;
  flex-direction: column; /* 子元素垂直排列 */
  align-items: center; /* 子元素在交叉轴上居中对齐 */
  justify-content: space-around; /* 主轴上子元素分散对齐，并留有空隙 */
  height: 100px; /* 根据需要设置容器的高度 */
  padding-right: 50px;
}

.image_upload{
    height: 400px; /* 可以根据需要调整高度 */
    width: 800px;
    border: 2px dashed #5e9f74; /* 虚线框 */
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 20px;
    position: relative;
    overflow: hidden;
    background: #e7f3ec;
    transition: transform 0.6s ease, box-shadow 0.6s ease,background-color 0.6s ease;;
}
.image_upload:hover {
  background: #cdd8d1;
  box-shadow: 0 4px 10px rgb(66, 149, 97);
}
.image_upload1{
    max-height: 400px; /* 可以根据需要调整高度 */
    max-width: 800px;
    display: flex;
    align-items: center;
    justify-content: center;
    width: auto;
    height: auto;
}
.image_result_version{
  margin-top:-3px;
  width: 90%;
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
</style>