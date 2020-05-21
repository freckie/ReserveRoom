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
                >
                </v-text-field>
              </v-col>

              <v-col class="d-flex" cols="2" sm="6">
                <v-btn
                  dense
                  color="#891a2b"
                  id="find-btn"
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
          { id: 1, name: '전자정보대학' },
          { id: 2, name: '멀티미디어관' },
          { id: 3, name: '외국어대학' }
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
      rooms: [
        { college: '전자정보대학', id: '전101', capacity: 60 },
        { college: '전자정보대학', id: '전102', capacity: 60 },
        { college: '전자정보대학', id: '전103', capacity: 60 },
        { college: '전자정보대학', id: '전136', capacity: 82 },
        { college: '전자정보대학', id: '전205', capacity: 202 },
        { college: '전자정보대학', id: '전211-1', capacity: 97 },
        { college: '전자정보대학', id: '전211-2', capacity: 37 },
        { college: '전자정보대학', id: '전211-3', capacity: 18 },
        { college: '전자정보대학', id: '전217', capacity: 40 },
        { college: '전자정보대학', id: '전218', capacity: 40 },
        { college: '전자정보대학', id: '전219', capacity: 40 },
        { college: '전자정보대학', id: '전220', capacity: 90 },
        { college: '전자정보대학', id: '전221', capacity: 40 },
        { college: '전자정보대학', id: '전223', capacity: 40 },
        { college: '전자정보대학', id: '전226', capacity: 90 },
        { college: '전자정보대학', id: '전227', capacity: 78 },
        { college: '전자정보대학', id: '전445', capacity: 82 },
        { college: '전자정보대학', id: '전539', capacity: 50 },
        { college: '전자정보대학', id: '전309', capacity: 22 },
        { college: '전자정보대학', id: '전409', capacity: 22 },
        { college: '전자정보대학', id: '전509', capacity: 22 },
        { college: '전자정보대학', id: '전207', capacity: 24 },
        { college: '전자정보대학', id: '전208', capacity: 24 },
        { college: '전자정보대학', id: '전209', capacity: 24 },
        { college: '전자정보대학', id: '전325-2', capacity: 30 },
        { college: '전자정보대학', id: '전333', capacity: 24 },
        { college: '전자정보대학', id: '전B01', capacity: 54 },
        { college: '전자정보대학', id: '전B05', capacity: 40 },
        { college: '전자정보대학', id: '전B06', capacity: 50 },
        { college: '전자정보대학', id: '전B07', capacity: 42 },
        { college: '전자정보대학', id: '전B09', capacity: 42 },
        { college: '전자정보대학', id: '전B11', capacity: 42 }
      ]
    }
  },
  methods: {
    getDetail (room) {
      window.scrollTo(0, 0)
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
