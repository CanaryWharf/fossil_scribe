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

function getClass(concernKey) {
  if (selectedConcerns.value.indexOf(concernKey) < 0) {
    return 'unselected';
  }
  return 'selected';
};

</script>

<style scoped>
.concern-card-container {
  padding-left: 0;
  display: grid;
  gap: 1rem;
}

@media (min-width: 768px) {
  .concern-card-container {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .concern-card-container {
    grid-template-columns: repeat(3, 1fr);
  }
}

.concern-card-container li {
  list-style: none;
  border: 1px solid var(--pico-primary);
  border-radius: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.concern-card-container .unselected:hover {
  background-color: var(--pico-muted-border-color);
}

.selected, .selectd:hover {
  background-color: var(--pico-text-selection-color);
}

.concern-card-container li p {
  margin-bottom: 3px;
  margin-top: 3px;
  padding: 5px;
  width: 250px;
  text-align: center;
}
</style>

<template>
  <div v-if="!ready">
    Loading...
  </div>
  <article v-else>
    <h3>Select top concerns</h3>
    <ul class="concern-card-container">
      <li
          class="concern-card clickable"
          :class="getClass(concern.key)"
          @click="selectConcern(concern.key)"
          v-for="concern in allConcerns">
        <p>{{ concern.name }}</p>
      </li>
    </ul>
    <button @click="$emit('concern', selectedConcerns)">Submit</button>
  </article>
</template>
