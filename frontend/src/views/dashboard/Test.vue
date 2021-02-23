<template>
  <v-container>
    <h1>Test</h1>
    <v-radio-group 
      v-model="select" 
      @change="logVar(select)"
      >
      <v-radio
        label="Test 1"
        value="testvalue1">
      </v-radio>
      <v-radio
        label="Test 2"
        value="testvalue2">
      </v-radio>
    </v-radio-group>
    <v-btn @click="openModal">
      Open Modal
    </v-btn>
    <v-dialog
      v-model="modal"
      width="500"
      height="250"
      hide-overlay
      offset-x
      >
      <TestModal />
    </v-dialog>
  </v-container>
</template>

<script>
import TestModal from "../../components/dashboard/TestModal";

export default {
  data () {
      return {
        inputSelect: "testvalue1",
        select: "",
        modal: false,
      }
  },
  components: {
    TestModal,
  },
  methods: {
    logVar(variable) {
      console.log(variable)
    },
    openModal() {
      this.modal = true
    }
  },
  mounted () {
    this.select = this.inputSelect
  }
}
</script>

<style scoped>

</style>