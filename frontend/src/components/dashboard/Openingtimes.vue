<template>
  <v-container>
    <h2>Openingstijden wijzigen</h2>
    <v-row v-for="day in days" :key="day.title">
      <v-col cols="2">
        <v-subheader>{{ day.title }}</v-subheader>
      </v-col>
      <v-col cols="10" class="textfieldContainer">
                <v-text-field
          class="textfield"
          label="Openingstijd"
          :value="day.start"
        ></v-text-field>
        <v-text-field
          class="textfield"
          label="Sluittijd"
          :value="day.end"
        ></v-text-field>
          <v-switch
          v-model="day.closed"
          label="Gesloten"
          :value="day.closed"
          ></v-switch>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data: () => ({
    currency: "€",
    days: [
      {
        title: "Monday",
        start: "10:00",
        end: "18:00",
        closed: false
      },
      {
        title: "Tuesday",
        start: "10:00",
        end: "18:00",
        closed: false
      },
      {
        title: "Wednesday",
        start: "10:00",
        end: "18:00",
        closed: false
      },
      {
        title: "Thursday",
        start: "10:00",
        end: "18:00",
        closed: false
      },
      {
        title: "Friday",
        start: "10:00",
        end: "18:00",
        closed: false
      },
      {
        title: "Saturday",
        start: "10:00",
        end: "18:00",
        closed: false
      },
      {
        title: "Sunday",
        start: "10:00",
        end: "18:00",
        closed: true
      }
    ]
  }),
  methods: {}
};
</script>
<style scoped>
.textfieldContainer {
  display: flex;
  flex-flow: row wrap;
  justify-content: space-between;
}
.textfield {
  margin: 0 10px;
}
</style>
