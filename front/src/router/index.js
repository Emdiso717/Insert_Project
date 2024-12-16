import { createRouter, createWebHistory } from 'vue-router'
import LoginVue from '@/components/login.vue'
import MainVue from  '@/components/main.vue'
import Result from "@/components/result.vue";
import Tree from "@/components/tree.vue"
const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes:[
        {
            path: '/',
            redirect: '/login'
        },
        {
            path:'/login',
            component : LoginVue
        },
        {
            path:'/main',
            name:'Main',
            component : MainVue,
            props: true
        },
        {
            path:'/result',
            name:'Result',
            component : Result,
        },
        {
            path:'/tree',
            name:'Tree',
            component : Tree,
        }
    ]

})
export default router