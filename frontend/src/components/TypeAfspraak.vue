<template>
  <v-container>
    <v-checkbox input-value="true" value="shiatsu" label="Shiatsu Therapie" v-model="treatment" @click="changeBehandeling" aria-label="Selecteer Type Afspraak: Shiatsu Therapie"></v-checkbox>
    <v-checkbox input-value="false" value="voeding" label="Voedingsadvies" v-model="treatment" @click="changeBehandeling" aria-label="Selecteer Type Afspraak: Voedingsadvies"></v-checkbox>
  </v-container>
</template>

<script>
import { bus } from '../main'
export default {
  data() {
    return {
      treatment: ["shiatsu"]
    };
  },
  methods: {
    changeBehandeling () {
      bus.$emit('treatmentArray', this.treatment);
    }
  }
};
</script>
