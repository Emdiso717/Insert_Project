import { createRouter, createWebHistory } from 'vue-router'
import LoginVue from '@/components/login.vue'
import MainVue from  '@/components/main.vue'
import SearchingVue from '@/components/searching.vue';
import DetailsVue from '@/components/insectshow.vue';
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
            path:'/searching',
            component : SearchingVue,
        },
        {
            path:'/details',
            name:'Details',
            component : DetailsVue,
            props: true
        }
    ]

})
export default router