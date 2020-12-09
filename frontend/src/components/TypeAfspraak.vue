<template>
  <v-container>
    <h2>Type Afspraak:</h2>
    <v-checkbox input-value="true" label="Shiatsu Therapie" v-model="shiatsu" @click:event="changeBehandeling"></v-checkbox>
    <v-checkbox input-value="false" label="Voedingsadvies" v-model="voeding" @click:event="changeBehandeling"></v-checkbox>
  </v-container>
</template>

<script>
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
