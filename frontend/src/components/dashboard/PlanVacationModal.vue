<template>
  <v-card color="grey lighten-4" min-width="350px" flat>
    <v-toolbar color="indigo lighten-1" dark>
      <v-toolbar-title>Plan een vakantie</v-toolbar-title>
      <v-spacer></v-spacer>
    </v-toolbar>
    <form @submit.prevent="addVacation">
      <div class="margin top15">
        <v-text-field
          :counter="150"
          label="Vakantie naam"
          dense
          v-model="vacationTitle"
          prepend-icon="mdi-form-textbox"
        ></v-text-field>
      </div>
      <div class="margin">
        <v-menu
          ref="menuOne"
          v-model="menuOne"
          :close-on-content-click="false"
          :return-value.sync="vacationStartDate"
          transition="scale-transition"
          offset-y
          min-width="auto"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-text-field
              v-model="vacationStartDate"
              label="Start dag"
              prepend-icon="mdi-calendar"
              readonly
              v-bind="attrs"
              v-on="on"
            ></v-text-field>
          </template>
          <v-date-picker
            v-model="vacationStartDate"
            no-title
            scrollable
            :min="vacationStartDate"
            :max="vacationEndDate"
          >
            <v-spacer></v-spacer>
            <v-btn text color="primary" @click="menuOne = false">
              Cancel
            </v-btn>
            <v-btn
              text
              color="primary"
              @click="$refs.menuOne.save(vacationStartDate)"
            >
              OK
            </v-btn>
          </v-date-picker>
        </v-menu>
      </div>
      <div class="margin">
        <v-menu
          ref="menuTwo"
          v-model="menuTwo"
          :close-on-content-click="false"
          :return-value.sync="vacationEndDate"
          transition="scale-transition"
          offset-y
          min-width="auto"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-text-field
              v-model="vacationEndDate"
              label="Eind dag"
              prepend-icon="mdi-calendar"
              readonly
              v-bind="attrs"
              v-on="on"
            ></v-text-field>
          </template>
          <v-date-picker
            v-model="vacationEndDate"
            no-title
            scrollable
            :min="vacationStartDate"
          >
            <v-spacer></v-spacer>
            <v-btn text color="primary" @click="menuTwo = false">
              Cancel
            </v-btn>
            <v-btn
              text
              color="primary"
              @click="$refs.menuTwo.save(vacationEndDate)"
            >
              OK
            </v-btn>
          </v-date-picker>
        </v-menu>
      </div>
      <v-card-actions>
        <v-btn text color="secondary" @click="closeModal">
          Terug
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn text color="orange lighten-2" type="submit">
          Plannen
        </v-btn>
      </v-card-actions>
    </form>
  </v-card>
</template>

<script>
import axios from "axios";

export default {
  props: ['vacationStartDate'],
  data: () => ({
    vacationTitle: "",
    vacationEndDate: "",
    menuOne: "",
    menuTwo: ""
  }),
  methods: {
    addVacation() {
      const start = this.vacationStartDate;
      const end = this.vacationEndDate;
      const title = this.vacationTitle;
      let body = {
        body: {
          name: title,
          start_date: start,
          end_date: end
        }
      };
      axios
        .post('dash_appointments/set_vacation/', body ,{
          headers: {
            Accept: "application/json",
            "Content-type": "application/json",
            "X-CSRFToken": this.$session.get("token"),
            Authorization: `Token ${this.$session.get("token")}`
          },
        })
        .then(res => {
          //Perform Success Action
          console.log(res.data);
          // window.location.reload();
          window.location.reload();
        })
        .catch(error => {
          console.log(error);
        })
        .finally(() => {
          //Perform action in always
        });
    },
    closeModal() {
      this.$emit('closeVacationModal', true)
    }
  }
}
</script>

<style scoped>


</style>