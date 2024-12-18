<script>
import {HomeFilled, List, UserFilled} from "@element-plus/icons-vue";
import axios from "axios";
import wikipedia from "wikipedia";
import {ElMessage} from "element-plus"; // 引入wikipedia模块

//导入读取excel的库
import * as XLSX from 'xlsx';

//树状图的库
import * as d3 from 'd3';


export default {
  components: {List, UserFilled, HomeFilled},
  data() {
    return {
      //账号id
      account: '',
      /*___________________树状图用数据_______________________
      *展示纲目科属种中的某一层次的单个具体条例，及其下属所有存在的
      * 如：当前层次： 昆虫纲， 则当前展示昆虫纲以及属于昆虫纲的所有目的节点如鞘翅目，双翅目等；
      * 点击其中某个节点如鞘翅目，则鞘翅目替代树中原来的昆虫纲的位置，下属节点变为鞘翅目下属的天牛科，叶甲科等
      * 直到子节点变为昆虫种，则点击直接跳转该昆虫的详细界面
      *
      * 运行须先运行以下两条指令
      * 'npm install d3' 和 'npm install xlsx'
      * */
      //当前父节点所在层次，从纲到属，从1到5表示
      level : 1,
      //父节点的父节点栈，用于追踪浏览轨迹，便于回到上层
      upperNodeStack:[{
        name: '',
        latinName: ''
      }],
      //当前父节点名称
      parentNode: {
        name: '昆虫纲',
        latinName: 'Insecta'
      },
      childrenNode:[],//子节点数组
      //存储excel中读取的信息
      excelData: null,

      //树状图信息
      treeData:{
        name: '',
        latinName: '',
        children:[],
      },
    }
  },
  created() {
    this.account = this.$route.query.account;
    wikipedia.setLang("zh");
  },
  mounted: async function() {
    await this.readExcelData(); // 确保数据加载完成
    await this.setTreeData();   // 确保树数据初始化成功
    this.createTree();          // 最后创建树图
  },
  methods: {
    changeRoute(path) {
      const currentRoute = this.$route;
      this.$router.push({
        path: path,
        query: currentRoute.query
      });
    },
    createTree() {
      d3.select("#tree").select("svg").remove();
      const width = 1400;
      let heightCount = this.treeData.children.length * 45;
      if(heightCount < 800){
        heightCount = 800;
      }
      const height = heightCount;

      const svg = d3.select("#tree")
        .append("svg")
        .attr("width", width + 600)
        .attr("height", height);

      const g = svg.append("g")
        .attr("transform", "translate(40,0)");
/*
      const tree = d3.tree()
        .size([height - 80, width - 360])
        .separation((a, b) => {
          // 使得同一层级的节点间隔相等
          return 1;
         });

      const root = d3.hierarchy(this.treeData);

      tree(root);
*/
      const cluster = d3.cluster()
        .size([height - 80, width - 200]);
      const root = d3.hierarchy(this.treeData);
      cluster(root);

      // Links (edges)
      g.selectAll(".link")
        .data(root.links())
        .enter().append("path")
        .attr("class", "link")
        .attr("d", d3.linkHorizontal()
          .x(d => d.y)
          .y(d => d.x))
        .style("fill", "none")
        .style("stroke", "#2E8B57");

      // Nodes
      const node = g.selectAll(".node")
        .data(root.descendants())
        .enter().append("g")
        .attr("class", "node")
        .attr("transform", d => `translate(${d.y},${d.x})`)
        .on("click" , (event , d) => {
          this.goToNode(d.data);
        })
        .on("mouseover", function(event, d) {
          // 放大圆形节点
          d3.select(this).select("circle")
            .transition()
            .duration(200)
            .attr("r", 25) // 增大圆形半径
            .style("cursor", "pointer");

          // 放大文本并向右移动
          d3.select(this).selectAll("text")
            .transition()
            .duration(200)
            //.style("font-size", "14px")
            .attr("x", d => d.depth === 0 ? 35 : d.children ? -35 : 35); // 右移文字

        })
        // 鼠标移开时恢复默认状态
        .on("mouseout", function(event, d) {
          // 恢复圆形节点大小
          d3.select(this).select("circle")
            .transition()
            .duration(200)
            .attr("r", 15) // 恢复圆形半径
            .style("cursor", "default");

          // 恢复文本大小和位置
          d3.select(this).selectAll("text")
            .transition()
            .duration(200)
            .style("font-size", "10px")
            .attr("x", d => d.depth === 0 ? 25 : d.children ? -25 : 25); // 恢复文本位置

          // 恢复连线的颜色和宽度
        });


      node.append("circle")
        .attr("r", 15)
        .style("fill", "#fff")
        .style("stroke", "steelblue")
          .attr("dx" , d => {
            if(d.depth ===0 ){
              return 100;
            }else{
              return 0;
            }
          });

      const text1 = node.append("text")
        .attr("dy", ".31em")
        .attr("x", d => {
          if (d.depth === 0) {
            return 25; // 根节点的文本向右移一个半径距离
          }
          return d.children ? -25 : 25;
        })
        .style("text-anchor", d => {
          if (d.depth === 0) {
            return "start"; // 根节点文本在右侧
          }
          return d.children ? "end" : "start";
        })
        .html(d => {
          if (d.data.name === '(未命名)') {
            // 如果名字是 '(未命名)'，显示拉丁名
            return `<tspan style=" font-size: 20px;">${d.data.latinName}</tspan>`;
          }
          // 否则显示普通的名字
          return `<tspan style=" font-size: 20px;">${d.data.name}</tspan>`;
        });

      const text2 = node.append("text")
        .attr("dy", ".200em")
        .attr("x", d => {
          if (d.depth === 0) {
            return 25; // 根节点的文本向右移一个半径距离
          }
          return d.children ? -25 : 25;
        })
        .attr("y" , d => {
          if (d.depth === 0) {
            return 15; // 根节点的文本向右移一个半径距离
          }
          return d.children ? -15 : 15;
        })
        .style("text-anchor", d => {
          if (d.depth === 0) {
            return "start"; // 根节点文本在右侧
          }
          return d.children ? "end" : "start";
        })
        .html(d => {
          return `<tspan style=" font-size: 13px;font-weight: 900;font-style: italic;">${d.data.latinName}</tspan>`;
        })
    },

    async setTreeData(){
      this.treeData.name = this.parentNode.name;
      this.treeData.latinName = this.parentNode.latinName;
      this.treeData.children = this.childrenNode;
    },

    async readExcelData(){
      try{
        const response = await fetch('/Tree_data.xlsx');
        if(!response.ok) throw new Error('Failed to load file');

        const data = await response.arrayBuffer();
        const workbook = XLSX.read(data, { type: 'array' });

        const firstSheetName = workbook.SheetNames[0];
        const worksheet = workbook.Sheets[firstSheetName];

        this.excelData = XLSX.utils.sheet_to_json(worksheet);
        console.log('read data complete')
        this.parentNode = {
          name: '昆虫纲',
          latinName:  'Insecta'
        };
        this.level = 1;
        const seen = new Set();
          this.childrenNode = this.excelData
            .filter(data => data.纲中文名 === '昆虫纲' && data.目拉丁名)
            .map(data => ({
              name: data.目中文名,
              latinName: data.目拉丁名
            }))
            .filter(item => {
              const isDuplicate = seen.has(item.name);
              if (!isDuplicate) {
                seen.add(item.name);
                return true;
              }
              return false;
            });
      }catch(error){
        console.error('Error:' , error);
      }
    },

    //当点击节点时，即
    goToNode(pNode) {
      console.log('Checked node:' , pNode);
      let isDown;
      if(pNode.latinName === this.parentNode.latinName){
        isDown = 0;
      }else{
        isDown = 1;
      }
      if(isDown === 1){
        //level++
        if(this.level < 5){
        this.level++;
        }
        this.upperNodeStack.push(this.parentNode);
        this.parentNode = pNode;
      }else{
        //level--
        if(this.level > 1){
          this.level--;
        }
        this.parentNode = this.upperNodeStack.pop();
      }
      switch (this.level) {
        case 1:
            this.parentNode = {
              name:'昆虫纲',
              latinName: 'Insecta'
            }
            const seen0 = new Set();
            this.childrenNode = this.excelData
              .filter(data => data.纲拉丁名 === this.parentNode.latinName && data.目拉丁名)
              .map(data => ({
                name: data.目中文名 || '(未命名)',
                latinName: data.目拉丁名
              }))
              .filter(item => {
                const isDuplicate = seen0.has(item.latinName);
                if (!isDuplicate) {
                  seen0.add(item.latinName);
                  return true;
                }
                return false;
              });
            break;
          case 2:
            const seen1 = new Set();
            this.childrenNode = this.excelData
              .filter(data => data.目拉丁名 === this.parentNode.latinName && data.科拉丁名)
              .map(data => ({
                name: data.科中文名 || '(未命名)',
                latinName: data.科拉丁名
              }))
              .filter(item => {
                const isDuplicate = seen1.has(item.latinName);
                if (!isDuplicate) {
                  seen1.add(item.latinName);
                  return true;
                }
                return false;
              });
            break;
          case 3:
            const seen2 = new Set();
            this.childrenNode = this.excelData
              .filter(data => data.科拉丁名 === this.parentNode.latinName && data.属拉丁名)
              .map(data => ({
                name: data.属中文名 || '(未命名)',
                latinName: data.属拉丁名
              }))
              .filter(item => {
                const isDuplicate = seen2.has(item.latinName);
                if (!isDuplicate) {
                  seen2.add(item.latinName);
                  return true;
                }
                return false;
              });
            break;
          case 4:
            const seen3 = new Set();
            this.childrenNode = this.excelData
              .filter(data => data.属拉丁名 === this.parentNode.latinName && data.物种拉丁名)
              .map(data => ({
                name: data.物种中文名 || '(未命名)',
                latinName: data.物种拉丁名
              }))
              .filter(item => {
                const isDuplicate = seen3.has(item.latinName);
                if (!isDuplicate) {
                  seen3.add(item.latinName);
                  return true;
                }
                return false;
              });
            break;
          case 5:
            if(pNode.name === '(未命名)'){
              console.warn('无对应条目');
              this.level--;
              this.parentNode = this.upperNodeStack.pop();
            }else{
              this.$router.push({
                path: '/result',
                query: {
                  searchQuery: pNode.name,
                  account:this.account
                },
              })
            }
            break;
      }
      this.setTreeData();
      this.createTree();
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
      <div id="tree"></div>
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
  background-image: url("./icons/stacked-waves-haikei.svg");
  background-repeat: no-repeat;
  background-position: right bottom;
  background-size: cover;
}

.main > div {
  margin-bottom: 20px;
}
#tree {
  width: 100%;
  height: 100%;
}

.link {
  fill: none;
  stroke: #ccc;
}

.node {
  font: 12px sans-serif;
}

.node circle {
  fill: #fff;
  stroke: steelblue;
  stroke-width: 1.5px;
}

.node text {
  font: 12px sans-serif;
}
</style>
