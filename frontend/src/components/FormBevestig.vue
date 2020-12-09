<template>
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