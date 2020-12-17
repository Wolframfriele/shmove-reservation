<template>
  <v-container class="treatmentContainer">
    <h2>Behandelingen wijzigen</h2>
    <v-row v-for="(treatment, counter) in treatments" v-bind:key="counter">
      <v-col cols="2">
        <div v-if="treatment.title">
          <v-subheader>{{ treatment.title }}</v-subheader>
        </div>
        <div v-else>
          <v-subheader>Nieuwe behandeling</v-subheader>
        </div>
      </v-col>
      <v-col cols="10" class="textfieldContainer">
        <v-text-field
          class="textfield"
          label="Naam"
          :value="treatment.title"
        ></v-text-field>
        <v-text-field
          class="textfield duration"
          label="Tijdsduur"
          :value="treatment.duration"
          suffix=" Minuten"
        ></v-text-field>
        <v-text-field
          class="textfield price"
          label="Prijs"
          :value="treatment.price"
          :prefix="currency"
        ></v-text-field>
        <div v-if="treatment.title">
          <v-btn class="mx-2 minus" fab dark x-small color="red" @click="deleteTreatment(counter)">
            <v-icon dark>
              mdi-minus
            </v-icon>
          </v-btn>
        </div>
        <div v-else>
          <v-btn class="mx-2 minus" fab dark x-small color="green" @click="saveTreatment">
            <v-icon dark>
              mdi-check
            </v-icon>
          </v-btn>
        </div>
      </v-col>
    </v-row>
    <v-btn class="mx-2 plus" fab dark color="indigo" @click="addTreatment">
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
        duration: "120",
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
    deleteTreatment(counter) {
      this.treatments.splice(counter, 1);
    },
    saveTreatment(){

    }
  }
};
</script>
<style scoped>
.plus {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
}
.minus {
  position: absolute;
  bottom: 25px;
}
h2 {
  margin-bottom: 20px;
}
.treatmentContainer.container {
  margin-bottom: 80px;
}
.textfieldContainer {
  display: flex;
  flex-flow: row wrap;
  position: relative;
  max-width: 80%;
}
.textfield {
  margin: 0 10px;
  max-width: 200px;
}
.price,
.duration {
  width: 100px;
}
</style>
