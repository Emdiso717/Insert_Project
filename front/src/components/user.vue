<script>
import { HomeFilled, List, UserFilled } from "@element-plus/icons-vue";
import axios from "axios";
import wikipedia from "wikipedia";
import { ElMessage } from "element-plus"; // 引入wikipedia模块
import AchievementCard from './AchieveCard.vue'
export default {
  components: { List, UserFilled, HomeFilled, AchievementCard },
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
      user: {
        account: 'Emdiso717',
        email: '111111111@email.com'
      },
      insectAchievements: [
        {
          id: 1,
          title: "初识昆虫",
          description: "搜索 1 种昆虫",
          icon: "🐜",
          target: 1
        },
        {
          id: 2,
          title: "昆虫爱好者",
          description: "搜索 5 种昆虫",
          icon: "🐛",
          target: 5
        },
        {
          id: 3,
          title: "初级昆虫学家",
          description: "搜索 10 种昆虫",
          icon: "🦗",
          target: 10
        },
        {
          id: 4,
          title: "进阶昆虫学家",
          description: "搜索 30 种昆虫",
          icon: "🦋",
          target: 30
        },
        {
          id: 5,
          title: "专业昆虫学家",
          description: "搜索 50 种昆虫",
          icon: "🪲",
          target: 50
        },
        {
          id: 6,
          title: "昆虫研究员",
          description: "搜索 100 种昆虫",
          icon: "🐞",
          target: 100
        },
        {
          id: 7,
          title: "昆虫专家",
          description: "搜索 200 种昆虫",
          icon: "🦎",
          target: 200
        },
        {
          id: 8,
          title: "昆虫权威",
          description: "搜索 500 种昆虫",
          icon: "🕷️",
          target: 500
        },
        {
          id: 9,
          title: "昆虫大师",
          description: "搜索 800 种昆虫",
          icon: "⭐",
          target: 800
        },
        {
          id: 10,
          title: "昆虫之王",
          description: "搜索 1000 种昆虫",
          icon: "👑",
          target: 1000
        }
      ]
    }
  },
  created() {
    this.account = this.$route.query.account;
    this.get_em();
    wikipedia.setLang("zh");
  },

  methods: {
    get_em() {
      axios.post("/get_account",
        {
          account: this.account,
        }).then(response => {
          this.user = response.data;
          if(this.user.account==="Emdiso717"){
            this.user.count = 1260;
          }
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
          this.searchResult = "未找到相��内容，请尝试其他关键词。";
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
        query: { searchQuery: this.searchQuery },
      });
    },
    quit() {
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
            <HomeFilled />
          </el-icon>
          <template #title>搜索</template>
        </el-menu-item>
        <el-menu-item @click="changeRoute('/tree')" index="2" class="icon">
          <el-icon style="color: #244a31">
            <List />
          </el-icon>
          <template #title>昆虫树状图</template>
        </el-menu-item>
        <el-menu-item @click="changeRoute('/user')" index="3" class="icon">
          <el-icon style="color: #244a31">
            <UserFilled />
          </el-icon>
          <template #title>个人信息</template>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-main class="main">
      <!--      <img class="background" src="./icons/cool-background%20.svg" alt="Description" />-->
      <div class="content-card">
        <!-- User Info Section -->
        <div class="user-info-card">
          <div class="card-header">
            <div class="avatar-section">
              <el-avatar :size="120" src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"
                class="profile-avatar" />
              <div class="user-name">{{ user.account }}</div>
              <el-tag type="success" class="user-level" effect="dark">Level {{ Math.floor((user.count / 100)) +1}}</el-tag>
            </div>

            <div class="info-grid">
              <div class="info-item">
                <div class="item-label">Email</div>
                <div class="item-value">{{ user.email }}</div>
              </div>
              <div class="info-item">
                <div class="item-label">Join Date</div>
                <div class="item-value">{{ user.date_joined || '2024-03-20' }}</div>
              </div>
              <div class="info-item">
                <div class="item-label">Insects Found</div>
                <div class="item-value highlight">{{ user.count }}</div>
              </div>
              <div class="info-item">
                <div class="item-label">Achievement Rate</div>
                <div class="item-value highlight">{{ Math.floor((user.count / 1000) * 100) }}%</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Achievements Display Section -->
        <div class="achievements-section">
          <div class="achievements-header">
            <div class="header-content">
              <h2 class="section-title">Achievement Collection</h2>
              <div class="achievement-stats">
                <div class="stat-item">
                  <span class="stat-label">Total Discoveries</span>
                  <span class="stat-value">{{ user.count }}</span>
                </div>
                <div class="stat-item">
                  <span class="stat-label">Progress</span>
                  <span class="stat-value">{{ Math.floor((user.count / 1000) * 100) }}%</span>
                </div>
              </div>
            </div>
            <el-progress :percentage="Math.min((user.count / 1000) * 100, 100)" :stroke-width="8" :show-text="false"
              color="#36714a" class="total-progress" />
          </div>

          <div class="achievements-container">
            <AchievementCard v-for="achievement in insectAchievements" :key="achievement.id" :title="achievement.title"
              :description="achievement.description" :icon="achievement.icon" :current="user.count"
              :total="achievement.target" :locked="user.count < achievement.target" />
          </div>
        </div>
      </div>
      <el-button @click="quit" style="margin-left: 1500px">Quit</el-button>
    </el-main>
  </el-container>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet');

.form_font {
  font-family: 'Montserrat', sans-serif;
  color: #000000;
  font-size: 20px;
  font-style: italic;
  font-weight: 900;
  letter-spacing: 2px;
}

.mat {
  margin-top: 10px;
}

.text {
  font-family: 'Montserrat', sans-serif;
  color: #000000;
  font-size: 13px;
  font-style: italic;
  font-weight: 600;
  letter-spacing: 2px;
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
.down {
  position: relative;

  top: -70px;
  width: 80%;
  margin-left: 10%;
  height: 58%;
}

.down2 {
  margin-top: 10px;
}

.divider {
  position: relative;
  top: -80px;
  margin-left: 10%;
  width: 80%;
}

.po1 {
  position: relative;
  top: -80px;
  left: 200px;
}

.po2 {
  margin-top: 10px;
}

.avatar {
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

.main>div {
  margin-bottom: 20px;
}

.card {
  position: relative;
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

.font {
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
  box-shadow: 0 2px 10px rgb(10, 64, 165, 0.2);
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

.text_button {
  font-family: 'Montserrat', sans-serif;
  font-size: 14px;
  font-style: italic;
  font-weight: 900;
  letter-spacing: 2px;
}

.user-info-card {
  background: white;
  border-radius: 20px;
  padding: 30px;
  margin-bottom: 30px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}

.card-header {
  display: flex;
  gap: 40px;
  align-items: flex-start;
}

.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  min-width: 200px;
}

.profile-avatar {
  border: 4px solid #36714a;
  padding: 4px;
  background: white;
  box-shadow: 0 4px 12px rgba(54, 113, 74, 0.15);
  transition: transform 0.3s ease;
}

.profile-avatar:hover {
  transform: scale(1.05);
}

.user-name {
  font-size: 24px;
  font-weight: 600;
  color: #244a31;
  margin-top: 8px;
}

.user-level {
  padding: 4px 12px;
  border-radius: 12px;
}

.info-grid {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 16px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.item-label {
  font-size: 14px;
  color: #666;
  font-weight: 500;
}

.item-value {
  font-size: 16px;
  color: #2c3e50;
  font-weight: 600;
}

.item-value.highlight {
  color: #36714a;
  font-size: 24px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .card-header {
    flex-direction: column;
    align-items: center;
    gap: 24px;
  }

  .avatar-section {
    min-width: unset;
    width: 100%;
  }

  .info-grid {
    grid-template-columns: 1fr;
    width: 100%;
    padding: 16px;
  }

  .info-item {
    text-align: center;
  }
}

.achievements-section {
  padding: 20px 30px;
  background: white;
  border-radius: 20px;
  margin: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}

.achievements-header {
  margin-bottom: 30px;
  padding: 20px;
  background: linear-gradient(to right, #f8f9fa, #ffffff);
  border-radius: 16px;
  border: 1px solid #eee;
}

.header-content {
  margin-bottom: 20px;
}

.section-title {
  color: #244a31;
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 16px;
}

.achievement-stats {
  display: flex;
  gap: 40px;
  margin-bottom: 16px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-label {
  color: #666;
  font-size: 14px;
  font-weight: 500;
}

.stat-value {
  color: #36714a;
  font-size: 24px;
  font-weight: 600;

}

.total-progress {
  margin-top: 16px;

}

.achievements-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  padding: 10px;
}

/* Custom scrollbar for achievements container */
.achievements-container::-webkit-scrollbar {
  width: 8px;
}

.achievements-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.achievements-container::-webkit-scrollbar-thumb {
  background: #36714a;
  border-radius: 4px;
}

.achievements-container::-webkit-scrollbar-thumb:hover {
  background: #244a31;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .achievements-section {
    padding: 15px;
    margin: 10px;
  }

  .achievements-header {
    padding: 15px;
  }

  .achievement-stats {
    flex-direction: column;
    gap: 20px;
  }

  .achievements-container {
    grid-template-columns: 1fr;
  }

  .stat-item {
    align-items: center;
  }
}
</style>
