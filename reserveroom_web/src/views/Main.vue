<template>
  <div>
    <div id="panel1-wrapper">
      <Panel1 />
    </div>
    <div id="panel2-wrapper">
      <Panel2 />
    </div>
  </div>
</template>

<script>
import Panel1 from '@/components/Panel1.vue'
import Panel2 from '@/components/Panel2.vue'

export default {
  name: 'Main',
  components: {
    Panel1,
    Panel2
  }
}
</script>

<style lang="scss" scoped>
#panel1-wrapper {
  width: 55%;
  margin: 0;
  float: left;
}
#panel2-wrapper {
  width: calc(45% - 10px);
  display: inline-block;
  margin-left: 5px;
}
</style>
