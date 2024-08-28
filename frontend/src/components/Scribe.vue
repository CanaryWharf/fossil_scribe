<script setup>
import { ref } from 'vue';
import CauseCard from './CauseCard.vue';
import ConcernCard from './ConcernCard.vue';
import EmailCard from './EmailCard.vue';

const allPages = ref(['Causes', 'Concerns', 'Send email'])

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
  console.log("Updating cause")
  currentCause.value = newCause;
  nextPage();
}

function updateConcerns(newConcerns) {
  currentConcerns.value = newConcerns;
  nextPage();
}

</script>

<template>
  <section class="section">
    <div class="container has-text-centered">
      <h1 class="title">
        Fossil Scribe
      </h1>
    </div>
  </section>
  <section class="section">
    <button class="button" @click="reset">Reset</button>
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
         name="Ya Boi"
         />
    </div>

  </section>
</template>
