<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { marked } from 'marked';
import { computed } from 'vue';

const ready = ref(false);

const currentMessage = ref('')
const recipients = ref([]);

const props = defineProps({
  concerns: Array,
  cause: String,
  name:  String,
})

function getFullMessage(msg) {
  return `${msg}\n\nKind Regards\n${props.name}`;
}

function startEmail() {
  const { concerns, cause, name } = props;
  axios.post('/api/message-gen', {
    concerns,
    cause,
  }).then((res) => {
    currentMessage.value = getFullMessage(res.data.msg);
    recipients.value = res.data.recipients;
    ready.value = true;
  });
}
startEmail();

const mailToLink = computed(() => {
  if (!ready.value) {
    return undefined;
  }
  const toList = recipients.value.map(x => `${x.name} <${x.email}>`);
  const to = encodeURIComponent(toList.join(';'))
  const subject = encodeURIComponent('Some subject')
  const body = encodeURIComponent(currentMessage.value)
  return `mailto:${to}?subject=${subject}&body=${body}`

});
</script>

<style scoped>
.message-body {
  white-space: pre-wrap;
}
</style>

<template>
  <div v-if="!ready">
    Loading...
  </div>
  <div v-else>
    <div class="message">
      <div class="message-header">
        <p>Email</p>
      </div>
      <div class="message-body" v-html="currentMessage">
      </div>
    </div>
    <!-- <button class="button" @click="startEmail">Send Mail</button> -->
    <a class="button" :href="mailToLink">Send Mail</a>
  </div>
</template>
