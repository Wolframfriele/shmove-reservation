// define a mixin object
export default {
  methods: {
    dateToString (datum) {
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
      const reserverings_tijd = new Date(datum);

      const dayIndex = reserverings_tijd.getDay();
      const day = days[dayIndex];
      const date = reserverings_tijd.getDate();
      const monthIndex = reserverings_tijd.getMonth();
      const month = months[monthIndex];
      const hours = reserverings_tijd.getHours();
      const minutes = reserverings_tijd.getMinutes().toLocaleString('en-US', {minimumIntegerDigits: 2, useGrouping:false});

      return `${ day } ${ date } ${ month } om ${ hours }:${ minutes }`;
    },
    parseDate(date){
      // parse date time to dd/mm/yyy, h:m:s
      return new Date(date).toLocaleString('en-GB', { timeZone: 'CET' });
    },
    logVariable(variable) {
      console.log(variable)
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
  }
}