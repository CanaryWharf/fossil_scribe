<script setup>
import { ref } from 'vue';
import CauseCard from './CauseCard.vue';
import ConcernCard from './ConcernCard.vue';
import EmailCard from './EmailCard.vue';
import Stepper from './stepper.vue';

const allPages = ref(['Causes', 'Concerns', 'Finalise'])

const currentPage = ref(0);

const currentCause = ref(null);

const currentConcerns = ref([]);


function reset() {
  currentPage.value = 0;
  currentCause.value = null;
  currentConcerns.value = []
}

function updatePage(newPage) {
  currentPage.value = newPage;
}
function nextPage() {
  if (currentPage.value < allPages.value.length) {
   currentPage.value += 1
  }
}

function updatecurrentCause(newCause) {
  currentCause.value = newCause;
  nextPage();
}

function updateConcerns(newConcerns) {
  currentConcerns.value = newConcerns;
  nextPage();
}

</script>

<style scoped>
.title {
  text-align: center;
}
</style>

<template>
  <header class="container">
    <h1 class="title">
      Action Scribe
    </h1>
  </header>
  <body class="container">
    <Stepper :stages="allPages" :current-stage="currentPage"></Stepper>
    <div class="controls">
      <button class="outline" @click="reset">Reset</button>
    </div>
    <hr>
    <div v-if="currentPage === 0">
      <CauseCard @cause="updatecurrentCause" />
    </div>
    <div v-if="currentPage === 1">
      <ConcernCard :cause="currentCause" @concern="updateConcerns" />
    </div>
    <div v-if="currentPage === 2">
      <EmailCard 
         :concerns="currentConcerns"
         :cause="currentCause"
         />
    </div>
  </body>
</template>
