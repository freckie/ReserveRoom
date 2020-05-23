<template>
  <div>
    <!-- Logo -->
    <div id="logo-wrapper">
      <img :src="imgLogo" width="150px" />
      <br>
      <span id="logo-title">대면 시험 강의실 예약 서비스</span>
    </div>

    <!-- Form -->
    <v-form class="white-form" id="signin-form">
      <v-container>
        <v-row>
          <v-col>
            <v-text-field
              v-model="password"
              :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
              :type="showPassword ? 'text' : 'password'"
              label="새로운 비밀번호"
              v-on:keyup.enter="reqResetPW"
              @click:append="showPassword = !showPassword"
              required
            >
            </v-text-field>
          </v-col>
        </v-row>

        <v-row>
          <v-col>
            <v-text-field
              v-model="password2"
              :append-icon="showPassword2 ? 'mdi-eye' : 'mdi-eye-off'"
              :type="showPassword2 ? 'text' : 'password'"
              label="새로운 비밀번호 (확인)"
              v-on:keyup.enter="reqResetPW"
              @click:append="showPassword2 = !showPassword2"
              required
            >
            </v-text-field>
          </v-col>
        </v-row>
        <v-btn
          depressed
          color="#891a2b"
          id="signin-btn"
          @click="reqResetPW"
        >
          비밀번호 변경
        </v-btn>
      </v-container>

    </v-form>

    <!-- Tooltip Form -->
    <div class="white-form" id="tooltip-form">
      새로운 비밀번호는 신중히 결정 부탁드립니다.
    </div>
  </div>
</template>

<script>
export default {
  name: 'ResetPW',
  props: {
    imgLogo: {
      type: String,
      default: require('@/assets/khu-logo.png')
    }
  },
  data: () => {
    return {
      password: '',
      password2: '',
      showPassword: false,
      showPassword2: false
    }
  },
  methods: {
    reqResetPW () {
      if (this.password === '' || this.password === null || this.password2 === '' || this.password2 === null) {
        alert('변경할 비밀번호를 입력해주세요.')
        return
      }

      if (this.password !== this.password2) {
        alert('새로운 비밀번호가 서로 일치하지 않습니다.')
        return
      }

      var url = this.$store.getters.getHost + '/api/auth/resetpw'
      var token = this.$store.getters.getAccessToken
      var newPassword = this.password
      this.$http
        .post(
          url, {
            new_password: newPassword
          }, {
            headers: {
              Authorization: 'Bearer ' + token,
              'Content-Type': 'application/json'
            }
          })
        .then(res => {
          alert('비밀번호 변경이 성공했습니다!')
          this.redirect()
        })
        .catch(error => {
          console.log(error.response)
          alert('비밀번호 변경이 실패했습니다.')
        })
    },
    redirect () {
      var user = this.$store.getters.getUserInfo
      if (user.level === 9) {
        this.$router.push('/admin/main')
      } else {
        this.$router.push('/mymenu/main')
      }
    }
  }
}
</script>

<style lang="scss" scoped>
#logo-wrapper {
  margin-top: 30px;

  #logo-title {
    font-size: 1.3rem;
    cursor: default;
  }
}

.white-form {
  max-width: 600px;
  margin: 0 auto;
  padding: 10px;

  border: 1px solid rgba(238, 238, 238, 0.801);
  border-radius: 15px;

  background-color: #ffffff;
}

#signin-form {
  margin-top: 30px;

  #signin-btn {
    width: 100%;
    color: white;
  }
}

#tooltip-form {
  margin-top: 10px;
}
</style>
