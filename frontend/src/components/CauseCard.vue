<script setup>
import { ref } from 'vue';
import axios from 'axios';

const allCauses = ref([])
const ready = ref(false);

axios.get('/api/causes').then((res) => {
  console.log("GOT", res);
  allCauses.value = res.data.causes;
  ready.value = true;
});

function emitChosen(cause) {
}

</script>

<style scoped>
.cause-card {
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
      class="card cause-card clickable"
      @click="$emit('cause', cause.name)"
      v-for="cause in allCauses">
      <header class="card-header">
        <p class="card-header-title">{{ cause.title }}</p>
      </header>
      <div class="card-image">
        <figure class="image is-4by3">
          <img src="../assets/plane.png">
        </figure>
      </div>
    </div>
  </div>
</template>
