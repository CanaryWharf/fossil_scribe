<script setup>
import { ref } from 'vue';
import CauseCard from './CauseCard.vue';
import ConcernCard from './ConcernCard.vue';
import EmailCard from './EmailCard.vue';
import RepCard from './RepresentativeCard.vue';
import Stepper from './stepper.vue';

const allPages = ref(['Causes', 'Representatives', 'Concerns', 'Email'])

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

function updatecurrentCause(newCause) {
  currentCause.value = newCause;
  nextPage();
}

function updateConcerns(newConcerns) {
  currentConcerns.value = newConcerns;
  nextPage();
}

function updatePostcode(postcode) {
  currentPostcode.value = postcode;
  nextPage();
}
</script>

<style scoped>
.title {
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
    <Stepper :stages="allPages" :current-stage="currentPage"></Stepper>
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
