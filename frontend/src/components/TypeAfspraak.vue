<template>
<<<<<<< HEAD
=======
<<<<<<< HEAD
  <v-container>
    <h2>Type Afspraak:</h2>
    <v-checkbox input-value="true" label="Shiatsu Therapie" v-model="shiatsu" @click:event="changeBehandeling"></v-checkbox>
    <v-checkbox input-value="false" label="Voedingsadvies" v-model="voeding" @click:event="changeBehandeling"></v-checkbox>
=======
>>>>>>> 3327489e70c390d7285e91d02e4be219f984bf3a
  <v-container fluid>
    <h2>Type Behandeling:</h2>
    <v-checkbox
      input-value="true"
      label="Knippen"
      value
    ></v-checkbox>
    <v-checkbox
      input-value="false"
      label="verven"
      value
    ></v-checkbox>
    <h2>Haarlengte:</h2>
    <v-radio-group v-model="haarLengte">
      <v-radio
        key="1"
        label="Kort"
        value="1"
      ></v-radio>
      <v-radio
        key="2"
        label="Halflang"
        value="2"
      ></v-radio>
      <v-radio
        key="3"
        label="Lang"
        value="3"
      ></v-radio>
    </v-radio-group>
    <h2>Keuze Stylist:</h2>
    <v-radio-group v-model="stylistkeuze">
      <v-radio
        key="1"
        label="Geen Voorkeur"
        value="1"
      ></v-radio>
      <v-radio
        key="2"
        label="Shane"
        value="2"
      ></v-radio>
      <v-radio
        key="3"
        label="Declan"
        value="3"
      ></v-radio>
    </v-radio-group>
<<<<<<< HEAD
=======
>>>>>>> 6d2b6ad... frontend merged
>>>>>>> 3327489e70c390d7285e91d02e4be219f984bf3a
  </v-container>
</template>

<script>
<<<<<<< HEAD
=======
<<<<<<< HEAD
import { bus } from '../main'
export default {
  data() {
    return {
      shiatsu: true,
      voeding: false,
      treatment: []
    };
  },
  methods: {
    changeBehandeling () {
      if (this.shiatsu == true) {
        this.treatment.push("shiatsu")
      }
      if (this.voeding == true) {
        this.treatment.push("voeding")
      }
      bus.$emit('changeBehandeling', this.treatment);
    }
  }
};
</script>
=======
>>>>>>> 3327489e70c390d7285e91d02e4be219f984bf3a
  export default {
    data () {
      return {
        haarLengte: 1,
        stylistkeuze: 1,
      }
    },
  }
<<<<<<< HEAD
</script>
=======
</script>
>>>>>>> 6d2b6ad... frontend merged
>>>>>>> 3327489e70c390d7285e91d02e4be219f984bf3a
