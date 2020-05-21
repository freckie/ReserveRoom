<template>
  <v-app>
    <Toolbar :admin="true" />
    <v-content id="content">
      <router-view></router-view>
    </v-content>
  </v-app>
</template>

<script>
import Toolbar from '@/components/Toolbar.vue'
export default {
  name: 'AdminMainLayout',
  components: {
    Toolbar
  }
}
</script>

<style lang="scss" scoped>
#content {
  margin-top: 52px;
}
</style>
