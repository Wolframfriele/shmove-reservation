<template>
  <v-container class="treatmentContainer">
    <h2>Behandelingen wijzigen</h2>
    <v-row v-for="treatment in treatments" :key="treatment.title">
      <v-col cols="2">
        <v-subheader>{{ treatment.title }}</v-subheader>
      </v-col>
      <v-col cols="10" class="textfieldContainer">
        <v-text-field
          class="textfield"
          :label="treatment.title"
          :value="treatment.title"
        ></v-text-field>
        <v-text-field
          class="textfield"
          label="Duration"
          :value="treatment.duration"
          suffix=" Minuten"
        ></v-text-field>
        <v-text-field
          class="textfield"
          label="Prijs"
          :value="treatment.price"
          :prefix="currency"
        ></v-text-field>
      </v-col>
    </v-row>
    <v-btn
      class="mx-2 plus"
      fab
      dark
      color="indigo"
      @click="addTreatment"
    >
      <v-icon dark>
        mdi-plus
      </v-icon>
    </v-btn>
  </v-container>
</template>

<script>
export default {
  data: () => ({
    currency: "€",
    treatments: [
      {
        title: "Massage",
        icon: "mdi-calendar",
        duration: "120",
        price: "100.00"
      },
      {
        title: "Voedingscoaching",
        icon: "mdi-calendar",
        duration: "60",
        price: "50.00"
      }
    ]
  }),
  methods: {
    addTreatment() {
      this.treatments.push({
        title: "",
        icon: "mdi-calendar",
        duration: "",
        price: ""
      });
    },
    deleteVisa(counter) {
      this.treatments.splice(counter, 1);
    }
  }
};
</script>
<style scoped>
.plus {
  position: absolute;
  right: 20px;
}
h2 {
  margin-bottom: 20px;
}
.treatmentContainer.container {
  margin-bottom: 60px;
}
.textfieldContainer {
  display: flex;
  flex-flow: row wrap;
  justify-content: space-between;
}
.textfield {
  margin: 0 10px;
}
</style>
