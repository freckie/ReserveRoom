<template>
  <div id="main-panel1">
    <v-card id="control-tab-wrapper">

      <!-- Control Tabs (Header) -->
      <v-tabs
        v-model="controlPanel.tab"
        id="control-tabs-header"
        fixed-tabs
        background-color="#891a2b"
        dark
      >
        <v-tab>전체 강의실 조회</v-tab>
        <v-tab>내 예약 현황 조회</v-tab>
      </v-tabs>

      <!-- Control Tabs (Items) -->
      <v-tabs-items
        v-model="controlPanel.tab"
        class="control-tabs-item"
      >
        <!-- Tab 1 -->
        <v-tab-item>
          <v-card flat>
            <v-row>
              <v-col class="d-flex" cols="2" sm="6">
                <v-select
                  v-model="controlPanel.selectedCollege"
                  :items="controlPanel.colleges"
                  item-text="name"
                  item-value="id"
                  label="단과대학"
                  hide-details="true"
                  outlined
                  dense
                ></v-select>
              </v-col>

              <v-col class="d-flex" cols="2" sm="6">
                <v-select
                  v-model="controlPanel.selectedDate"
                  :items="controlPanel.dates"
                  item-text="value"
                  item-value="id"
                  label="날짜"
                  hide-details="true"
                  outlined
                  dense
                ></v-select>
              </v-col>

              <v-col class="d-flex" cols="2" sm="6">
                <v-text-field
                  v-model="controlPanel.capacity"
                  label="인원"
                  hide-details="true"
                  outlined
                  dense
                  v-on:keyup.enter="getRoomsList"
                >
                </v-text-field>
              </v-col>

              <v-col class="d-flex" cols="2" sm="6">
                <v-btn
                  dense
                  color="#891a2b"
                  id="find-btn"
                  @click="getRoomsList"
                >조회</v-btn>
              </v-col>
            </v-row>
          </v-card>
        </v-tab-item>

        <!-- Tab 2 -->
        <v-tab-item>
          <v-btn
            dense
            color="#891a2b"
            id="find-btn2"
          >조회</v-btn>
        </v-tab-item>
      </v-tabs-items>

    </v-card> <!-- Control Panel End -->

    <!-- Room Table -->
    <v-card id="room-table">
      <v-simple-table>
        <template v-slot:default>
          <thead v-if="controlPanel.tab === 0">
            <tr>
              <th class="text-center">단과대학</th>
              <th class="text-center">호 수</th>
              <th class="text-center">수용 가능 인원</th>
              <th class="text-center">&nbsp;</th>
            </tr>
          </thead>
          <thead v-else>
            <tr>
              <th class="text-center">단과대학</th>
              <th class="text-center">호 수</th>
              <th class="text-center">날 짜</th>
              <th class="text-center">과 목 명</th>
              <th class="text-center">&nbsp;</th>
            </tr>
          </thead>

          <tbody v-if="controlPanel.tab === 0">
            <tr
              v-for="room in rooms"
              :key="room.id"
            >
              <td>{{ room.college }}</td>
              <td>{{ room.id }}</td>
              <td>{{ room.capacity }} 명</td>
              <td>
                <v-btn
                  color="#891a2b"
                  dense
                  class="reserve-btn"
                  @click="getDetail(room)"
                >
                  조회 및 예약 ▶
                </v-btn>
              </td>
            </tr>
          </tbody>
          <tbody v-else>
            <tr
              v-for="(item, idx) in myReservations"
              :key="idx"
            >
              <td>{{ item.college }}</td>
              <td>{{ item.id }}</td>
              <td>{{ item.date }}</td>
              <td>{{ item.subject }}</td>
              <td>
                <v-btn
                  color="#891a2b"
                  dense
                  class="reserve-btn"
                  @click="getDetail(item)"
                >
                  상세 조회 ▶
                </v-btn>
              </td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
    </v-card>

  </div>
</template>

<script>
export default {
  name: 'Panel1',
  data: () => {
    return {
      controlPanel: {
        tab: 0, // 0 or 1
        colleges: [
          { id: 1, name: '전자정보대학' }
        ],
        dates: [
          { id: '2020-06-22', value: '6/22 (월)' },
          { id: '2020-06-23', value: '6/23 (화)' },
          { id: '2020-06-24', value: '6/24 (수)' },
          { id: '2020-06-25', value: '6/25 (목)' },
          { id: '2020-06-26', value: '6/26 (금)' }
        ],
        selectedCollege: null,
        selectedDate: null,
        capacity: null
      },
      myReservations: [
        { college: '전자정보대학', id: '전101', date: '6/22 (월)', subject: '운영체제' },
        { college: '전자정보대학', id: '전102', date: '6/22 (월)', subject: '운영체제' },
        { college: '전자정보대학', id: '전211-2', date: '6/22 (월)', subject: '미분적분학' },
        { college: '전자정보대학', id: '전211-2', date: '6/22 (월)', subject: '선형대수' }
      ],
      rooms: []
    }
  },
  methods: {
    getRoomsList () {
      if (
        this.controlPanel.selectedCollege === null ||
        this.controlPanel.selectedDate === null ||
        this.controlPanel.capacity === null ||
        this.controlPanel.capacity === 0
      ) {
        alert('조회 조건을 모두 세팅해주세요.')
        return
      }

      this.rooms = []
      var url = this.$store.getters.getHost + '/api/rooms'
      var token = this.$store.getters.getAccessToken
      var capacity = this.controlPanel.capacity.replace(/[^0-9]/g, '')
      this.$http
        .get(
          url, {
            params: {
              college_id: Number(this.controlPanel.selectedCollege),
              capacity: capacity
            }
          }, {
            headers: {
              Authorization: 'Bearer ' + token,
              'Content-Type': 'application/json'
            }
          })
        .then(res => {
          var rooms = res.data.data.rooms
          if (rooms.length === 0) {
            alert('검색 결과가 없습니다.')
            return
          }
          rooms.forEach(element => {
            this.rooms.push({
              college: element.college,
              id: element.classroom_id,
              capacity: element.capacity
            })
          })
        })
        .catch(error => {
          console.log(error.response)
          alert('조회가 실패했습니다.')
        })

      console.log(this.controlPanel)
    },
    getDetail (room) {
      window.scrollTo(0, 0)
      this.$emit('getDetailClickEvent', room.id)
    }
  }
}
</script>

<style lang="scss" scoped>
#main-panel1 {
  margin-left: 5px;

  #control-tab-wrapper {
    width: 100%;
    margin-bottom: 10px;

    #control-tabs-header {
      width: 100%;
    }

    .control-tabs-item {
      padding: 0 5px;
    }

    #find-btn {
      color: white;
      height: 40px;
    }

    #find-btn2 {
      color: white;
      height: 40px;
      width: 70%;
      margin: 10px auto;
    }
  }

  #room-table {
    margin-top: 5px;
    margin-bottom: 10px;

    .reserve-btn {
      color: white;
    }
  }
}
</style>
