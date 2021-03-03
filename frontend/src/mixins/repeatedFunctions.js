// define a mixin object
export default {
  methods: {
    dateToString(datum) {
      const days = [
        "zondag",
        "maandag",
        "dinsdag",
        "woensdag",
        "donderdag",
        "vrijdag",
        "zaterdag"
      ];
      const months = [
        "januari",
        "februari",
        "maart",
        "april",
        "mei",
        "juni",
        "juli",
        "augustus",
        "september",
        "oktober",
        "november",
        "december"
      ];
      const reserverings_tijd = new Date(datum);

      const dayIndex = reserverings_tijd.getDay();
      const day = days[dayIndex];
      const date = reserverings_tijd.getDate();
      const monthIndex = reserverings_tijd.getMonth();
      const month = months[monthIndex];
      const hours = reserverings_tijd.getHours();
      const minutes = String(reserverings_tijd.getMinutes()).padStart(2, '0');

      return `${day} ${date} ${month} om ${hours}:${minutes}`;
    },
    parseDate(inputVar) {
      // parse date time to dd/mm/yyy, h:m:s
      const year = new Date(inputVar).getFullYear();
      const day = String(new Date(inputVar).getDate()).padStart(2, '0');
      const month = String(new Date(inputVar).getMonth()).padStart(2, '0');
      const hours = String(new Date(inputVar).getHours()).padStart(2, '0');
      const minutes = String(new Date(inputVar).getMinutes()).padStart(2, '0');
      const seconds = String(new Date(inputVar).getSeconds()).padStart(2, '0');


      return `${day}/${month}/${year}, ${hours}:${minutes}:${seconds}`;
    },
    logVariable(variable) {
      console.log(variable);
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
    getEventColor(event) {
      return event.color;
    }
  }
};
