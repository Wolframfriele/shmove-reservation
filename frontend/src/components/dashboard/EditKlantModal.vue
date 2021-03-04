<template>
<v-container id="wrap-modal">
  <v-card color="grey lighten-4" flat>
    <v-toolbar color="teal">
      <v-spacer></v-spacer>
      <v-btn @click="saveCustomer">Opslaan</v-btn>
    </v-toolbar>
    <v-card-text>
      <!-- Bewerk Persoonsgegevens -->
      <v-text-field label="Voornaam" v-model="firstName"></v-text-field>
      <v-text-field label="Achternaam" v-model="lastName"></v-text-field>
      <v-text-field label="Email" v-model="email"></v-text-field>
      <v-text-field
        label="Telefoon Nummer"
        v-model="phoneNumber"
      ></v-text-field>
    </v-card-text>
    <v-card-actions>
      <v-btn text color="gray" @click="closeModal">Terug</v-btn>
      <v-spacer></v-spacer>
      <v-btn color="red" @click="deleteCheck = true" class="white--text"
        >Verwijder Klant</v-btn
      >
    </v-card-actions>
  </v-card>
  <v-overlay v-model="deleteCheck">
    <v-card width="400px">
      <v-card-text>
        <h2>Weet je zeker dat je de klant wilt verwijderen?</h2>
        <br />
        <p>
          Pas op! Het verwijderen van een klant verwijdert ook alle
          bijbehorende afspraken. Dit kan niet ongedaan gemaakt worden.
        </p>
      </v-card-text>
      <v-card-text class="center">
        <v-btn text color="gray" @click="deleteCheck = false">Anuleren</v-btn>
        <v-btn color="red" @click="deleteCustomer" class="white--text"
          >Verwijder Afspraak</v-btn
        >
      </v-card-text>
    </v-card>
  </v-overlay>
</v-container>
</template>

<script>
import { bus } from "../../main";
import axios from "axios";

export default {
  props: ["selectedKlant"],
  data: () => ({
    customer_id: "",
    firstName: "",
    lastName: "",
    email: "",
    phoneNumber: "",
    deleteCheck: false
  }),
  created() {
    this.customer_id = this.selectedKlant.customer_id;
    this.firstName = this.selectedKlant.firstName;
    this.lastName = this.selectedKlant.lastName;
    this.email = this.selectedKlant.email;
    this.phoneNumber = this.selectedKlant.phoneNumber;
  },
  watch: {
    selectedKlant: function() {
      this.customer_id = this.selectedKlant.customer_id;
      this.firstName = this.selectedKlant.firstName;
      this.lastName = this.selectedKlant.lastName;
      this.email = this.selectedKlant.email;
      this.phoneNumber = this.selectedKlant.phoneNumber;
    }
  },
  methods: {
    closeModal() {
      this.$emit("closeKlantModal", true);
    },
    saveCustomer() {
      let body = {
        body: {
          customer_id: this.customer_id,
          first_name: this.firstName,
          last_name: this.lastName,
          email: this.email,
          phone_number: this.phoneNumber
        }
      };
      axios
        .put("dashboard/change_client/", body, {
          headers: {
            Accept: "application/json",
            "Content-type": "application/json",
            "X-CSRFToken": this.$session.get("token"),
            Authorization: `Token ${this.$session.get("token")}`
          }
        })
        .then(res => {
          if (res.data == "Success") {
            this.$emit("closeKlantModal", true);
            this.$emit("reloadKlanten");
          }
        })
        .catch(e => {
          console.log(e);
        });
    },
    deleteCustomer() {
      let body = {
        body: {
          customer_id: this.customer_id
        }
      };
      axios
        .post("dashboard/delete_client/", body, {
          headers: {
            Accept: "application/json",
            "Content-type": "application/json",
            "X-CSRFToken": this.$session.get("token"),
            Authorization: `Token ${this.$session.get("token")}`
          }
        })
        .then(res => {
          if (res.data == "Success") {
            this.deleteCheck = false;
            this.$emit("closeKlantModal", true);
            this.$emit("reloadKlanten");
            bus.$emit("updateCalendar");
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
#wrap-modal {
  padding: 0px;
  margin: 0px;
}

.center {
  margin: auto;
}

#delete-box {
  width: 400px;
}
</style>
