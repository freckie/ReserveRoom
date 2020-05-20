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
      </div>
    </v-toolbar-title>
    <v-spacer></v-spacer>

    <!-- User Info -->
    <div id="toolbar-user-info">
      <v-icon>mdi-account-circle</v-icon>
      <span>{{ user.name }} 교수님</span>
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
    }
  },
  data: () => {
    return {
      user: {
        name: '김명현'
      }
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
}
</style>
