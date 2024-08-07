<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { io } from "socket.io-client"
import { marked } from 'marked';

const ready = ref(true);

const currentMessage = ref('')

const props = defineProps({
  concerns: Array,
  cause: String,
  mp: String,
  name:  String,
})

const socket = io("/socket")

socket.on("connect", () => {
  console.log("we in");
})
socket.on("token", (msg) => {
  console.log(msg);
  currentMessage.value = marked(msg)
});

function startEmail() {
  socket.emit("message", JSON.stringify({
    concerns: props.concerns,
    cause: props.cause,
    mp: props.mp,
    name: props.name,
  }));
}

</script>

<style scoped>
</style>

<template>
  <div v-if="!ready">
    Loading...
  </div>
  <div v-else>
    <div class="message">
      <div class="message-header">
        <p>Letter to {{ props.mp }}</p>
      </div>
      <div class="message-body" v-html="currentMessage">
      </div>
    </div>
    <button class="button" @click="startEmail">Send Mail</button>
  </div>
</template>
