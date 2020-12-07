<template>
  <v-main>
    <validation-observer ref="observer" v-slot="{ invalid }">
      <form @submit.prevent="submit">
        <validation-provider v-slot="{ errors }" name="Naam">
          <v-text-field
            v-model="name"
            :error-messages="errors"
            label="Naam"
            outlined
            required
          ></v-text-field>
        </validation-provider>
        <validation-provider
          v-slot="{ errors }"
          name="email"
          rules="required|email"
        >
          <v-text-field
            v-model="email"
            :error-messages="errors"
            label="E-mail"
            outlined
            required
          ></v-text-field>
        </validation-provider>
        <p>
          U wordt <strong>{{ convertDate }}</strong> geknipt door <strong>Shane</strong>.
        </p>
        <validation-provider
          v-slot="{ errors }"
          rules="required"
          name="checkbox"
        >
          <v-checkbox
            v-model="checkbox"
            :error-messages="errors"
            value="1"
            label="Ja, ik ga akkoord met de algemene voorwaarden."
            type="checkbox"
            required
          ></v-checkbox>
        </validation-provider>

        <v-btn @click="back">
          Terug
        </v-btn>

        <v-btn class="mr-4" color="primary" type="submit" :disabled="invalid">
          Bevestig
        </v-btn>
      </form>
    </validation-observer>
  </v-main>
</template>

<script>
import { required, digits, email, max, regex } from "vee-validate/dist/rules";
import {
  extend,
  ValidationObserver,
  ValidationProvider,
  setInteractionMode
} from "vee-validate";

setInteractionMode("eager");

extend("digits", {
  ...digits,
  message: "{_field_} needs to be {length} digits. ({_value_})"
});

extend("required", {
  ...required,
  message: "{_field_} can not be empty"
});

extend("max", {
  ...max,
  message: "{_field_} may not be greater than {length} characters"
});

extend("regex", {
  ...regex,
  message: "{_field_} {_value_} does not match {regex}"
});

extend("email", {
  ...email,
  message: "Email must be valid"
});

export default {
  components: {
    ValidationProvider,
    ValidationObserver
  },
  props: ["date"],
  data: () => ({
    name: "",
    email: "",
    checkbox: null,
  }),
  methods: {
    findDate () {
      
    },
    submit() {
      this.$refs.observer.validate()
      this.$router.push("afspraak-geboekt")
    },
    back() {
      this.$router.push("afspraak-maken")
    }
  },
  computed: {
    convertDate: function () {
      const days = [
        'zondag',
        'maandag',
        'dinsdag',
        'woensdag',
        'donderdag',
        'vrijdag',
        'zaterdag'
      ];
      const months = [
        'januari',
        'februari',
        'maart',
        'april',
        'mei',
        'juni',
        'juli',
        'augustus',
        'september',
        'oktober',
        'november',
        'december'
      ];
      const reserverings_tijd = new Date(this.$route.params.date);

      console.log(reserverings_tijd)
      const dayIndex = reserverings_tijd.getDay();
      const day = days[dayIndex];
      const date = reserverings_tijd.getDate();
      const monthIndex = reserverings_tijd.getMonth();
      const month = months[monthIndex];
      const hours = reserverings_tijd.getHours();
      const minutes = reserverings_tijd.getMinutes();

      return `${ day } ${ date } ${ month } om ${ hours }:${ minutes }`;
    }
  }
};
</script>

<style scoped>
.mr-4 {
  margin-left: 3em;
}
</style>
