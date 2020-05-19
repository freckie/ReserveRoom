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
          <v-col cols="12" md="4">
            <v-text-field
              v-model="email"
              label="이메일"
              required
            >
            </v-text-field>
          </v-col>

          <v-col cols="12" md="4">
            <v-text-field
              v-model="password"
              label="비밀번호"
              required
            >
            </v-text-field>
          </v-col>
        </v-row>
        <v-btn depressed color="#891a2b" id="signin-btn">로그인</v-btn>
      </v-container>

    </v-form>

    <!-- Tooltip Form -->
    <div class="white-form" id="tooltip-form">
      초기 비밀번호는 <span style="color: #036eb8">1111</span> 입니다.
      최초 로그인 후 변경해주세요.
    </div>
  </div>
</template>

<script>
export default {
  name: 'Signin',
  props: {
    imgLogo: {
      type: String,
      default: require('@/assets/khu-logo.png')
    }
  },
  data: () => {
    return {
      email: '',
      password: ''
    }
  }
}
</script>

<style lang="scss" scoped>
#logo-wrapper {
  margin-top: 30px;

  #logo-title {
    font-size: 1.3rem;
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
