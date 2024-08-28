<script setup>
import { ref } from 'vue';
import axios from 'axios';

const props = defineProps({
  cause: String,
})

const allConcerns = ref([])
const selectedConcerns = ref([]);
const ready = ref(false);

axios.get(`/api/causes/${props.cause}/concerns`).then((res) => {
  allConcerns.value = res.data.concerns;
  ready.value = true;
});

function selectConcern(concern) {
  const index = selectedConcerns.value.indexOf(concern);
  if (index < 0) {
    selectedConcerns.value.push(concern)
  } else {
    selectedConcerns.value.splice(index, 1);
  }
}

</script>

<style scoped>
</style>

<template>
  <div v-if="!ready">
    Loading...
  </div>
  <div v-else>
    <h3>Select up to 3 concerns</h3>
    {{ selectedConcerns }}
    <div
      class="card concern-card clickable"
      @click="selectConcern(concern.key)"
      v-for="concern in allConcerns">
      <header class="card-header">
        <p class="card-header-title">{{ concern.name }}</p>
      </header>
    </div>
    <button class="button" @click="$emit('concern', selectedConcerns)">Submit</button>
  </div>
</template>
