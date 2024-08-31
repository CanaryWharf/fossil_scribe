<script setup>
import { ref, computed } from 'vue';
import axios from 'axios';
import { marked } from 'marked';

const ready = ref(false);

const currentMessage = ref('')
const subject = ref('');
const recipients = ref([]);
const name = ref('');

const props = defineProps({
  concerns: Array,
  cause: String,
  postcode: String,
})

const signOffs = [
  'Kind Regards',
  'Sincerely',
];

function getFullMessage(msg) {
  const sign = signOffs[Math.floor(Math.random() * signOffs.length)]
  return `${msg}\n\n${sign}`;
}

function startEmail() {
  const { concerns, cause, postcode } = props;
  axios.post('/api/message-gen', {
    concerns,
    cause,
    postcode,
  }).then((res) => {
    currentMessage.value = getFullMessage(res.data.msg);
    subject.value = res.data.subject;
    recipients.value = res.data.recipients;
    ready.value = true;
  });
}
const finalEmail = computed(() => {
  return `${currentMessage.value}\n${name.value}`
});
startEmail();

const mailToLink = computed(() => {
  if (!ready.value) {
    return undefined;
  }
  const toList = recipients.value.map(x => `${x.email}`);
  const to = encodeURIComponent(toList.join(';'))
  const subjectEncoded = encodeURIComponent(subject.value)
  const body = encodeURIComponent(finalEmail.value)
  return `mailto:${to}?subject=${subjectEncoded}&body=${body}`

});

function copyToClipboard() {
  navigator.clipboard.writeText(finalEmail.value).then(() => {
    console.log('Content copied to clipboard');
  },() => {
    console.error('Failed to copy');
  });
}

</script>

<style scoped>
.message-body {
  white-space: pre-wrap;
}
footer form {
  display: flex;
  flex-direction: column;
}
.email-controls {
  display: flex;
  gap: 10px;
}
.email-controls button, .email-controls a{
  width: 100%;
}
</style>

<template>
  <div aria-busy="true" v-if="!ready">
    Loading...
  </div>
  <article v-else>
    <header>
      <p>{{ subject }}</p>
    </header>
    <div class="message-body" v-html="currentMessage"></div>
    <footer>
      <form @submit.prevent>
        <input type="text" name="name" placeholder="Name" v-model="name">
        <div class="email-controls">
          <button @click="copyToClipboard">Copy</button>
          <a role="button" :href="mailToLink" data-tooltip="You will have a chance to make changes in your mail app">Open in Mail</a>
        </div>
      </form>
    </footer>
  </article>
</template>
