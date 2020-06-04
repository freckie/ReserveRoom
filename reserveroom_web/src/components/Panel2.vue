<template>
  <div id="main-panel2" v-show="show">

    <!-- Reservation Form -->
    <v-card class="panel2-card">
      <v-toolbar color="#891a2b" dark>
        <v-card-title v-if="mode==='new'">{{ roomData.id }}호 새로운 예약</v-card-title>
        <v-card-title v-else>{{ roomData.id }}호 예약 수정</v-card-title>
      </v-toolbar>

      <v-form id="reservation-form">
        <v-container>
          <v-row>
            <v-col>
              <v-text-field
                v-model="reservation.subject"
                label="과목명"
                hide-details="true"
                outlined
                dense
              >
              </v-text-field>
            </v-col>
          </v-row>

          <v-row>
            <v-col class="d-flex" cols="6">
              <v-text-field
                v-model="reservation.userName"
                label="교수명"
                hide-details="true"
                outlined
                dense
                disabled
              >
              </v-text-field>
            </v-col>

            <v-col class="d-flex" cols="6">
              <v-select
                v-model="reservation.date"
                :items="selectItems.dates"
                item-text="value"
                item-value="id"
                label="날짜"
                hide-details="true"
                outlined
                dense
              ></v-select>
            </v-col>
          </v-row>

          <v-row>
            <v-col class="d-flex" cols="6">
              <v-select
                v-model="reservation.startTime"
                :items="selectItems.times"
                item-text="value"
                item-value="id"
                label="시작 시간"
                hide-details="true"
                outlined
                dense
              ></v-select>
            </v-col>

            <v-col class="d-flex" cols="6">
              <v-select
                v-model="reservation.endTime"
                :items="selectItems.times"
                item-text="value"
                item-value="id"
                label="종료 시간"
                hide-details="true"
                outlined
                dense
              ></v-select>
            </v-col>
          </v-row>

          <!-- Buttons -->
          <v-btn
            v-if="mode==='new'"
            depressed
            color="#891a2b"
            id="ok-btn"
            @click="createReservation"
          >신&nbsp;청</v-btn>
          <div v-else>
            <v-btn
              depressed
              color="error"
              id="ok-btn"
              @click="deleteReservation"
            >삭&nbsp;제</v-btn>
            <v-btn
              depressed
              color="#891a2b"
              id="ok-btn"
              @click="updateReservation"
            >수&nbsp;정</v-btn>
          </div>
        </v-container>

      </v-form>
    </v-card>

    <!-- Timetable -->
    <v-card
      class="panel2-card"
      v-show="mode==='new'"
    >
      <v-toolbar color="#891a2b" dark>
        <v-card-title>{{ roomData.id }}호 예약 현황</v-card-title>
      </v-toolbar>

      <!-- Reservations Table -->
      <v-simple-table>
        <template v-slot:default>
          <thead>
            <tr>
              <th class="text-center">날짜</th>
              <th class="text-center">시작 시간</th>
              <th class="text-center">종료 시간</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(item, idx) in roomData.reservations"
              :key="idx"
            >
              <td>{{ item.date }}</td>
              <td>{{ item.startTime }}</td>
              <td>{{ item.endTime }}</td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
    </v-card>
  </div>
</template>

