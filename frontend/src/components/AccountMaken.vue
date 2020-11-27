<template>
<v-main>
  <validation-observer
    ref="observer"
    v-slot="{ invalid }"
  >
    <form @submit.prevent="submit">
      <validation-provider
        v-slot="{ errors }"
        name="Wachtwoord"
      >
        <v-text-field
            v-model="wachtwoord"
            :error-messages="errors"
            :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
            :rules="[rules.required, rules.min]"
            :type="show1 ? 'text' : 'password'"
            name="input-10-1"
            label="Wachtwoord"
            hint="At least 8 characters"
            outlined
            counter
            @click:append="show1 = !show1"
          ></v-text-field>
      </validation-provider>
      <validation-provider
        v-slot="{ errors }"
        name="Wachtwoord Herhalen"
      >
        <v-text-field
            v-model="wachtwoord2"
            :error-messages="errors"
            :append-icon="show2 ? 'mdi-eye' : 'mdi-eye-off'"
            :rules="[rules.required, rules.min, rules.passwordmatch]"
            :type="show1 ? 'text' : 'password'"
            name="input-10-1"
            label="Herhaal Wachtwoord"
            hint="Zelfde als vorige wachtwoord"
            outlined
            @click:append="show1 = !show2"
          ></v-text-field>
      </validation-provider>

      <v-btn
        class="mr-4"
        color="primary"
        type="submit"
        :disabled="invalid"
      >
        Account Aanmaken
      </v-btn>
    </form>
  </validation-observer>
</v-main>
</template>


<script>
  import { required, digits, regex } from 'vee-validate/dist/rules'
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

  extend('regex', {
    ...regex,
    message: '{_field_} {_value_} does not match {regex}',
  })

  export default {
    components: {
      ValidationProvider,
      ValidationObserver,
    },
    data: () => ({
      wachtwoord: '',
      wachtwoord2: '',
      show1: false,
      show2: false,
      password: 'Password',
      rules: {
        required: value => !!value || 'Required.',
        min: v => v.length >= 8 || 'Min 8 characters',
        passwordmatch: input => input == this.wachtwoord || `De wachtwoorden zijn niet hetzelfde`,
      },
    }),

    methods: {
      submit () {
        this.$refs.observer.validate()
      },
    },
  }
</script>


<style scoped>

</style>