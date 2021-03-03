<template id="signin">
  <v-container class="container" fill-height>
    <v-row align="center" justify="center">
      <v-col>
        <v-card class="card">
          <v-system-bar color="primary" height="200">
            <v-img
              height="160"
              contain
              src="https://www.shiatsu-delft.nl/wp-content/uploads/2016/10/IN-KI-Shiatsu-voeding-logo-1.png"
              background="primary"
            ></v-img>
          </v-system-bar>
          <v-card-title>Inloggen Dashboard</v-card-title>
          <validation-observer ref="observer" v-slot="{ invalid }">
            <form @submit.prevent="submit" class="login">
              <validation-provider
                v-slot="{ errors }"
                name="Email"
                rules="required"
              >
                <v-text-field
                  v-model="email"
                  :error-messages="errors"
                  label="Email"
                  required
                  outlined
                ></v-text-field>
              </validation-provider>
              <validation-provider
                v-slot="{ errors }"
                name="Wachtwoord"
                rules="required"
              >
                <v-text-field
                  v-model="password"
                  :error-messages="errors"
                  :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                  :type="show1 ? 'text' : 'password'"
                  label="Wachtwoord"
                  outlined
                  @click:append="show1 = !show1"
                ></v-text-field>
              </validation-provider>
              <v-btn class="mr-4" large @click="submit" :disabled="invalid"
                >Submit</v-btn
              >
            </form>
            <v-card-subtitle>Shmove Reservations</v-card-subtitle>
          </validation-observer>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
<script>
import { required } from "vee-validate/dist/rules";
import {
  extend,
  ValidationObserver,
  ValidationProvider,
  setInteractionMode
} from "vee-validate";
setInteractionMode("lazy");

extend("required", {
  ...required,
  message: "{_field_} is verplicht"
});
import axios from "axios";
export default {
  data() {
    return {
      show1: false,
      email: "",
      password: "",
      token: "",
      rules: {
        required: value => !!value || "Required.",
        emailMatch: () => `The email and password you entered don't match`
      }
    };
  },
  components: {
    ValidationProvider,
    ValidationObserver
  },
  methods: {
    submit() {
      axios
        .post('signin/', {
          body: {
            email: this.email,
            password: this.password
          }
        })
        .then(res => {
          if (res.data.authenticate == true) {
            this.$session.start();
            this.$session.set("token", res.data.token);
            this.$router.push({ name: "Dashboard" });
          }
        })
        .catch(e => {
          console.log(e);
        });
    }
  }
};
</script>
<style scoped>
.container {
  width: 550px;
}

.login {
  width: 515px;
  margin: auto;
}

.card {
  padding: 0px;
}
</style>
