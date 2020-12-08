<template>
  <v-container>
    <v-row align-content="center" align="center">
      <v-col align="center">
        <h2>Type Afspraak:</h2>
        <v-checkbox input-value="true" label="Shiatsu Therapie" align="center" v-model="shiatsu" @click:event="changeBehandeling"></v-checkbox>
        <v-checkbox input-value="false" label="Voedingsadvies" align="center" v-model="voeding" @click:event="changeBehandeling"></v-checkbox>
      </v-col>
    </v-row>
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
      // if (knippen == true) {
      //   this.treatment.push()
      // }
      bus.$emit('changeBehandeling', this.treatment);
    }
  }
};
</script>
