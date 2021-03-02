<template>
  <v-row>
    <v-col>
      <v-sheet height="64">
        <!-- Calendar Toolbar -->
        <v-toolbar flat>
          <v-btn outlined class="mr-4" color="grey darken-2" @click="setToday" aria-label="Navigeer naar vandaag">
            Today
          </v-btn>
          <v-btn fab text small color="grey darken-2" @click="prev" aria-label="Vorige week">
            <v-icon small>
              mdi-chevron-left
            </v-icon>
          </v-btn>
          <v-btn fab text small color="grey darken-2" @click="next" aria-label="Volgende week">
            <v-icon small>
              mdi-chevron-right
            </v-icon>
          </v-btn>
          <v-toolbar-title v-if="$refs.calendar">
            {{ $refs.calendar.title }}
          </v-toolbar-title>
          <v-spacer> </v-spacer>
        </v-toolbar>
      </v-sheet>
      <v-sheet>
        <v-overlay :absolute="absolute" v-if="loaded == false" opacity="0">
          <v-progress-circular
            :size="70"
            indeterminate
            color="primary"
          ></v-progress-circular>
        </v-overlay>
        <v-calendar
          ref="calendar"
          v-model="focus"
          color="primary"
          :events="events"
          :event-color="getEventColor"
          :type="type"
          :weekdays="weekdays"
          :first-interval="firstinterval"
          :interval-count="intervalcount"
          :interval-format="intervalFormat"
          :locale="locale"
          @click:event="bevestigAfspraak"

          @change="updateRange"
        >
          <!-- Usabillity Modifications -->

          <!-- Modified Calendar Header -->
          <template v-slot:day-label-header="{date, day, present, past, weekday}">
            <v-avatar v-if="past" color="white">{{ day }}</v-avatar>
            <v-avatar v-else-if="present" color="primary" class="white--text">{{ day }}</v-avatar>
            <v-btn v-else fab depressed color="white" :aria-label="dateToString(date)" :href="returnID(weekday)">{{ day }} </v-btn>
          </template>
          <!-- Modified Calendar Events -->
          <template v-slot:event="{event, eventParsed}">
            <p class="event-text">Vrij</p>  
            <p class="event-text" :id="eventParsed.start.weekday" tabindex="0" role="button" @keydown.enter="bevestigAfspraak({event})">
              {{ eventParsed.start.time }} tot {{ eventParsed.end.time }}
            </p>
          </template>
        </v-calendar>
        <v-alert v-if="noEvents" color="primary" class="no-events" width="615">
          <p class="white--text">Er zijn helaas geen vrije plekkken meer voor deze periode.</p>
        </v-alert>
      </v-sheet>
    </v-col>
  </v-row>
</template>

<script>
import { bus } from '../main'
import axios from "axios";
import repeatedFunctions from "../mixins/repeatedFunctions";

export default {
  mixins: [repeatedFunctions],
  data: () => ({
    focus: "",
    type: "week",
    weekdays: [1, 2, 3, 4, 5, 6, 0],
    firstinterval: "9",
    intervalcount: "11",
    locale: "nl",
    eventColor:  ['primary', 'red'],
    treatment: "",
    events: [],
    loaded: false,
    absolute: true,
    noEvents: false,
  }),
  created() {
    // Receive Data from treatments
    bus.$on('treatmentArray', (data) => {
      this.treatment = data;
    })
  },
  mounted() {
    this.$refs.calendar.checkChange();
  },
  methods: {
    returnID(id) {
      return `#${id}`;
    },
    intervalFormat(interval) {
      return interval.time;
    },
    bevestigAfspraak({ event }) {
      bus.$on('treatmentArray', (data) => {
      this.treatment = data;
      })
      this.$router.push({name: "AfspraakBevestigen", params: {start: event.start, end: event.end, treatment: this.treatment}});
    },
    updateRange({ start, end }) {
      this.getFreePlaces(start.date, end.date);
    },
    getFreePlaces(beginweek, endweek){
      this.events = []
      this.noEvents = false
      this.loaded = false
      axios.get('appointments/get_appointments_customer/',
      {
      params: {
        beginweek: beginweek,
        endweek: endweek
      }}
      ).then(res => {
        this.events = []
        res.data.forEach(times => {
            this.events.push({
            name: times.taken ? "Bezet" : "Vrij",
            start: times.start,
            end: times.end,
            color: times.taken ? this.eventColor[1] : this.eventColor[0],
            timed: true
          })
        });
        if (this.events.length == 0) {
          this.noEvents = true
        }
        this.loaded = true
      }).catch(e => {
        console.log(e)
      })
    },
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

.event-text {
  padding: 5px;
  margin-bottom: 0px !important;
}

.no-events {
  position: absolute;
  z-index: 2;
  margin: auto;
  top: 510px;
  left: 480px;
}
</style>
