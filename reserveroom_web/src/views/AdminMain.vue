<template>
  <div>
    <div id="a-panel1-wrapper">
      <AdminPanel1 />
    </div>
    <div id="a-panel2-wrapper">
      <AdminPanel2 />
    </div>
  </div>
</template>

<script>
import AdminPanel1 from '@/components/AdminPanel1.vue'
import AdminPanel2 from '@/components/AdminPanel2.vue'

export default {
  name: 'AdminMain',
  components: {
    AdminPanel1,
    AdminPanel2
  }
}
</script>

<style lang="scss" scoped>
#a-panel1-wrapper {
  width: 55%;
  margin: 0;
  float: left;
}
#a-panel2-wrapper {
  width: calc(45% - 10px);
  display: inline-block;
  margin-left: 5px;
}
</style>
