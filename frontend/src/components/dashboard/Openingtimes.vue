<template>
  <v-container>
    <h2>Openingstijden wijzigen</h2>
    <v-row v-for="day in days" :key="day.day_id">
      <v-col cols="2">
        <v-subheader>{{ day.title }}</v-subheader>
      </v-col>
      <v-col v-for="slot in timeslots" :key="slot.day_id" cols="10" class="textfieldContainer">
        <div class="" v-if="day.day_id == slot.day_id">
        <v-text-field
          class="textfield"
          label="Starttijd"
          :value="slot.start"

        ></v-text-field>
        <v-text-field
          class="textfield"
          label="Eindtijd"
          :value="slot.end"
        ></v-text-field>
      </div>
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
        day_id: "0",
        title: "Maandag"
      },
      {
        day_id: "1",
        title: "Dinsdag"
      },
      {
        day_id: "2",
        title: "Woensdag"
      },
      {
        day_id: "3",
        title: "Donderdag"
      },
      {
        day_id: "4",
        title: "Vrijdag"
      },
      {
        day_id: "5",
        title: "Zaterdag"
      },
      {
        day_id: "6",
        title: "Zondag"
      }
    ],
    timeslots: [
      {
        start: "10:00",
        end: "18:00",
        day_id: "0"
      },
      {
        start: "12:00",
        end: "14:00",
        day_id: "0"
      },
      {
        start: "10:00",
        end: "18:00",
        day_id: "1"
      },
      {
        start: "10:00",
        end: "18:00",
        day_id: "2"
      },
      {
        start: "10:00",
        end: "18:00",
        day_id: "3"
      },
      {
        start: "10:00",
        end: "18:00",
        day_id: "4"
      },
      {
        start: "10:00",
        end: "18:00",
        day_id: "5"
      },
      {
        start: "10:00",
        end: "18:00",
        day_id: "6"
      }
    ]
  }),
  computed: {
    // timesliceFilter: function () {
    //   return this.slot.filter(this.day_id == day.day_id)
    // }
  },
  methods: {}
};
</script>
<style scoped>
.test {
  display: none;
  margin-left: 10px;
}
h2 {
  margin-bottom: 20px;
}
.textfieldContainer {
  display: flex;
  flex-flow: row wrap;
  position: relative;
  max-width: 80%;
}
.textfieldContainer:hover .test {
  display: block;
}
.textfield {
  margin: 0 10px;
  max-width: 200px;
}
</style>
