<template>
<<<<<<< HEAD
  <v-main>
    <validation-observer ref="observer" v-slot="{ invalid }">
      <form @submit.prevent="submit">
        <validation-provider v-slot="{ errors }" name="Voornaam">
          <v-text-field
            v-model="firstname"
            :error-messages="errors"
            label="Voornaam"
            outlined
            required
          ></v-text-field>
        </validation-provider>
        <validation-provider v-slot="{ errors }" name="Achternaam">
          <v-text-field
            v-model="lastname"
            :error-messages="errors"
            label="Achternaam"
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
        <validation-provider
        v-slot="{ errors }"
        name="phoneNumber"
        :rules="{
          required: true,
        }"
      >
        <v-text-field
          v-model="phonenumber"
          :error-messages="errors"
          label="Telefoon Nummer"
=======
<v-main>
  <validation-observer
    ref="observer"
    v-slot="{ invalid }"
  >
    <form @submit.prevent="submit">
      <validation-provider
        v-slot="{ errors }"
        name="Naam"
      >
        <v-text-field
          v-model="name"
          :error-messages="errors"
          label="Naam"
>>>>>>> All reservation steps and call appointments via api
          outlined
          required
        ></v-text-field>
      </validation-provider>
<<<<<<< HEAD
        <p>
          Uw afspraak staat gepland voor <strong>{{ convertDate }}</strong>. De afspraak duurt ongeveer 2 uur.
        </p>
        <p class="caption">
          Annuleren is kosteloos tot 48 uur van tevoren, daarna wordt de gereserveerde tijd in principe in rekening gebracht. 
        </p>
        <validation-provider
          v-slot="{ errors }"
          rules="required"
          name="checkbox"
        >
          <v-checkbox
            v-model="accepted"
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
import axios from "axios";
import { required, digits, email, max, regex } from "vee-validate/dist/rules";
import {
  extend,
  ValidationObserver,
  ValidationProvider,
  setInteractionMode
} from "vee-validate";

setInteractionMode("lazy");

extend("digits", {
  ...digits,
  message: "{_field_} needs to be {length} digits. ({_value_})"
});

extend("required", {
  ...required,
  message: "{_field_} kan niet leeg zijn"
});

extend("max", {
  ...max,
  message: "{_field_} mag niet langer dan {length} zijn"
});

extend("regex", {
  ...regex,
  message: "{_field_} {_value_} matched niet met {regex}"
});

extend("email", {
  ...email,
  message: "Email moet een valide adres zijn"
});

export default {
  components: {
    ValidationProvider,
    ValidationObserver
  },
  props: ["date"],
  data: () => ({
    firstname: "",
    lastname: "",
    email: "",
    phonenumber: '',
    accepted: null,
  }),
  methods: {
    submit() {
      this.$refs.observer.validate()
      axios.post(' http://127.0.0.1:8000/api/appointments/new_appointment/', 
        {
        firstname: this.firstname,
        lastname: this.lastname,
        email: this.email,
        phone_number: this.phonenumber,
        start: this.$route.params.start,
        end: this.$route.params.end,
        treatment: this.$route.params.treatment,
        } 
      )
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
      const reserverings_tijd = new Date(this.$route.params.start);

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
=======
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
      <p>U wordt <strong>Zaterdag 29 November</strong> om <strong>13:30</strong> geknipt door <strong>Shane</strong>.</p>
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

      <v-btn
        class="mr-4"
        color="primary"
        type="submit"
        :disabled="invalid"
      >
        Bevestig
      </v-btn>
    </form>
  </validation-observer>
</v-main>
</template>

<script>
  import { required, digits, email, max, regex } from 'vee-validate/dist/rules'
  import { extend, ValidationObserver, ValidationProvider, setInteractionMode } from 'vee-validate'

  setInteractionMode('eager')

  extend('digits', {
    ...digits,
    message: '{_field_} needs to be {length} digits. ({_value_})',
  })

  extend('required', {
    ...required,
    message: '{_field_} can not be empty',
  })

  extend('max', {
    ...max,
    message: '{_field_} may not be greater than {length} characters',
  })

  extend('regex', {
    ...regex,
    message: '{_field_} {_value_} does not match {regex}',
  })

  extend('email', {
    ...email,
    message: 'Email must be valid',
  })

  export default {
    components: {
      ValidationProvider,
      ValidationObserver,
    },
    data: () => ({
      name: '',
      phoneNumber: '',
      email: '',
      select: null,
      items: [
        'Item 1',
        'Item 2',
        'Item 3',
        'Item 4',
      ],
      checkbox: null,
    }),

    methods: {
      submit () {
        this.$refs.observer.validate()
        this.$router.push('afspraak-geboekt')
      },
      back () {
        this.$router.push('afspraak-maken')
      },
    },
  }
</script>


<style scoped>
  .mr-4 {
    margin-left: 3em;
  }
</style>
>>>>>>> All reservation steps and call appointments via api
