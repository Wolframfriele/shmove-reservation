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
        <v-btn small light color="green accent-3" class="test">Opslaan</v-btn>
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
        title: "Maandag",
        start: "10:00",
        end: "18:00",
        closed: false
      },
      {
        title: "Dinsdag",
        start: "10:00",
        end: "18:00",
        closed: false
      },
      {
        title: "Woensdag",
        start: "10:00",
        end: "18:00",
        closed: false
      },
      {
        title: "Donderdag",
        start: "10:00",
        end: "18:00",
        closed: false
      },
      {
        title: "Vrijdag",
        start: "10:00",
        end: "18:00",
        closed: false
      },
      {
        title: "Zaterdag",
        start: "10:00",
        end: "18:00",
        closed: false
      },
      {
        title: "Zondag",
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
.textfieldContainer:hover .test{
  display: block;
}
.textfield {
  margin: 0 10px;
  max-width: 200px;
}
</style>
