<script setup>
import { ref } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import Cause from './Cause.vue';

const allCauses = ref([])
const ready = ref(false);
const route = useRoute();
const emit = defineEmits(['cause']);

function handleCauseInQuery() {
  const causeKey = route.query.cause;
  const cause = allCauses.value.find(x => x.key === causeKey);
  if (cause) {
    emit('cause', cause);
  }
};

axios.get('/api/causes').then((res) => {
  allCauses.value = res.data.causes;
  handleCauseInQuery();
  ready.value = true;
});

</script>

<style scoped>
.cause-card-container {
  display: flex;
  flex-wrap: wrap;
  flex-direction: column;
}
</style>

<template>
  <div v-if="!ready" aria-busy="true">
    Loading...
  </div>
  <div class="cause-card-container" v-else>
    <Cause
      class="card cause-card clickable"
      @click="$emit('cause', cause)"
      :name="cause.name"
      :cause-key="cause.key"
      :description="cause.description"
      v-for="cause in allCauses">
    </Cause>
  </div>
</template>
