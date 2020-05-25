<template>
  <div>
    <div id="a-panel1-wrapper">
      <AdminPanel1
        @getPanel2HideEvent="listenToPanel2Hide"
        @getDetailClickEvent="listenToPanel1Detail"
        @getReservationDetailClickEvent="listenToPanel1ReservationDetail"
      />
    </div>
    <div id="a-panel2-wrapper">
      <AdminPanel2
        ref="panel2"
      />
    </div>
  </div>
</template>

<script>
import AdminPanel1 from '@/components/AdminPanel1.vue'
import AdminPanel2 from '@/components/AdminPanel2.vue'

export default {
  name: 'Main',
  components: {
    AdminPanel1,
    AdminPanel2
  },
  data: () => {
    return {
      panel2Data: {
        roomID: null,
        reservationID: null
      }
    }
  },
  methods: {
    listenToPanel1Detail (roomID) {
      this.panel2Data.roomID = roomID
      this.$refs.panel2._clearForm()
      this.$refs.panel2.loadRoomData(this.panel2Data.roomID)
    },
    listenToPanel1ReservationDetail (reservationID) {
      this.panel2Data.reservationID = reservationID
      this.$refs.panel2._clearForm()
      this.$refs.panel2._changeMode('update')
      this.$refs.panel2.loadMyReservationData(this.panel2Data.reservationID)
    },
    listenToPanel2Hide () {
      this.$refs.panel2._hidePanel2()
    }
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
