import Vue from 'vue'
import VueRouter from 'vue-router'

import store from '../store'

import MainLayout from '@/components/layouts/MainLayout.vue'
import AdminMainLayout from '@/components/layouts/AdminMainLayout.vue'

import Signin from '@/views/Signin.vue'
import ResetPW from '@/views/ResetPW.vue'

import Main from '@/views/Main.vue'
import AdminMain from '@/views/AdminMain.vue'

Vue.use(VueRouter)

const requireAuth = () => (from, to, next) => {
  if (store.getters.getAccessToken !== null) {
    var refreshToken = store.getters.getRefreshToken
    store.dispatch('REFRESH', { refreshToken })
    return next()
  } else {
    console.log('Unauthorized.')
    alert('로그인이 필요한 서비스입니다.')
    next('/signin')
  }
}

const onlyAdmin = () => (from, to, next) => {
  if (store.getters.getAccessToken !== null) {
    var refreshToken = store.getters.getRefreshToken
    store.dispatch('REFRESH', { refreshToken })
    return next()
  } else {
    console.log('Unauthenticated.')
    alert('관리자만 접근이 가능한 메뉴입니다.')
    next('/signin')
  }
}

const routes = [
  {
    path: '/',
    redirect: '/signin'
  },
  {
    path: '/signin',
    name: 'Signin',
    component: Signin
  },
  {
    path: '/resetpw',
    name: 'ResetPW',
    component: ResetPW,
    beforeEnter: requireAuth()
  },
  /* Toolbar Layout */
  {
    path: '/mymenu',
    component: MainLayout,
    redirect: '/mymenu/main',
    children: [
      {
        path: '/mymenu/main',
        name: 'Main',
        component: Main,
        beforeEnter: requireAuth()
      }
    ]
  },
  /* AdminToolbar Layout */
  {
    path: '/admin',
    component: AdminMainLayout,
    redirect: '/admin/main',
    children: [
      {
        path: '/admin/main',
        name: 'AdminMain',
        component: AdminMain,
        beforeEnter: onlyAdmin()
      }
    ]
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
