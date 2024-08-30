<script setup>
import { computed } from 'vue';

const props = defineProps({
  name: {
    type: String,
    required: true,
  },
  causeKey: {
    type: String,
    required: true,
  },
  description: String,
});

function getImageUrl(filename) {
  return new URL(`../assets/${filename}.png`, import.meta.url).href;
}

</script>

<style scoped>
.cause-body {
  display: flex;
}
.cause-body img {
  max-width: 200px;
  max-height: 200px;
  border-radius: 20px;
  margin-right: 10px;
}
.cause-card {
}
</style>

<template>
  <article class="cause-card clickable">
    <header>{{ name }}</header>
    <div class="cause-body">
      <img :src="getImageUrl(causeKey)">
      <div class="card-content">{{ description }}</div>
    </div>
  </article>
</template>
