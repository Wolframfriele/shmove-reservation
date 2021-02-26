<template>
  <v-container class="treatmentContainer">
    <h2>Behandelingen wijzigen</h2>
    <v-row v-for="treatment in treatments" v-bind:key="treatment.id">
      <v-col cols="2">
        <div v-if="treatment.treatment">
          <v-subheader>{{ treatment.treatment }}</v-subheader>
        </div>
        <div v-else>
          <v-subheader>Nieuwe behandeling</v-subheader>
        </div>
      </v-col>
      <v-col cols="10" class="textfieldContainer">
        <form @submit.prevent="saveTreatment">
        <v-text-field
          class="textfield"
          label="Naam"
          :value="treatment.treatment"
          v-model="treatment.treatment"
        ></v-text-field>
        <v-text-field
          class="textfield price"
          label="Prijs"
          :value="treatment.price"
          v-model="treatment.price"
          :prefix="currency"
          type="number"
        ></v-text-field>
        <div v-if="treatment.treatment">
          <v-btn class="mx-2 minus" fab dark x-small color="red lighten-2" @click="deleteTreatment(treatment.id)">
            <v-icon dark>
              mdi-minus
            </v-icon>
          </v-btn>
          <v-btn class="mx-2 save" fab dark x-small color="green lighten-2" @click="saveTreatment(treatment.treatment, treatment.price)" >
            <v-icon dark>
              mdi-check
            </v-icon>
          </v-btn>
        </div>
        <div v-else>
          <v-btn class="mx-2 minus" fab dark x-small color="green lighten-2" @click="saveTreatment(treatment.treatment, treatment.price)">
            <v-icon dark>
              mdi-check
            </v-icon>
          </v-btn>
        </div>
        </form>
      </v-col>
    </v-row>
    <v-btn class="mx-2 plus" fab dark color="teal" @click="addTreatment">
      <v-icon dark>
        mdi-plus
      </v-icon>
    </v-btn>
  </v-container>
</template>

<script>
import axios from "axios";
export default {
  data: () => ({
    currency: "€",
    treatments: [],
    prijs: "",
    behandeling: ""
  }),
  created() {
    let self = this;
    axios.get(`${this.$store.state.HOST}/api/dashboard/get_treatments/`, {
    headers: {
            Accept: "application/json",
            "Content-type": "application/json",
            "X-CSRFToken": self.$session.get('token'),
             Authorization: `Token ${self.$session.get('token')}`,
    }})
    .then(res=>{
      res.data.forEach(element => {
        this.treatments.push(element)
      })
    })
  },
  methods: {
    addTreatment() {
      this.treatments.push({
        treatment: "",
        price: ""
      });
    },
    deleteTreatment(id) {
      axios
        .delete('dashboard/delete_treatments/', {
          params: {
            id: id
          },
          headers: {
            Accept: "application/json",
            "Content-type": "application/json",
            "X-CSRFToken": this.$session.get('token'),
             Authorization: `Token ${this.$session.get('token')}`,
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

    },
    saveTreatment(treatment, price){
      let body = {
        body: {
          name: treatment,
          price: price
        }
      };
      axios
        .put('dashboard/update_treatments/', body,{
        headers: {
            Accept: "application/json",
            "Content-type": "application/json",
            "X-CSRFToken": this.$session.get('token'),
             Authorization: `Token ${this.$session.get('token')}`,
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
    }
};
</script>
<style scoped>
.plus {
  position: absolute;
  left: 25%;
}
h2 {
  margin-bottom: 20px;
}
.treatmentContainer.container {
  margin-bottom: 80px;
}
.textfieldContainer {
  display: flex;
  flex-flow: row wrap;
  position: relative;
  max-width: 80%;
}
.textfield {
  margin: 0 10px;
  max-width: 200px;
}
.price,
.duration {
  width: 100px;
}
form {
  display: flex;
}
</style>
