<template>
  <div id="main-panel2">

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
      roomData: {
        id: '전101',
        reservations: [
          { date: '6/22 (월)', startTime: '09 : 00', endTime: '10 : 00' },
          { date: '6/22 (월)', startTime: '10 : 15', endTime: '10 : 30' },
          { date: '6/22 (월)', startTime: '11 : 00', endTime: '13 : 00' },
          { date: '6/22 (월)', startTime: '13 : 30', endTime: '14 : 45' },
          { date: '6/22 (월)', startTime: '15 : 00', endTime: '16 : 45' }
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
    this.createTimeItems()
  },
  methods: {
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
