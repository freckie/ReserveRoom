<template>
  <div>
    <div id="panel1-wrapper">
      <Panel1 />
    </div>
  </div>
</template>

<script>
import Panel1 from '@/components/Panel1.vue'
export default {
  name: 'Main',
  components: {
    Panel1
  }
}
</script>

<style lang="scss" scoped>
#panel1-wrapper {
  position: relative;
  width: 60%;
  margin: 0;
  // top: 48px;
}
</style>
