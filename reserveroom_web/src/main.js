import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'
import '@mdi/font/css/materialdesignicons.css'

Vue.use(Vuetify)

Vue.config.productionTip = false

// Axios
Vue.prototype.$http = axios
axios.interceptors.request.use(
  function (config) {
    var refreshToken = store.getters.getRefreshToken
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
