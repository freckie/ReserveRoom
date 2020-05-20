import Vue from 'vue'
import VueRouter from 'vue-router'

// import store from '../store'

import MainLayout from '@/components/layouts/MainLayout.vue'

import Signin from '@/views/Signin.vue'
import ResetPW from '@/views/ResetPW.vue'

import Main from '@/views/Main.vue'

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
    path: '/signin',
    name: 'Signin',
    component: Signin
  },
  {
    path: '/resetpw',
    name: 'ResetPW',
    component: ResetPW
  },
  /* Toolbar Layout */
  {
    path: '/',
    component: MainLayout,
    redirect: '/main',
    children: [
      {
        path: '/main',
        name: 'Main',
        component: Main
      }
    ]
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
