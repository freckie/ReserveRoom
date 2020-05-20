<template>
  <v-card id="main-panel2">
    <!-- Timetable -->

    <!-- Reservation Form -->
    <v-form id="reservation-form">
      <div class="form-title">
        <span>새로운 예약</span>
      </div>
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
          <v-col>
            <v-text-field
              v-model="reservation.userName"
              label="교수명"
              hide-details="true"
              outlined
              dense
            >
            </v-text-field>
          </v-col>
        </v-row>

        <v-row>
          <v-col>
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
          <v-col>
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
        </v-row>

        <v-row>
          <v-col>
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
</template>

<script>
export default {
  name: 'Panel2',
  data: () => {
    return {
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
    .form-title {
      text-align: left;
      margin-left: 10px;

      span {
        margin-top: 10px;
        font-size: 1.3rem;
      }
    }

    #ok-btn {
      color: white;
    }
  }
}
</style>
