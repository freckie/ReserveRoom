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
              @click:append="showPassword2 = !showPassword2"
              required
            >
            </v-text-field>
          </v-col>
        </v-row>
        <v-btn depressed color="#891a2b" id="signin-btn">비밀번호 변경</v-btn>
      </v-container>

    </v-form>

    <!-- Tooltip Form -->
    <div class="white-form" id="tooltip-form">
      비밀번호는 필수로 변경해주세요.
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
