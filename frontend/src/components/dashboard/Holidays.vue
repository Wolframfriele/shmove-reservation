<template>
  <v-container class="holidayContainer">
    <h1>Vakantiedagen inplannen</h1>
    <h2>Geplande vakantie's</h2>
    <v-container class="plannedHolidays">
      <div v-for="days in planneddays" :key="days.id">
        <div class="plannedHolidayContainer">
        <h4>{{days.title}}</h4>
        <v-date-picker
        v-model="days.dates"
        range
      ></v-date-picker>
      </div>
        </div>
    </v-container>
    <h2>Nieuwe vakantie inplannen</h2>
    <v-container class="newHoliday">
      <v-text-field value="Titel"></v-text-field>
      <v-date-picker
        range
      ></v-date-picker>
      <v-btn
              color="green"
              dark
              large
            >
              Inplannen
            </v-btn>
    </v-container>
  </v-container>
</template>

<script>
export default {
  data: () => ({
    currency: "€",
    planneddays: [
      {
        id: "1",
        title: "Vakantie Bali",
        dates: ['2021-01-10', '2021-01-20']
      },
      {
        id: "2",
        title: "Vakantie Spanje",
        dates: ['2021-01-10', '2021-01-20']
      },
      {
        id: "3",
        title: "Vakantie Drenthe",
        dates: ['2021-01-10', '2021-01-20']
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
