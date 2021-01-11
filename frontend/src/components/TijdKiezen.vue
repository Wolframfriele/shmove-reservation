<template>
  <v-row class="fill-height">
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
      <div class='loader' v-if='!appointmentsLoaded'>
        <v-progress-circular
          :size="50"
          color="primary"
          indeterminate
        ></v-progress-circular>
        <p style="color:#895638" class='mt-5'>Vrije plaatsen worden geladen</p>
      </div>
      <v-sheet>
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
            <v-btn v-else-if="present" fab depressed color="primary" :aria-label="dateToString(date)" :href="returnID(weekday)">{{ day }}</v-btn>
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
      </v-sheet>
    </v-col>
  </v-row>
</template>

<script>
import { bus } from '../main'
import axios from "axios";

export default {
  data: () => ({
    focus: "",
    type: "week",
    weekdays: [1, 2, 3, 4, 5, 6, 0],
    firstinterval: "9",
    intervalcount: "11",
    locale: "nl",
    eventColor:  ['primary', 'red'],
    treatment: ["shiatsu"],
    events: [],
    appointmentsLoaded: false,
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
    log(input) {
      console.log(input)
    },
    setToday() {
      this.focus = "";
    },
    prev() {
      this.$refs.calendar.prev();
    },
    next() {
      this.$refs.calendar.next();
    },
    getEventColor (event) {
        return event.color
    },
    updateRange ({ start, end }) {
      this.getFreePlaces(start.date, end.date)
    },
    intervalFormat(interval) {
      return interval.time;
    },
    bevestigAfspraak({ event }) {
      this.$router.push({name: "AfspraakBevestigen", params: {start: event.start, end: event.end, treatment: this.treatment}});
    },
    getFreePlaces(beginweek, endweek){
      let self = this;
      this.events = []
      axios.get(`${self.$store.state.HOST}/api/appointments/get_appointments/`,
      {
      params: {
        beginweek: beginweek,
        endweek: endweek
      }}
      ).then(res => {
        if(res.data){
          self.appointmentsLoaded = true
        }else{
          self.appointmentsLoaded = false
        }
        self.events = []
        res.data.forEach(times => {
          if (times.taken == false) {
            self.events.push({
            name: times.taken ? "Bezet" : "Vrij",
            start: times.start,
            end: times.end,
            color: times.taken ? self.eventColor[1] : self.eventColor[0],
            timed: true
          })
          }
        });
      }).catch(e => {
        console.log(e)
      })
    },
    dateToString: function (input) {
      const days = [
        'zondag',
        'maandag',
        'dinsdag',
        'woensdag',
        'donderdag',
        'vrijdag',
        'zaterdag'
      ];
      const months = [
        'januari',
        'februari',
        'maart',
        'april',
        'mei',
        'juni',
        'juli',
        'augustus',
        'september',
        'oktober',
        'november',
        'december'
      ];
      const datum = new Date(input);

      const dayIndex = datum.getDay();
      const day = days[dayIndex];
      const date = datum.getDate();
      const monthIndex = datum.getMonth();
      const month = months[monthIndex];

      return `${ day } ${ date } ${ month }`;
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
.loader{
  width: 100%;
  height:auto;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  margin-bottom: -50px;
  position: relative;
  top: 45%;
  z-index: 10;
}
</style>
