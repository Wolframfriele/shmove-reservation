<template id="signin">
  <v-container>
    <v-container fill-height="fill-height">
      <div class="outerContainer">
        <h1>Inloggen</h1>
        <div class="mainContainer">
          <div class="innerContainer">
            <validation-observer ref="observer" v-slot="{ invalid }">
              <form @submit.prevent="submit">
                <validation-provider
                  v-slot="{ errors }"
                  name="Username"
                  rules="required"
                >
                  <v-text-field
                    v-model="username"
                    :error-messages="errors"
                    label="Username"
                    required
                  ></v-text-field>
                </validation-provider>
                <validation-provider
                  v-slot="{ errors }"
                  name="password"
                  :rules="{
                    required: true,
                    digits: 7,
                    regex: '^(71|72|74|76|81|82|84|85|86|87|88|89)\\d{5}$'
                  }"
                >
                  <v-text-field
                    v-model="password"
                    :error-messages="errors"
                    label="Password"
                    required
                  ></v-text-field>
                </validation-provider>
                <v-btn class="mr-4" type="submit" :disabled="invalid">
                  submit
                </v-btn>
                <v-btn @click="clear">
                  clear
                </v-btn>
              </form>
            </validation-observer>
          </div>
        </div>
      </div>
    </v-container>
  </v-container>
</template>
<script>
import { required, regex } from "vee-validate/dist/rules";
import {
  extend,
  ValidationObserver,
  ValidationProvider,
  setInteractionMode
} from "vee-validate";
setInteractionMode("eager");

extend("required", {
  ...required,
  message: "{_field_} can not be empty"
});
extend("regex", {
  ...regex,
  message: "{_field_} {_value_} does not match {regex}"
});
// import axios from 'axios';
export default {
  data: () => ({
    username: "",
    password: ""
  }),
  components: {
    ValidationProvider,
    ValidationObserver
  },
  created() {},
  mounted() {},
  methods: {
    submit() {
      this.$refs.observer.validate();
    },
    clear() {
      this.username = "";
      this.password = "";
      this.$refs.observer.reset();
    }
  }
};
</script>
<style scoped>
.outerContainer {
  max-width: 800px;
  max-height: 800px;
  height: 100%;
  width: 100%;
  margin: 0 auto;

  text-align: center;
}
.mainContainer {

}
.innerContainer {

}
</style>
