<script setup>
import { ref } from 'vue';
import axios from 'axios';
import Cause from './Cause.vue';

const allCauses = ref([])
const ready = ref(false);

axios.get('/api/causes').then((res) => {
  allCauses.value = res.data.causes;
  ready.value = true;
});

</script>

<style scoped>
</style>

<template>
  <div v-if="!ready">
    Loading...
  </div>
  <div v-else>
    <Cause
      class="card cause-card clickable"
      @click="$emit('cause', cause.key)"
      :name="cause.name"
      :cause-key="cause.key"
      :description="cause.description"
      v-for="cause in allCauses">
    </Cause>
  </div>
</template>
