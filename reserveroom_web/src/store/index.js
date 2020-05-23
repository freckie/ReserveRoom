import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

import createPersistedState from 'vuex-persistedstate'

Vue.use(Vuex)

// JWT
var jwtDecode = require('jwt-decode')

const resourceHost = 'http://15.164.93.91:8000'

export default new Vuex.Store({
  plugins: [
    createPersistedState({
      storage: window.sessionStorage
    })
  ],
  state: {
    // for global constants.
    host: resourceHost,
    // state variables for Auth.
    accessToken: null,
    refreshToken: null,
    userEmail: null,
    userName: null,
    userLevel: null
  },
  getters: {
    getHost: state => {
      return state.host
    },
    getAccessToken: state => {
      return state.accessToken
    },
    getRefreshToken: state => {
      return state.refreshToken
    },
    getUserInfo: state => {
      return {
        email: state.userEmail,
        name: state.userName,
        level: state.userLevel
      }
    }
  },
  mutations: {
    LOGIN (
      state, {
        accessToken,
        refreshToken,
        userEmail,
        userName,
        userLevel
      }
    ) {
      state.accessToken = accessToken
      state.refreshToken = refreshToken
      state.userEmail = userEmail
      state.userName = userName
      state.userLevel = userLevel
    },
    LOGOUT (state) {
      state.accessToken = null
      state.refreshToken = null
      state.userEmail = null
      state.userName = null
      state.userLevel = null
    }
  },
  actions: {
    LOGIN ({ commit }, { email, password }) {
      return axios
        .post(
          `${resourceHost}/api/auth/signin`, {
            email: email,
            password: password
          }, {
            headers: {
              'Content-Type': 'application/json'
            }
          }
        )
        .then(res => {
          var data = res.data.data
          var atoken = jwtDecode(data.access_token)
          var userClaims = atoken.user_claims
          console.log('로그인 성공. %s님 환영합니다.', userClaims.name)

          // commit LOGIN Action
          commit('LOGIN', {
            accessToken: data.access_token,
            refreshToken: data.refresh_token,
            userEmail: userClaims.email,
            userName: userClaims.name,
            userLevel: userClaims.level
          })
        })
    },
    LOGOUT ({ commit }) {
      commit('LOGOUT')
    },
    REFRESH ({ commit }, { refreshToken }) {
      return axios
        .post(
          `${resourceHost}/api/auth/refresh`, {}, {
            headers: {
              'Content-Type': 'application/json',
              Authorization: 'Bearer ' + refreshToken
            }
          }
        )
        .then(res => {
          var data = res.data.data
          var atoken = jwtDecode(data.access_token)
          var userClaims = atoken.user_claims
          console.log('세션 연장 성공. %s님 환영합니다.', userClaims.name)

          // commit LOGIN Action
          commit('LOGIN', {
            accessToken: data.access_token,
            refreshToken: data.refresh_token,
            userEmail: userClaims.email,
            userName: userClaims.name,
            userLevel: userClaims.level
          })
        })
        .catch(error => {
          console.log('Refresh 실패.')
          console.log(error)
          alert('세션 연장 실패.' + error)
        })
    }
  },
  modules: {
  }
})
