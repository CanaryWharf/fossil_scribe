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

<template>
  <div class="card clickable">
    <header class="card-header">
        <p class="card-header-title">{{ name }}</p>
      </header>
      <div class="card-image">
        <figure class="image is-4by3">
          <img :src="getImageUrl(causeKey)">
        </figure>
      </div>
      <div class="card-content">{{ description }}</div>
  </div>
</template>