<script>
export default {
  name: 'Panel2',
  data: () => {
    return {
      show: false,
      mode: 'new', // 'new' or 'update'
      roomData: {
        id: '',
        reservations: []
      },
      reservation: {
        subject: null,
        userName: null,
        userEmail: null,
        date: null,
        startTime: null,
        endTime: null,
        reservationID: null, // for update
        origin: { // for update
          startTime: null,
          endTime: null
        }
      },
      selectItems: {
        dates: [
          { id: '2020-06-22', value: '6/22 (월)' },
          { id: '2020-06-23', value: '6/23 (화)' },
          { id: '2020-06-24', value: '6/24 (수)' },
          { id: '2020-06-25', value: '6/25 (목)' },
          { id: '2020-06-26', value: '6/26 (금)' }
        ],
        times: []
      },
      sending: false
    }
  },
  created () {
    this.sending = false
    this.show = false
    this.createTimeItems()
  },
  methods: {
    loadRoomData (roomID) {
      // Load Room Metadata
      this.roomData.id = roomID
      this.show = true
      this.mode = 'new'

      // room counts
      this.roomData.count = roomID.split(' ').length

      this._loadRoomReservations(roomID)

      // Load User Info
      var user = this.$store.getters.getUserInfo
      this.reservation.userName = user.name
      this.reservation.userEmail = user.email
    },
    loadMyReservationData (reservationID) {
      // Load Reservation Metadata
      this._loadMyReservation(reservationID)

      // Load User Info
      var user = this.$store.getters.getUserInfo
      this.reservation.userName = user.name
      this.reservation.userEmail = user.email

      this.show = true
      this.mode = 'update'
    },
    createTimeItems () {
      for (var i = 9; i < 20; i++) {
        var hh = ('00' + i).slice(-2)
        for (var j = 0; j < 60; j += 5) {
          var mm = ('00' + j).slice(-2)
          this.selectItems.times.push({
            id: hh + ':' + mm,
            value: hh + ' : ' + mm
          })
        }
      }
    },
    createReservation () {
      if (this.sending) {
        return
      }

      this.sending = true
      // Check all parameters valid
      if (
        this.reservation.subject === '' || this.reservation.subject === null ||
        this.reservation.startTime === '' || this.reservation.startTime === null ||
        this.reservation.endTime === '' || this.reservation.endTime === null ||
        this.reservation.date === '' || this.reservation.date === null
      ) {
        alert('입력이 제대로 됐는지 다시 확인 부탁드립니다.')
        this.sending = false
        return
      }

      // Check time is valid
      if (!this._checkTimeValidation(this.reservation.startTime, this.reservation.endTime)) {
        alert('시간 입력이 잘못되었습니다.')
        this.sending = false
        return
      }

      // Reserve only one room
      var params = {}
      var url = this.$store.getters.getHost
      if (this.roomData.count === 1) {
        url = url + '/api/reservations'
        params = {
          user_email: this.reservation.userEmail,
          classroom_id: this.roomData.id,
          start_time: this.reservation.date + ' ' + this.reservation.startTime,
          end_time: this.reservation.date + ' ' + this.reservation.endTime,
          subject: this.reservation.subject
        }
      // Reserve two rooms
      } else {
        url = url + '/api/reservations2'
        var ids = this.roomData.id.split(' ')
        params = {
          reservations: [
            {
              user_email: this.reservation.userEmail,
              classroom_id: ids[0],
              start_time: this.reservation.date + ' ' + this.reservation.startTime,
              end_time: this.reservation.date + ' ' + this.reservation.endTime,
              subject: this.reservation.subject
            },
            {
              user_email: this.reservation.userEmail,
              classroom_id: ids[1],
              start_time: this.reservation.date + ' ' + this.reservation.startTime,
              end_time: this.reservation.date + ' ' + this.reservation.endTime,
              subject: this.reservation.subject
            }
          ]
        }
      }

      // Request
      var token = this.$store.getters.getAccessToken
      var vm = this
      setTimeout(function () {
        vm.$http
          .post(
            url, params, {
              headers: {
                Authorization: 'Bearer ' + token,
                'Content-Type': 'application/json'
              }
            })
          .then(res => {
            alert('예약 신청이 성공했습니다.')
            this.sending = false
            vm._clearForm()
            vm._loadRoomReservations(vm.roomData.id)
          })
          .catch(error => {
            console.log(error.response)
            alert('예약 신청이 실패했습니다 : ' + error.response.data.message)
            this.sending = false
          })
        vm.sending = false
      }, 500)
    },
    updateReservation () {
      if (this.sending) {
        return
      }

      this.sending = true
      // Check all parameters valid
      if (
        this.reservation.subject === '' || this.reservation.subject === null ||
        this.reservation.startTime === '' || this.reservation.startTime === null ||
        this.reservation.endTime === '' || this.reservation.endTime === null ||
        this.reservation.date === '' || this.reservation.date === null
      ) {
        alert('입력이 제대로 됐는지 다시 확인 부탁드립니다.')
        this.sending = false
        return
      }

      // Check time is valid
      if (!this._checkTimeValidation(this.reservation.startTime, this.reservation.endTime)) {
        alert('시간 입력이 잘못되었습니다.')
        this.sending = false
        return
      }

      // Update reservations
      var params = {}
      var url = this.$store.getters.getHost
      url = url + '/api/reservations/' + this.reservation.reservationID
      params = {
        classroom_id: this.roomData.id,
        start_time: this.reservation.date + ' ' + this.reservation.startTime,
        end_time: this.reservation.date + ' ' + this.reservation.endTime,
        origin_start_time: this.reservation.date + ' ' + this.reservation.origin.startTime,
        origin_end_time: this.reservation.date + ' ' + this.reservation.origin.endTime,
        subject: this.reservation.subject
      }

      // Request
      var token = this.$store.getters.getAccessToken
      var vm = this
      setTimeout(function () {
        vm.$http
          .put(
            url, params, {
              headers: {
                Authorization: 'Bearer ' + token,
                'Content-Type': 'application/json'
              }
            })
          .then(res => {
            alert('기존 예약 수정이 성공했습니다.')
            this.sending = false
            vm._loadRoomReservations(vm.roomData.id)
          })
          .catch(error => {
            console.log(error.response)
            alert('기존 예약 수정이 실패했습니다 : ' + error.response.data.message)
            this.sending = false
            vm._clearForm()
            vm._loadMyReservation(vm.reservation.reservationID)
          })
        this.sending = false
      }, 500)
    },
    deleteReservation () {
      if (this.sending) {
        return
      }

      this.sending = true
      // Check
      var result = prompt('예약이 삭제됩니다.\n계속 진행하시려면 "삭제"를 입력해주세요.')
      if (result !== '삭제') {
        alert('잘못 입력하셨습니다.')
        this.sending = false
        return
      }

      // Update reservations
      var url = this.$store.getters.getHost
      url = url + '/api/reservations/' + this.reservation.reservationID

      // Request
      var token = this.$store.getters.getAccessToken
      var vm = this
      setTimeout(function () {
        vm.$http
          .delete(
            url, {
              headers: {
                Authorization: 'Bearer ' + token,
                'Content-Type': 'application/json'
              }
            }, {})
          .then(res => {
            alert('예약 삭제에 성공했습니다. 페이지가 새로고침됩니다.')
            this.sending = false
            vm._loadRoomReservations(vm.roomData.id)
            vm.sending = false
            vm.$router.go()
          })
          .catch(error => {
            console.log(error.response)
            alert('기존 예약 삭제에 실패했습니다 : ' + error.response.data.message)
            this.sending = false
            vm._clearForm()
            vm._loadMyReservation(vm.reservation.reservationID)
          })
        vm.sending = false
      }, 500)
    },
    _clearForm () {
      this.reservation.subject = null
      this.reservation.startTime = null
      this.reservation.endTime = null
      this.reservation.userName = null
      this.reservation.userEmail = null
      this.reservation.date = null
    },
    _hidePanel2 () {
      this.show = false
    },
    _changeMode (mode) {
      this.mode = mode
    },
    _loadRoomReservations (roomID) {
      this.roomData.reservations = []

      var url = this.$store.getters.getHost + '/api/rooms/detail'
      var token = this.$store.getters.getAccessToken
      this.$http
        .get(
          url, {
            params: {
              room_id: String(roomID)
            },
            headers: {
              Authorization: 'Bearer ' + token,
              'Content-Type': 'application/json'
            }
          })
        .then(res => {
          var rooms = res.data.data.times
          rooms.forEach(element => {
            var dateTokens = element.start_time.split(' ')[0].split('-')
            var date = dateTokens[1] + '/' + dateTokens[2] + ' ' + this._dateToDay(dateTokens[1], dateTokens[2])
            this.roomData.reservations.push({
              date: date,
              startTime: element.start_time,
              endTime: element.end_time
            })
          })
        })
        .catch(error => {
          console.log(error.response)
          alert('조회가 실패했습니다. 다시 시도해주세요.')
        })
      return roomID
    },
    _loadMyReservation (reservationID) {
      // Load Reservation Metadata
      var url = this.$store.getters.getHost + '/api/reservations/' + reservationID
      var token = this.$store.getters.getAccessToken
      this.$http
        .get(url, {
          headers: {
            Authorization: 'Bearer ' + token,
            'Content-Type': 'application/json'
          }
        })
        .then(res => {
          var data = res.data.data.reservation
          this.roomData.id = data.classroom_id
          this.reservation.subject = data.subject
          this.reservation.date = data.start_time.split(' ')[0]
          this.reservation.startTime = data.start_time.split(' ')[1]
          this.reservation.endTime = data.end_time.split(' ')[1]
          this.reservation.reservationID = reservationID
          this.reservation.origin.startTime = this.reservation.startTime
          this.reservation.origin.endTime = this.reservation.endTime
        })
        .catch(error => {
          console.log(error.response)
          alert('조회가 실패했습니다. : ' + error.response.data.message)
        })
    },
    _dateToDay (month, day) {
      if (month === '06') {
        switch (day) {
          case '20':
            return '(토)'
          case '21':
            return '(일)'
          case '22':
            return '(월)'
          case '23':
            return '(화)'
          case '24':
            return '(수)'
          case '25':
            return '(목)'
          case '26':
            return '(금)'
          case '27':
            return '(토)'
        }
      }
      return ''
    },
    _checkTimeValidation (start, end) {
      var startTokens = start.split(':')
      var endTokens = end.split(':')
      if (Number(startTokens[0]) < Number(endTokens[0])) {
        return true
      } else if (Number(startTokens[0]) > Number(endTokens[0])) {
        return false
      } else {
        if (Number(startTokens[1]) < Number(endTokens[1])) {
          return true
        } else {
          return false
        }
      }
    }
  }
}
</script>

<style lang="scss" scoped>
#main-panel2 {

  #reservation-form {

    #ok-btn {
      color: white;
      margin-left: 5px;
      margin-right: 5px;
    }
  }
}

.panel2-card {
  margin-bottom: 10px;
}
</style>
