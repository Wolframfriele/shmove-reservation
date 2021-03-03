<template>
  <validation-observer ref="observer" v-slot="{}">
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
        name="Telefoon Nummer"
        :rules="{
          required: true
        }"
      >
        <v-text-field
          v-model="phonenumber"
          :error-messages="errors"
          label="Telefoon Nummer"
          outlined
          required
        ></v-text-field>
      </validation-provider>
      <v-textarea
        outlined
        v-model="reason"
        name="reden"
        label="Reden voor de behandeling"
        value="Omschrijf wat voor klachten u heeft, of wat voor andere reden."
      ></v-textarea>
      <p>
        Uw selectie is <strong>{{ dateToZin($route.params.start) }}</strong
        >.
      </p>
      <p class="caption">
        Annuleren is kosteloos tot 48 uur van tevoren, daarna wordt de
        gereserveerde tijd in principe in rekening gebracht.
      </p>

      <validation-provider v-slot="{ errors }" rules="required" name="checkbox">
        <v-checkbox
          v-model="accepted"
          :error-messages="errors"
          input-value="false"
          label="Ja, ik ga akkoord met de algemene voorwaarden."
          type="checkbox"
        >
          <template v-slot:label>
            <div>
              ja, ik ga akkoord met de
              <v-tooltip bottom>
                <template v-slot:activator="{ on }">
                  <a
                    target="_blank"
                    href="https://www.shiatsu-delft.nl/privacy-beleid/"
                    @click.stop
                    v-on="on"
                  >
                    algemene voorwaarden.
                  </a>
                </template>
                Opent in nieuw venster
              </v-tooltip>
            </div>
          </template>
        </v-checkbox>
      </validation-provider>
      <span id="error-message"
        >Er is iets mis gegaan met het bevestigen van de afspraak, probeert U
        het nog eens of neem contact op met de beheerder.</span
      >
      <v-btn @click="back">
        Terug
      </v-btn>

      <v-btn class="mr-4" color="primary" type="submit" :disabled="!accepted">
        Bevestig
      </v-btn>
    </form>
  </validation-observer>
</template>

<script>
import axios from "axios";
import repeatedFunctions from "../mixins/repeatedFunctions";
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
  message: "{_field_} moet minstens {length} characters lang zijn. ({_value_})"
});

extend("required", {
  ...required,
  message: "{_field_} is verplicht"
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
  mixins: [repeatedFunctions],
  components: {
    ValidationProvider,
    ValidationObserver
  },
  props: ["date"],

  data: () => ({
    firstname: "",
    lastname: "",
    email: "",
    phonenumber: "",
    accepted: false,
    reason: "",
    error: ""
  }),

  created() {},

  methods: {
    submit() {
      this.$refs.observer.validate();
      axios
        .post("appointments/new_appointment/", {
          body: {
            date_booked_start: this.parseDate(this.$route.params.start),
            date_booked_end: this.parseDate(this.$route.params.end),
            treatment: this.$route.params.treatment,
            reason: this.reason,
            first_name: this.firstname,
            last_name: this.lastname,
            email: this.email,
            phone_number: this.phonenumber
          }
        })
        .then(res => {
          const error = res.data.error;
          if (error == "None") {
            this.$router.push({
              name: "AfspraakGeboekt",
              params: { time: this.dateToString(this.$route.params.start) }
            });
          } else {
            document.getElementById("error-message").style.display =
              "inline-block";
          }
        })
        .catch(e => {
          console.log(e);
          if (e != "") {
            document.getElementById("error-message").style.display =
              "inline-block";
          }
        });
    },
    back() {
      this.$router.push("afspraak-maken");
    },
    dateToZin(datum) {
      const days = [
        "zondag",
        "maandag",
        "dinsdag",
        "woensdag",
        "donderdag",
        "vrijdag",
        "zaterdag"
      ];
      const months = [
        "januari",
        "februari",
        "maart",
        "april",
        "mei",
        "juni",
        "juli",
        "augustus",
        "september",
        "oktober",
        "november",
        "december"
      ];
      const reserverings_tijd = new Date(datum);

      const dayIndex = reserverings_tijd.getDay();
      const day = days[dayIndex];
      const date = reserverings_tijd.getDate();
      const monthIndex = reserverings_tijd.getMonth();
      const month = months[monthIndex];
      const hours = reserverings_tijd.getHours();
      // const minutes = String(reserverings_tijd.getMinutes()).padStart(2, '0');

      return `${day} ${date} ${month} om ${hours}`;
    },
  }
};
</script>

<style scoped>
.mr-4 {
  margin-left: 3em;
}

#error-message {
  color: red;
  display: none;
  padding: 5px;
}
</style>
