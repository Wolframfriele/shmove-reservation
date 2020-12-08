<template>
  <v-container>
    <v-row>
      <v-col>
        <h2>Type Behandeling:</h2>
        <v-checkbox input-value="true" label="Knippen" v-model="knippen" @click:event="changeBehandeling"></v-checkbox>
        <v-checkbox input-value="false" label="verven" v-model="verven" @click:event="changeBehandeling"></v-checkbox>
      </v-col>
      <v-col>
      <h2>Haarlengte:</h2>
        <v-radio-group v-model="haarLengte">
          <v-radio key="1" label="Kort" value="1"></v-radio>
          <v-radio key="2" label="Halflang" value="2"></v-radio>
          <v-radio key="3" label="Lang" value="3"></v-radio>
        </v-radio-group>
      </v-col>
      <v-col>
        <h2>Keuze Stylist:</h2>
        <v-radio-group v-model="stylistkeuze">
          <v-radio key="1" label="Geen Voorkeur" value="1"></v-radio>
          <v-radio key="2" label="Shane" value="2"></v-radio>
          <v-radio key="3" label="Declan" value="3"></v-radio>
        </v-radio-group>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { bus } from '../main'
export default {
  data() {
    return {
      knippen: true,
      verven: false,
      haarLengte: "1",
      stylistkeuze:"1",
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
