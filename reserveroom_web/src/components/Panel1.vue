<template>
  <div id="main-panel1">
    <div id="control-tab-wrapper">
      <v-card>

        <!-- Control Tabs (Header) -->
        <v-tabs
          v-model="controlPanel.tab"
          id="control-tabs-header"
          fixed-tabs
          background-color="#891a2b"
          dark
        >
          <v-tab>전체 강의실 조회</v-tab>
          <v-tab>예약 건 보기</v-tab>
        </v-tabs>

        <!-- Control Tabs (Items) -->
        <v-tabs-items
          v-model="controlPanel.tab"
          class="control-tabs-item"
        >
          <!-- Tab 1 -->
          <v-tab-item :key="controlPanel.tabKeys[0]">
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
          <v-tab-item :key="controlPanel.tabKeys[1]">
          </v-tab-item>
        </v-tabs-items>

      </v-card>
    </div> <!-- Control Panel End -->

    <!-- Room Talbe -->
    <v-card id="room-table">
      <v-simple-table>
        <template v-slot:default>
          <thead>
            <tr>
              <th class="text-center">단과대학</th>
              <th class="text-center">호&nbsp;수</th>
              <th class="text-center">수용 가능 인원</th>
              <th class="text-center">&nbsp;</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="room in rooms"
              :key="room.id"
            >
              <td>{{ room.college }}</td>
              <td>{{ room.id }} 호</td>
              <td>{{ room.capacity }} 명</td>
              <td>
                <v-btn
                  color="#891a2b"
                  dense
                  class="reserve-btn"
                >
                  조회 및 예약 ▶
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
        tab: null,
        tabKeys: ['tab1', 'tab2'],
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
      rooms: [
        { college: '전자정보대학', id: '전101', capacity: 30 },
        { college: '전자정보대학', id: '전101', capacity: 30 },
        { college: '전자정보대학', id: '전101', capacity: 30 },
        { college: '전자정보대학', id: '전101', capacity: 30 },
        { college: '전자정보대학', id: '전101', capacity: 30 },
        { college: '전자정보대학', id: '전101', capacity: 30 },
        { college: '전자정보대학', id: '전101', capacity: 30 },
        { college: '전자정보대학', id: '전101', capacity: 30 },
        { college: '전자정보대학', id: '전101', capacity: 30 },
        { college: '전자정보대학', id: '전101', capacity: 30 },
        { college: '전자정보대학', id: '전101', capacity: 30 },
        { college: '전자정보대학', id: '전101', capacity: 30 }
      ]
    }
  }
}
</script>

<style lang="scss" scoped>
#control-tab-wrapper {
  width: 100%;

  #control-tabs-header {
    width: 100%;
  }

  .control-tabs-item {
    padding: 0 5px;
  }

  #find-btn {
    color: white;
  }
}

#room-table {
  margin-top: 5px;
  margin-bottom: 10px;

  .reserve-btn {
    color: white;
  }
}
</style>
