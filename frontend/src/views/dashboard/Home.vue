<template id="dashboard">
  <v-container>
    <v-card>
      <v-tabs v-model="tab">
        <v-tab v-for="item in items" :key="item.title">
          {{ item.title }} <v-icon class="icon"> {{ item.icon }} </v-icon>
        </v-tab>
        <v-container class="signout" @click="logOut">
          <div class="signoutbtn">
          Uitloggen<v-icon class="icon"> mdi-exit-to-app </v-icon>
          </div>
        </v-container>
      </v-tabs>
      <v-tabs-items v-model="tab">
        <v-tab-item v-for="item in items" :key="item.title">
          <v-card flat>
            <v-card-text>
              <component v-bind:is="item.content" @changeToVakantie="changeToVakantie"></component>
            </v-card-text>
          </v-card>
        </v-tab-item>
      </v-tabs-items>
    </v-card>
  </v-container>
</template>
<script>
import Calendar from "../../components/dashboard/Calendar";
import Holidays from "@/components/dashboard/Holidays";
import Klanten from "@/components/dashboard/Klanten";
import Settings from "@/components/dashboard/Settings";
// import Statistics from "@/components/dashboard/Statistics";
export default {
  data: () => ({
    tab: null,
    items: [
      { title: "Agenda",
        icon: "mdi-calendar",
        content: "Calendar" },
      {
        title: "Vakanties",
        icon: "mdi-white-balance-sunny",
        content: "Holidays"
      },
      {
        title: "Klanten",
        icon: "mdi-account",
        content: "Klanten"
      },      
      {
        title: "Instellingen",
        icon: "mdi-cog",
        content: "Settings"
      },
      // {
      //   title: "Statistieken",
      //   icon: "mdi-chart-bar",
      //   content: "Statistics"
      // }
    ]
  }),
  components: {
    Calendar,
    Holidays,
    Klanten,
    Settings,
    // Statistics
  },
  // Session check
  beforeCreate: function () {
    if (!this.$session.exists()) {
      this.$router.push({name: "Login"})
    }
  },
  created() {},
  mounted() {},
  methods: {
    logOut: function () {
      this.$session.destroy()
      this.$router.push({name: "Login"})
    },
    changeToVakantie () {
      this.tab = 1
    }
  }
};
</script>
<style>
.v-calendar-daily__scroll-area {
  overflow-y: hidden !important;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.v-calendar-daily__head {
  margin-right: 0;
}

.col{
  padding: 0;
}

html::-webkit-scrollbar {
  width: 0;
  height: 0;
}
</style>
<style scoped>

.container {
  padding: 0;
  margin: 0;
  max-width: 100%;
}
.signout {
  background-color: #7955484d;
  width: 150px;
  height: 48px;
  position: absolute;
  right: 0;
  top: 0;
  cursor: pointer;
  transition: 0.3s ease-in-out;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}
.signout:hover {
  background-color: #795548ab;
  color: #fff;
}
.signout:hover .icon {
  color: #fff;
}
.signoutbtn {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%,-50%);
}
.icon {
  margin-left: 8px;
  transition: 0.3s ease-in-out;
}
.home-core {
  display: flex;
  justify-content: center;
  align-content: center;
  width: 100%;
  height: auto;
  border: 1px solid red;
}
</style>
