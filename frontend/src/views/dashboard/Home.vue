<template id="dashboard">
  <v-container>
    <v-card>
      <v-tabs v-model="tab">
        <v-tab v-for="item in items" :key="item.title">
          {{ item.title }} <v-icon class="icon"> {{ item.icon }} </v-icon>
        </v-tab>
      </v-tabs>
      <v-tabs-items v-model="tab">
        <v-tab-item v-for="item in items" :key="item.title">
          <v-card flat>
            <v-card-text>
              <component v-bind:is="item.content"></component>
            </v-card-text>
          </v-card>
        </v-tab-item>
      </v-tabs-items>
    </v-card>
  </v-container>
</template>
<script>
// import axios from 'axios';
import Calendar from "../../components/dashboard/Calendar";
import OpeningTimes from "@/components/dashboard/Openingtimes";
import Treatments from "@/components/dashboard/Treatments";
export default {
  data: () => ({
    tab: null,
    items: [
      { title: "Agenda",
        icon: "mdi-calendar",
        content: "Calendar" },
      {
        title: "Behandelingen",
        icon: "mdi-basket-plus",
        content: "Treatments"
      },
      {
        title: "Openingstijden",
        icon: "mdi-storefront",
        content: "OpeningTimes"
      }
    ]
  }),
  components: {
    Calendar,
    OpeningTimes,
    Treatments
  },
  created() {},
  mounted() {},
  methods: {}
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
.icon {
  margin-left: 8px;
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
