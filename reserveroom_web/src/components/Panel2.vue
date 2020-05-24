<template>
  <div id="main-panel2" v-show="show">

    <!-- Reservation Form -->
    <v-card class="panel2-card">
      <v-toolbar color="#891a2b" dark>
        <v-card-title>{{ roomData.id }}호 새로운 예약</v-card-title>
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

          <v-btn depressed color="#891a2b" id="ok-btn">신&nbsp;청</v-btn>
        </v-container>

      </v-form>
    </v-card>

    <!-- Timetable -->
    <v-card class="panel2-card">
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
      roomData: {
        id: '',
        reservations: [
          // { date: '6/22 (월)', startTime: '09 : 00', endTime: '10 : 00' },
          // { date: '6/22 (월)', startTime: '10 : 15', endTime: '10 : 30' },
          // { date: '6/22 (월)', startTime: '11 : 00', endTime: '13 : 00' },
          // { date: '6/22 (월)', startTime: '13 : 30', endTime: '14 : 45' },
          // { date: '6/22 (월)', startTime: '15 : 00', endTime: '16 : 45' }
        ]
      },
      reservation: {
        subject: null,
        userName: null,
        userEmail: null,
        date: null,
        startTime: null,
        endTime: null
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
      }
    }
  },
  created () {
    this.show = false
    this.createTimeItems()
  },
  methods: {
    loadRoomData (roomID) {
      this.roomData.id = roomID
      this.show = true
      this.roomData.reservations = []

      var roomIDs = roomID.split(' ')
      console.log(roomIDs)
      roomIDs.forEach(id => {
        this._loadRoomReservations(id)
      })
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
    _loadRoomReservations (roomID) {
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
            var date = dateTokens[1] + '/' + dateTokens[2] + ' ' + this._dateToday(dateTokens[1], dateTokens[2])
            this.roomData.reservations.push({
              date: date,
              startTime: element.start_time,
              endTime: element.end_time
            })
          })
        })
        .catch(error => {
          console.log(error.response)
          alert('조회가 실패했습니다.')
        })
    },
    _dateToday (month, day) {
      console.log(month, day)
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
    }
  }
}
</script>

<style lang="scss" scoped>
#main-panel2 {

  #reservation-form {

    #ok-btn {
      color: white;
    }
  }
}

.panel2-card {
  margin-bottom: 10px;
}
</style>
