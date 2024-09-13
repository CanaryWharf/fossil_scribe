<script setup>
import { ref } from 'vue';
import CauseCard from './CauseCard.vue';
import ConcernCard from './ConcernCard.vue';
import EmailCard from './EmailCard.vue';
import RepCard from './RepresentativeCard.vue';
import Stepper from './stepper.vue';

const allPages = ref(['Causes', 'Representatives', 'Concerns', 'Email'])
const stageNameOverrides = ref([]);

const instructions = ref([
  'Select a cause to write about',
  'Find your representative',
  'Select your top concerns',
  'Generate email',
]);

const currentPage = ref(0);

const currentCause = ref(null);

const currentConcerns = ref([]);

const currentPostcode = ref(null);


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

function truncate(str, n=10) {
  return (str.length > n) ? str.slice(0, n-1) + '...' : str;
}

function updateCurrentStageName(name, index) {
  stageNameOverrides.value[index] = truncate(name);
}

function updatecurrentCause(newCause) {
  currentCause.value = newCause;
  updateCurrentStageName(newCause.name, currentPage.value);
  nextPage();
}

function updateConcerns(newConcerns) {
  currentConcerns.value = newConcerns;
  nextPage();
}

function updatePostcode(postcode, repName) {
  currentPostcode.value = postcode;
  updateCurrentStageName(repName, currentPage.value);
  nextPage();
}
</script>

<style scoped>
.title {
  margin-top: 0.5rem;
}
.controls button {
  margin-right: 1rem;
}
header {
  text-align: center;
}
.tag {
  font-size: x-small;
}
</style>

<template>
  <header class="container">
    <h1 class="title">
      Action Scribe
      <span class="tag">Beta</span>
    </h1>
    <h2>Write to your representatives the easy way</h2>
  </header>
  <body class="container">
    <Stepper :stages="allPages" @change="updatePage" :current-stage="currentPage" :stage-name-overrides="stageNameOverrides"></Stepper>
    <div class="controls">
      <button class="outline" @click="reset">Reset</button>
      <span class="instructions">Step {{ currentPage + 1 }}: {{instructions[currentPage]}}</span>
    </div>
    <hr>
    <div v-if="currentPage === 0">
      <CauseCard @cause="updatecurrentCause" />
    </div>
    <div v-if="currentPage === 1">
      <RepCard :cause="currentCause" @chosen="updatePostcode" />
    </div>
    <div v-if="currentPage === 2">
      <ConcernCard :cause="currentCause.key" @concern="updateConcerns" />
    </div>
    <div v-if="currentPage === 3">
      <EmailCard 
         :concerns="currentConcerns"
         :cause="currentCause.key"
         :postcode="currentPostcode"
         />
    </div>
  </body>
</template>
