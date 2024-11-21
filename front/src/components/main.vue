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
      //搜索的类型，比如学名搜索，描述搜索等,S代表标准（学名搜索），I代表图片搜索，A代表AI搜索
      selectedSearch: 'S',
      searchStatus : {
        S : "S",
        I : "I",
        A : "A",
      },
      //存储搜索结果
      searchResults: [
        {
          //俗名
          Common_name: "蟑螂",
          //中文学名
          Chinese_name: "蜚蠊",
          //拉丁文学名
          Latin_name: "Blattodea",
          //别名
          Alias_name: "黄嚓、曱甴、小强、黄婆娘、偷油婆、鞋板虫、油灶婆、滑虫",

          //界门纲目科属种依次：
          Kingdom: "动物界",
          Phylum: "节肢动物门",
          Class: "昆虫纲",
          Order: "蜚蠊目",
          Family: "蜚蠊科",
          Genus: "",
          Species: "",
          othertax: [
            //   总/超，亚，次/下的各种分类，可有可无，总:super-;亚:sub;次/下:infra
            {
              title : "亚门",
              tax: "六足亚门"
            },
            {
              title : "亚纲",
              tax: "有翅亚纲"
            },
          ],

          //其他各类描述,title为这个描述的题目，value为这个描述的内容，如："形态特征"为title，其内容为value
          attributes: [
              {
                title : "形态特征",
                value : "蟑螂是蜚蠊目蜚蠊科的昆虫。 其背部扁平；身体长而多节，有丝状触角；前胸背板大、如盾状；有皮革质前翅；后翅膜质，静止时呈扇状折叠；翅膀有的长、有的短、有的则完全无翅；尾须多节；雄性蟑螂腹部末节长有节芒（有的种类节芒退化或没有）。 此虫气如廉姜，又名“飞廉”。\n" +
                    "曾经有生物学家根据蟑螂的生态习性下了一个定论：如果有一天地球上发生了全球核子大战，在影响区内的所有生物包括人类和甚至鱼类等都会消失殆尽，只有蟑螂会继续它们的生活，这是因为通常情况下人类身体所能忍受的放射量为5rems，一旦总辐射量超过800rems则必死无疑。而德国小蠊可以忍受9000~105000rems，美洲大蠊则达到967500rem。（表示辐射剂量。rem剂量当量雷姆(rem) 希[沃特](Sv) 1Sv=100rem）所以即使有核子爆炸，蟑螂也可以幸存下来。美国政府用来消灭蟑螂一年的费用就达到15亿美元，大约是用在防治艾滋病预算的两倍。"
              },

          ],
          //图片url
          image_url : "https://cdn.pixabay.com/photo/2014/12/13/15/38/cockroach-566712_1280.jpg"
        },
        {
          //俗名
          Common_name: "蟑螂",
          //中文学名
          Chinese_name: "蜚蠊",
          //拉丁文学名
          Latin_name: "Blattodea",
          //别名
          Alias_name: "黄嚓、曱甴、小强、黄婆娘、偷油婆、鞋板虫、油灶婆、滑虫",

          //界门纲目科属种依次：
          Kingdom: "动物界",
          Phylum: "节肢动物门",
          Class: "昆虫纲",
          Order: "蜚蠊目",
          Family: "蜚蠊科",
          Genus: "",
          Species: "",
          othertax: [
            //   总/超，亚，次/下的各种分类，可有可无，总:super-;亚:sub;次/下:infra
            {
              title : "亚门",
              tax: "六足亚门"
            },
            {
              title : "亚纲",
              tax: "有翅亚纲"
            },
          ],

          //其他各类描述,title为这个描述的题目，value为这个描述的内容，如："形态特征"为title，其内容为value
          attributes: [
              {
                title : "形态特征",
                value : "蟑螂是蜚蠊目蜚蠊科的昆虫。 其背部扁平；身体长而多节，有丝状触角；前胸背板大、如盾状；有皮革质前翅；后翅膜质，静止时呈扇状折叠；翅膀有的长、有的短、有的则完全无翅；尾须多节；雄性蟑螂腹部末节长有节芒（有的种类节芒退化或没有）。 此虫气如廉姜，又名“飞廉”。\n" +
                    "曾经有生物学家根据蟑螂的生态习性下了一个定论：如果有一天地球上发生了全球核子大战，在影响区内的所有生物包括人类和甚至鱼类等都会消失殆尽，只有蟑螂会继续它们的生活，这是因为通常情况下人类身体所能忍受的放射量为5rems，一旦总辐射量超过800rems则必死无疑。而德国小蠊可以忍受9000~105000rems，美洲大蠊则达到967500rem。（表示辐射剂量。rem剂量当量雷姆(rem) 希[沃特](Sv) 1Sv=100rem）所以即使有核子爆炸，蟑螂也可以幸存下来。美国政府用来消灭蟑螂一年的费用就达到15亿美元，大约是用在防治艾滋病预算的两倍。"
              },

          ],
          //图片url
          image_url : "https://cdn.pixabay.com/photo/2014/12/13/15/38/cockroach-566712_1280.jpg"
        },
          {
          //俗名
          Common_name: "蟑螂",
          //中文学名
          Chinese_name: "蜚蠊",
          //拉丁文学名
          Latin_name: "Blattodea",
          //别名
          Alias_name: "黄嚓、曱甴、小强、黄婆娘、偷油婆、鞋板虫、油灶婆、滑虫",

          //界门纲目科属种依次：
          Kingdom: "动物界",
          Phylum: "节肢动物门",
          Class: "昆虫纲",
          Order: "蜚蠊目",
          Family: "蜚蠊科",
          Genus: "",
          Species: "",
          othertax: [
            //   总/超，亚，次/下的各种分类，可有可无，总:super-;亚:sub;次/下:infra
            {
              title : "亚门",
              tax: "六足亚门"
            },
            {
              title : "亚纲",
              tax: "有翅亚纲"
            },
          ],

          //其他各类描述,title为这个描述的题目，value为这个描述的内容，如："形态特征"为title，其内容为value
          attributes: [
              {
                title : "形态特征",
                value : "蟑螂是蜚蠊目蜚蠊科的昆虫。 其背部扁平；身体长而多节，有丝状触角；前胸背板大、如盾状；有皮革质前翅；后翅膜质，静止时呈扇状折叠；翅膀有的长、有的短、有的则完全无翅；尾须多节；雄性蟑螂腹部末节长有节芒（有的种类节芒退化或没有）。 此虫气如廉姜，又名“飞廉”。\n" +
                    "曾经有生物学家根据蟑螂的生态习性下了一个定论：如果有一天地球上发生了全球核子大战，在影响区内的所有生物包括人类和甚至鱼类等都会消失殆尽，只有蟑螂会继续它们的生活，这是因为通常情况下人类身体所能忍受的放射量为5rems，一旦总辐射量超过800rems则必死无疑。而德国小蠊可以忍受9000~105000rems，美洲大蠊则达到967500rem。（表示辐射剂量。rem剂量当量雷姆(rem) 希[沃特](Sv) 1Sv=100rem）所以即使有核子爆炸，蟑螂也可以幸存下来。美国政府用来消灭蟑螂一年的费用就达到15亿美元，大约是用在防治艾滋病预算的两倍。"
              },

          ],
          //图片url
          image_url : "https://cdn.pixabay.com/photo/2014/12/13/15/38/cockroach-566712_1280.jpg"
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

    //搜索
    async Search(status) {
      try {
        const response = await axios.get('url', {
          params: {
            //搜索的关键词
            query: this.searchQuery,
            //是什么搜索，S代表标准（学名搜索），I代表图片搜索，A代表AI搜索
            status: status
          }
        });
        this.searchResults = response.data.results; // 假定 API 返回结果在 data.results
      } catch (error) {
        console.error('搜索失败:', error);
      }
    },
    goToDetailPage(item) {
    // 跳转到详情页面
    this.$router.push({
      path: '/result',
      query: { name: item.Common_name }
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
      <div class="search-container">
        <el-input
            v-model="searchQuery"
            placeholder="输入关键词"
            @keyup.enter.native="Search(selectedSearch)"
            clearable>
        </el-input>
        <el-select v-model="selectedSearch" class="search-select" placeholder="选择搜索方式">
          <el-option label="学名搜索" :value="searchStatus.S"></el-option>
          <el-option label="图片搜索" value="searchStatus.I"></el-option>
          <el-option label="AI搜索" value="searchStatus.A"></el-option>
        </el-select>
        <el-button @click="Search(selectedSearch)">搜索</el-button>
      </div>

      <el-list>
        <template v-for="(item, index) in searchResults" :key="index">
          <el-card class="result-card" @click="goToDetailPage(item)">
            <div style="display: flex; align-items: center;">
              <div style="flex: 1;">
                <h3>{{ item.Common_name }}</h3>
                <p>{{ item.Chinese_name }} ({{ item.Latin_name }})</p>
                <p>别名: {{ item.Alias_name }}</p>
              </div>
              <img :src="item.image_url" alt="Image" style="max-height: 100px; max-width: 100px; margin-left: 20px;">
            </div>
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

.el-button {
  margin-right: 10px;
}

.el-input{
  margin-right: 10px;
  width: 600px;
}

.search-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

 .search-select {
  margin-right: 10px;
  width: 300px; /* 设置宽度 */
}

.search-select {
  margin-right: 10px;
  width: 100px; /* 设置宽度 */
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
</style>
