<script setup>
const props = defineProps({
  stages: Array,
  currentStage: Number,
  stageNameOverrides: {
    type: Array,
    default: () => [],
  },
});

const emit = defineEmits(['change']);

function updatePage(index) {
  if (index < props.currentStage) {
    emit('change', index);
  }
};

</script>

<style scoped>
.step {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
}
.step-index {
  border: 1px solid var(--pico-contrast-focus);
  border-radius: 50%;
  width: 25px;
  height: 25px;
  display: inline-flex;
  justify-content: center;
  align-items: center;
}

.step-index.current {
  border: 1px solid var(--pico-primary);
}

ul {
  display: flex;
  justify-content: space-between;
  padding-left: 0;
}

</style>

<template>
  <ul>
    <li @click="updatePage(index)" class="step" :class="{ clickable : index < currentStage }" v-for="stage, index in stages">
      <span class="step-index" :class="{ current: currentStage === index }">{{index + 1}}</span><span class="step-stage">{{stageNameOverrides[index] || stage}}</span>
    </li>
  </ul>
  <progress :value="currentStage" :max="stages.length - 1"></progress>
</template>
