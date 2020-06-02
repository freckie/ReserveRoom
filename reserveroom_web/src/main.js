import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'
import '@mdi/font/css/materialdesignicons.css'
import moment from 'moment'
import VueMomentJS from 'vue-momentjs'

Vue.use(Vuetify)
Vue.use(VueMomentJS, moment)

Vue.config.productionTip = false

// Axios
Vue.prototype.$http = axios
axios.interceptors.request.use(
  function (config) {
    if (store.getters.getAccessToken === null) {
      return config
    }
    var refreshToken = store.getters.getRefreshToken
    if (refreshToken === null || refreshToken === '') {
      return config
    }

    if (config.url.includes('/auth/refresh')) {
      return config
    }
    console.log('refresh 요청 중 ...')
    store.dispatch('REFRESH', { refreshToken })
    return config
  },
  function (error) {
    return Promise.reject(error)
  }
)

new Vue({
  vuetify: new Vuetify(),
  router,
  store,
  render: h => h(App)
}).$mount('#app')
