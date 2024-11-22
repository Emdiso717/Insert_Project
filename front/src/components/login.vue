<script>
import {Lock, Message, User} from "@element-plus/icons-vue";
import axios from "axios";
import {ElMessage} from "element-plus";
export default {
  components: {Message, User, Lock},
  data() {
    return {
      account: '',
      password:'',
      new_acc:1,
      new_account:'',
      new_password:'',
      new_email:''
    };
  },
  created() {
    this.account = this.$route.query.account;
    console.log('Received account:', this.account);
  },
  methods:{
    Login(){
      axios.post("/login",
          {
            account:this.account,
            password:this.password
          }).then(response => {
        let message = response.data
        if (message.includes("success")) {
          ElMessage.success(message)
          this.$router.push({
            name:"Main",
            query:{
              account:this.account
            }
          })
        } else {
          ElMessage.error(message)
        }
      })
    },
    register(){
      let regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
      let emailValid = regex.test(this.new_email);
      if(this.new_account.length<=6){
        ElMessage.error("请保证账号至少有六位！")
      }else if(!emailValid){
        ElMessage.error("请输入正确格式邮箱！")
      }else if(this.new_password.length<=6){
        ElMessage.error("请保证密码至少有六位！")
      }
      else{
        axios.post("/login/register",
            {
              account:this.new_account,
              email:this.new_email,
              password:this.new_password
            }).then(response => {
          let message = response.data
          if (message.includes("success")) {
            this.new_acc=1
            ElMessage.success(message)
          } else {
            ElMessage.error(message)
          }
        })
      }
    }
  }
}
</script>



<template>
  <div class="all">
    <div >
        <img  src="./icons/img.png"  alt="logo" class="img">
    </div>
    <div class="form">
      <div v-if="new_acc===1" class="name">
        <h1 class="title">Insect<br> Lens</h1>
      </div>
      <form  v-if="new_acc===1" class="form_input">
        <div class="login">
          <el-icon style="color: #244a31"><User /></el-icon>
          <input v-model="account" type="text" class="input" placeholder="Account"/>
        </div>
        <div class="login">
          <el-icon style="color: #244a31"><Lock /></el-icon>
          <input v-model="password" type="password" class="input" placeholder="Password">
        </div>
        <el-button class="button" @click="Login">
          <span class="text">Log In Now</span>
        </el-button>
        <br>
        <el-button class="button new_account" @click="new_acc=0,account='',password=''">
          <span class="text">Register</span>
        </el-button>
      </form>
      <form  v-if="new_acc===0" class="form_input new">
        <div class="login">
          <el-icon style="color: #244a31"><User /></el-icon>
          <input v-model="new_account" type="text" class="input" placeholder="Please Input your account"/>
        </div>
        <div class="login">
          <el-icon style="color: #244a31"><Message /></el-icon>
          <input v-model="new_email" type="email" class="input" placeholder="Please Input your email">
        </div>
        <div class="login">
          <el-icon style="color: #244a31"><Lock /></el-icon>
          <input v-model="new_password" type="password" class="input" placeholder="Please Input your Password">
        </div>
        <el-button class="button" @click="register">
          <span class="text">Register Now</span>
        </el-button>
        <br>
        <el-button class="button new_account" @click="new_acc=1,new_password='',new_account='',new_email=''">
          <span class="text">Back To Login</span>
        </el-button>
      </form>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet');
.new{
  margin-top: -100px;
}
.name{
  position: absolute;
  z-index: 2;
  margin-top: 10%;
  margin-left: 3%;
}
.title{
  font-family: 'Montserrat', sans-serif;
  color: #3f6a53;
  font-size: 75px;
  font-style: italic;
  font-weight: 900;
  letter-spacing: 2px;
}
.all{
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url("./icons/stacked-peaks-haikei.svg");
  background-repeat: no-repeat;
  background-position: right bottom;
  background-size: cover;
}
.form_input{
  position: absolute;
  width: 100%;
  height: 100%;
  padding-top: 65%;
  padding-right: 10%;
  z-index: 2;
}
.login{
  padding-top: 5%;
  padding-left: 10%;
}
.form{
  position: relative;
  background-color: rgba(255, 255, 255, 0.5);
  top:40%;
  left:50%;
  width: 480px;
  height: 620px;
  transform: translate(-50%, -50%);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.form:hover {
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.4);
}
.input {
  font-size: 18px;
  border: none;
  border-bottom: 2px solid #464646;
  width: 80%;
  background: none !important;
  padding: 5% 3% 1%;
  font-weight: 700;
  transition: .2s;
}
.input:active,
.input:focus,
.input:hover {
  outline: none;
  border-bottom-color: #244a31;
}
.img{
  position: relative;
  width: 280px;
  height: auto;
}
.button {
  background: #fff;
  margin-top: 10%;
  margin-left: 30%;
  padding: 20px;
  border-radius: 26px;
  border: 2px solid #3f6a53;
  display: flex;
  align-items: center;
  width: 70%;
  box-shadow: 0 4px 16px rgb(29, 50, 37);
  transition: .2s;
  color: #5e9f74;
}
.button:active,
.button:focus,
.button:hover {
  background-color: #ffffff;
  transition: box-shadow 0.3s ease;
  color: #1d3225;
  border-color: #3f6a53;
  box-shadow: 0 4px 16px rgb(36, 74, 49);
  border-width: 3px;
}
.new_account{
  margin-top: 4px;
}
.text{
  font-weight: 700;
  text-transform: uppercase;
}

</style>