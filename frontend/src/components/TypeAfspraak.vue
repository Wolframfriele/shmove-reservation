<template>
  <v-container>
    <v-checkbox 
      v-for="single_treatment in treatment_options" :key="single_treatment" 
      :label="single_treatment" 
      v-model="treatment" 
      :value="single_treatment" 
      @click="changeBehandeling"
      :aria-label="returnAria(single_treatment)"></v-checkbox>
    <!-- <v-checkbox input-value="true" value="shiatsu" label="Shiatsu Therapie" v-model="treatment" @click="changeBehandeling" aria-label="Selecteer Type Afspraak: Shiatsu Therapie"></v-checkbox>
    <v-checkbox input-value="false" value="voeding" label="Voedingsadvies" v-model="treatment" @click="changeBehandeling" aria-label="Selecteer Type Afspraak: Voedingsadvies"></v-checkbox> -->
  </v-container>
</template>

<script>
import { bus } from '../main'
import axios from "axios"

export default {
  data() {
    return {
      treatment_options:[],
      treatment: []
    };
  },
  created () {
    axios.get(`${this.$store.state.HOST}/api/get_treatments/`)
    .then(res=>{
      this.treatment.push(res.data[0].treatment)
      res.data.forEach(element => {
        this.treatment_options.push(element.treatment)
      })
    })
  },
  methods: {
    changeBehandeling () {
      bus.$emit('treatmentArray', this.treatment);
    },
    returnAria (input_treatment) {
      return `Selecteer Type Afspraak: ${input_treatment}`
    }
  }
};
</script>
