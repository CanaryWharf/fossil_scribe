<script setup>
import { ref, computed, toRaw } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

const props = defineProps({
  cause: Object,
});
const reps = ref([]);
const loading = ref(false);
const postcode = ref('');
const route = useRoute();

const emit = defineEmits(['chosen']);


const postcodeRegex = /([Gg][Ii][Rr] 0[Aa]{2})|((([A-Za-z][0-9]{1,2})|(([A-Za-z][A-Ha-hJ-Yj-y][0-9]{1,2})|(([A-Za-z][0-9][A-Za-z])|([A-Za-z][A-Ha-hJ-Yj-y][0-9][A-Za-z]?))))\s?[0-9][A-Za-z]{2})/

function isValidPostCode(code) {
  const regex = new RegExp(postcodeRegex);
  return regex.test(code);
}

const validPostcode = computed(() => {
  return isValidPostCode(postcode.value);
});

const disableSearch = computed(() => {
  return loading.value || !validPostcode.value;
});

const lookupRecipients = computed(() => {
  return Boolean(props.cause.recipients_lookup)
});

function getPartyStyle(partyProxy) {
  const party = toRaw(partyProxy);
  if (!party) {
    return {}
  }
  return {
    'background-color': '#' + party.backgroundColour,
    color: '#' + party.foregroundColour,
  }
}


function handleRepInQuery() {
  const postcodeFromRoute = route.query.postcode;
  if (isValidPostCode(postcodeFromRoute)) {
    getRepresentative().then(() => {
      emit('chosen', postcodeFromRoute, reps.value[0]?.name);
    });
  }
};

const getRepresentative = () => {
  loading.value = true;
  return axios.get(`/api/causes/${props.cause.key}/recipients?post_code=${postcode.value}`).then((res) => {
    reps.value = res.data.recipients;
  }).then(() => {
    loading.value = false;
  });
};

const recipientsFound = ref(false);

if (!lookupRecipients.value) {
  reps.value = props.cause.recipients;
  emit('chosen', undefined, props.cause.recipients[0]?.name);
};

const disableNext = computed(() => {
  return !reps.value.length;
});

// handleRepInQuery();

</script>

<style scoped>
.rep-details {
  display: flex;
  gap: 10px;
  justify-content: space-between;
}

.rep-right {
  display: flex;
  flex-direction: column;
  font-style: italic;
}
.rep-left {
  display: flex;
  flex-direction: column;
}

.rep-party {
  text-align: right;
  padding-right: 0.5rem;
}

.rep-details img {
  max-width: 10rem;
}
.rep-name {
  font-size: xx-large;
}
.rep-constituency {
  font-style: italic;
}
</style>

<template>
  <article>
    <template  v-if="lookupRecipients">
    <form @submit.prevent>
      <input v-model="postcode" placeholder="Post code">
      <button :disabled="disableSearch"@click="getRepresentative">Search</button>
    </form>
    <hr>
    </template>
    <div class="rep-details" :aria-busy="loading" v-for="rep in reps">
      <div class="rep-left">
        <span class="rep-name">{{rep.name}}</span>
        <span class="rep-constituency">{{ rep.constituency?.name }}</span>
      </div>
      <div class="rep-right">
        <img :src="rep.avatar">
        <span :style="getPartyStyle(rep.party)" class="rep-party">{{ rep.party?.name }}</span>
      </div>
    </div>
    <footer>
      <button :disabled="disableNext" @click="$emit('chosen', postcode, reps[0]?.name)">Next</button>
    </footer>
  </article>
</template>
