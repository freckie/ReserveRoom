<template>
  <v-toolbar id="top-toolbar" dense align-center>
    <!-- Back -->
    <v-btn
      color="#891a2b"
      text
      @click="refresh"
    >
      세션 만료까지 {{ tokenExpiryDiffStr }}
    </v-btn>

    <!-- Centered Logo -->
    <v-spacer></v-spacer>
    <v-toolbar-title>
      <div>
        <img :src="imgLogo" width="50px" />
        <span v-if="admin" id="logo-admin">Admin</span>
      </div>
    </v-toolbar-title>
    <v-spacer></v-spacer>

    <!-- User Info -->
    <div id="toolbar-user-info">
      <v-icon>mdi-account-circle</v-icon>
      <span v-if="!admin">{{ user.name }} 교수님</span>
      <span v-else>{{ user.name }}</span>
    </div>
  </v-toolbar>
</template>

<script>
export default {
  name: 'Toolbar',
  props: {
    imgLogo: {
      type: String,
      default: require('@/assets/khu-logo.png')
    },
    admin: {
      type: Boolean,
      default: false
    }
  },
  created () {
    this.loadUserData()

    // 세션 시간 표시 타이머
    this.startTimer()
    this.$store.watch(
      () => this.$store.getters.getAccessToken,
      accessToken => {
        if (accessToken !== null) {
          this.clearTimer()
          this.startTimer()
        }
      }
    )
  },
  data: () => {
    return {
      user: {
        name: ''
      },
      tokenExpiryDiffStr: '',
      timer: null
    }
  },
  methods: {
    refresh () {
      var refreshToken = this.$store.getters.getRefreshToken
      this.$store.dispatch('REFRESH', { refreshToken })
    },
    loadUserData () {
      var user = this.$store.getters.getUserInfo
      this.user.name = user.name
    },
    startTimer () {
      if (this.$store.state.accessToken !== null) {
        var vm = this

        var expiry = this.$store.state.accessTokenExpiry
        var target = this.$moment.unix(expiry)
        var now = this.$moment(new Date()).unix() * 1000
        var diff = target.diff(now) / 1000

        this.timer = setInterval(function () {
          vm.tokenExpiryDiffStr = vm.makeTimeFormat(diff)
          diff -= 1

          if (diff < 1) {
            clearInterval(vm.timer)
            alert('로그인 세션이 만료되었습니다.')
            vm.$router.push('/signin')
          }
        }, 1000)
      }
    },
    clearTimer () {
      clearInterval(this.timer)
    },
    makeTimeFormat (sec) {
      var seconds = sec % 60
      var minutes = (sec - seconds) / 60

      var result = ''
      if (minutes < 10) {
        result += '0' + minutes
      } else {
        result += String(minutes)
      }

      if (seconds < 10) {
        result += ':0' + seconds
      } else {
        result += ':' + seconds
      }

      return result
    }
  }
}
</script>

<style lang="scss" scoped>
#top-toolbar {
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 1000;

  #logo-admin {
    font-size: 0.825rem;
    color: #891a2b;
  }
}
</style>
