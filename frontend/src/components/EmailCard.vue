<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { marked } from 'marked';

const ready = ref(false);

const currentMessage = ref('')

const props = defineProps({
  concerns: Array,
  cause: String,
  mp: String,
  name:  String,
})

function startEmail() {
  const { concerns, cause, mp, name } = props;
  axios.post('/api/message-gen', {
    concerns,
    cause,
    mp,
    name,
  }).then((res) => {
    currentMessage.value = res.data.msg;
    ready.value = true;
  });
}
startEmail();

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
    <!-- <button class="button" @click="startEmail">Send Mail</button> -->
  </div>
</template>
