import Signin from '@/pages/Signin.vue'

import Vue from 'vue'
import VueRouter from 'vue-router'

// import store from '../store'

import Home from '../views/Home.vue'

Vue.use(VueRouter)

// const requireAuth = () => (from, to, next) => {
//   if (store.getters.getAccessToken !== null) {
//     var refreshToken = store.getters.getRefreshToken
//     store.dispatch('REFRESH', { refreshToken })
//     return next()
//   } else {
//     console.log("Unauthorized.");
//     alert("로그인이 필요한 서비스입니다.");
//     next("/signin");
//   }
// }

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/signin',
    name: 'Signin',
    component: Signin
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
