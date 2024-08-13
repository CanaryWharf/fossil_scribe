<script setup>
import { ref } from 'vue';
import axios from 'axios';

const props = defineProps({
  cause: String,
})

const allConcerns = ref([])
const ready = ref(false);

axios.get(`/api/causes/${props.cause}/concerns`).then((res) => {
  allConcerns.value = res.data.concerns;
  ready.value = true;
});

</script>

<style scoped>
.concern-card {
  width: 20em;
  margin: 1em;
}
</style>

<template>
  <div v-if="!ready">
    Loading...
  </div>
  <div v-else>
    <div
      class="card concern-card clickable"
      @click="$emit('concern', [concern.key])"
      v-for="concern in allConcerns">
      <header class="card-header">
        <p class="card-header-title">{{ concern.name }}</p>
      </header>
    </div>
  </div>
</template>
