<template>
  <v-container>
    <v-radio-group v-model="treatment" mandatory>
      <v-radio
        v-for="single_treatment in treatment_options"
        :key="single_treatment"
        :label="single_treatment"
        :value="single_treatment"
        :aria-label="returnAria(single_treatment)"
      ></v-radio>
    </v-radio-group>
  </v-container>
</template>

<script>
import { bus } from "../main";
import axios from "axios";

export default {
  data() {
    return {
      treatment_options: [],
      treatment: ""
    };
  },
  created() {
    axios.get("get_treatments/").then(res => {
      this.treatment = res.data[0].treatment;
      res.data.forEach(element => {
        this.treatment_options.push(element.treatment);
      });
      bus.$emit("treatmentArray", this.treatment);
    });
  },
  methods: {
    changeBehandeling() {
      bus.$emit("treatmentArray", this.treatment);
    },
    returnAria(input_treatment) {
      return `Selecteer Type Afspraak: ${input_treatment}`;
    }
  }
};
</script>
