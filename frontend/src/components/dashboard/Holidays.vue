<template>
  <v-container class="holidayContainer">
    <h1>Vakantiedagen inplannen</h1>
    <h2>Geplande vakantie's</h2>
    <v-container class="plannedHolidays">
      <div v-for="(days, i) in planneddays" :key="i">
        <div class="plannedHolidayContainer">
          <v-text-field class="margin"
          label="Vakantie naam"
          :value="days.name"
          required
        ></v-text-field>
          <v-text-field class="margin"
          label="Begin datum (YYYY-mm-dd)"
          :value="days.start_date"
          required
        ></v-text-field>
        <v-text-field class="margin"
          label="Eind datum (YYYY-mm-dd)"
          :value="days.end_date"
          required
        ></v-text-field>
    <v-btn
      class="ma-2"
      outlined
      color="indigo lighten-2"
      @click="updateVacation(days.id)"
    >
      Aanpassen
    </v-btn>
    <v-btn
      class="ma-2"
      outlined
      color="red lighten-2"
      @click="deleteVacation(days.id)"
    >
      Verwijderen
    </v-btn>
      </div>
        </div>
    </v-container>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  data: () => ({
    currency: "€",
    menuOne: "",
    menuTwo: "",
    planneddays: []
  }),
  created() {
    this.getVacations();
  },
  methods: {
    async getVacations() {
      let self = this;
      await axios
        .get(`${self.$store.state.HOST}/api/dash_appointments/get_vacations/`, {
          headers: {
            Accept: "application/json",
            "Content-type": "application/json",
            "X-CSRFToken": self.$session.get("token"),
            Authorization: `Token ${self.$session.get("token")}`
          }
        })
        .then(res => {
          res.data.forEach(element => {
            this.planneddays.push(element);
          });
        });
    },
    updateVacation(id,name,start_date,end_date){
      let self = this;
      let body = {
        body: {
          id: id,
          name: name,
          start_date: start_date,
          end_date
        }
      };
      axios
        .put(`${self.$store.state.HOST}/api/dash_appointments/change_vacation/`, body,{
          headers: {
            Accept: "application/json",
            "Content-type": "application/json",
            "X-CSRFToken": self.$session.get('token'),
             Authorization: `Token ${self.$session.get('token')}`,
          }
        })
        .then(res => {
          //Perform Success Action
          console.log(res.data);
          window.location.reload();
        })
        .catch(error => {
          console.log(error);
        })
    },
    deleteVacation(id){ //Not yet pushed to Yanickhost it seems :(
      let self = this;
      axios
        .delete(`${this.$store.state.HOST}/api/dashboard/delete_vacation/`, {
          params: {
            id: id
          },
          headers: {
            Accept: "application/json",
            "Content-type": "application/json",
            "X-CSRFToken": self.$session.get('token'),
             Authorization: `Token ${self.$session.get('token')}`,
          }
        })
        .then(res => {
          //Perform Success Action
          console.log(res.data);
          window.location.reload();
        })
        .catch(error => {
          console.log(error);
        });
    }
  }
};
</script>
<style scoped>
.holidayContainer h1, .holidayContainer h2 {
  margin-left: 12px;
}
.plannedHolidays {
  display: flex;
  flex-flow: row wrap;
  justify-content: flex-start;
  margin: 0;
}
.plannedHolidayContainer {
  margin: 30px;
}
.plannedHolidayContainer:first-child {
  margin-left: 0;
}
.margin {
  margin: 8px;
}
.plannedHolidayContainer p, .plannedHolidayContainer h4{
  margin: 8px;
  text-transform: Capitalize;
}
.newHoliday {
  margin: 0;
  display:flex;
  flex-flow: column;
  max-width: 290px;
}
h1 {
  margin-bottom: 20px;
}
.holidayContainer.container {
  margin-bottom: 80px;
}

</style>
