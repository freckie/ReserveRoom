<template>
  <div>
    <!-- Logo -->
    <div class="logo-wrapper">
      <img :src="imgLogo" />
      <span class="display-1">대면 시험 강의실 예약 서비스</span>
    </div>

    <!-- Form -->
    <div class="signin-form">
    </div>

    <!-- Tooltip Form -->
    <div class="tooltip-form">
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
  }
}
</script>

<style lang="scss" scoped>

</style>
