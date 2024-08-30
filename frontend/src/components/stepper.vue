<script setup>
const props = defineProps({
  stages: Array,
  currentStage: Number,
});

</script>

<style scoped>
.step {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
}
.step-index {
  border: 1px solid var(--pico-primary);
  border-radius: 50%;
  width: 25px;
  height: 25px;
  display: inline-flex;
  justify-content: center;
  align-items: center;
}

ul {
  display: flex;
  justify-content: space-between;
  padding-left: 0;
}

</style>

<template>
  <ul>
    <li class="step" v-for="stage, index in stages">
      <span class="step-index">{{index + 1}}</span><span class="step-stage">{{stage}}</span>
    </li>
  </ul>
  <progress :value="currentStage" :max="stages.length - 1"></progress>
</template>
