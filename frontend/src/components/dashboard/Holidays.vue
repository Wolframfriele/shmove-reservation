<template>
  <v-container class="holidayContainer">
    <h1>Vakantiedagen inplannen</h1>
    <h2>Geplande vakantie's</h2>
    <v-container class="plannedHolidays">
      <div v-for="days in planneddays" :key="days.id">
        <div class="plannedHolidayContainer">
        <h4>{{days.title}}</h4>
        <v-menu
              ref="menuOne"
              v-model="menuOne"
              :close-on-content-click="false"
              :return-value.sync="days.start_date"
              transition="scale-transition"
              offset-y
              min-width="auto"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  v-model="days.start_date"
                  label="Eind dag"
                  prepend-icon="mdi-calendar"
                  readonly
                  v-bind="attrs"
                  v-on="on"
                ></v-text-field>
              </template>
              <v-date-picker
                v-model="days.start_date"
                no-title
                scrollable
                :max="days.end_date"
              >
                <v-spacer></v-spacer>
                <v-btn text color="primary" @click="menuOne = false">
                  Cancel
                </v-btn>
                <v-btn
                  text
                  color="primary"
                  @click="$refs.menuOne.save(days.start_date)"
                >
                  OK
                </v-btn>
              </v-date-picker>
            </v-menu>
          <v-menu
              ref="menuTwo"
              v-model="menuTwo"
              :close-on-content-click="false"
              :return-value.sync="days.end_date"
              transition="scale-transition"
              offset-y
              min-width="auto"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  v-model="days.end_date"
                  label="Eind dag"
                  prepend-icon="mdi-calendar"
                  readonly
                  v-bind="attrs"
                  v-on="on"
                ></v-text-field>
              </template>
              <v-date-picker
                v-model="days.end_date"
                no-title
                scrollable
                :min="days.start_date"
              >
                <v-spacer></v-spacer>
                <v-btn text color="primary" @click="menuTwo = false">
                  Cancel
                </v-btn>
                <v-btn
                  text
                  color="primary"
                  @click="$refs.menuTwo.save(days.end_date)"
                >
                  OK
                </v-btn>
              </v-date-picker>
            </v-menu>
      </div>
        </div>
    </v-container>
  </v-container>
</template>

<script>
export default {
  data: () => ({
    currency: "€",
    menuOne: "",
    menuTwo: "",
    planneddays: [
      {
        id: "1",
        title: "Vakantie Bali",
        start_date: "2021-02-02",
        end_date: "2021-04-04",
      },
      {
        id: "2",
        title: "Vakantie Bali",
        start_date: "2021-02-02",
        end_date: "2021-04-04",
      },
      {
        id: "3",
        title: "Vakantie Bali",
        start_date: "2021-02-02",
        end_date: "2021-04-04",
      }
    ]
  }),
  methods: {

  }
};
</script>
<style scoped>
.holidayContainer h1, .holidayContainer h2 {
  margin-left: 12px;
}
.plannedHolidays {
  display: flex;
  flex-flow: row wrap;
  justify-content: flex-start;
  margin: 0;
}
.plannedHolidayContainer {
  margin: 30px;
}
.plannedHolidayContainer:first-child {
  margin-left: 0;
}
.newHoliday {
  margin: 0;
  display:flex;
  flex-flow: column;
  max-width: 290px;
}
h1 {
  margin-bottom: 20px;
}
.holidayContainer.container {
  margin-bottom: 80px;
}

</style>
