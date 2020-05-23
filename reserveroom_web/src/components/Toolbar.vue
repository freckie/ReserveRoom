<template>
  <v-toolbar id="top-toolbar" dense align-center>
    <!-- Back -->
    <v-btn icon>
      <v-icon>mdi-arrow-left</v-icon>
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
  },
  data: () => {
    return {
      user: {
        name: ''
      }
    }
  },
  methods: {
    loadUserData () {
      var user = this.$store.getters.getUserInfo
      this.user.name = user.name
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
