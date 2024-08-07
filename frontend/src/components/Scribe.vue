<script setup>
import { ref } from 'vue';
import CauseCard from './CauseCard.vue';
import EmailCard from './EmailCard.vue';

const allPages = ref(['Causes', 'Find your MP', 'Concerns', 'Send email'])

// const currentPage = ref('Causes');
const currentPage = ref('Send email');

const chosenCause = ref(null);

const chosenConcerns = ref([]);

const mpName = ref('');


function updatePage(newPage) {
  currentPage.value = newPage;
}
function nextPage() {
}

function updatecurrentCause(newCause) {
  currentCause.value = newCause;
}

function updateConcerns(newConcerns) {
  chosenConcerns.value = newConcerns;
}

function updateMP(newMP) {
  mpName.value = newMP;
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
    <article class="panel is-primary">
      <p class="panel-heading">Primary</p>
      <p class="panel-tabs">
      <a v-for="page in allPages" :class="{'is-active' : page === currentPage}">{{page}}</a>
      </p>
      <div v-if="currentPage === 'Causes'">
        <CauseCard @cause="updatecurrentCause" />
      </div>
      <div v-if="currentPage === 'Send email'">
        <EmailCard 
           :concerns="['health']"
           cause="airport"
           mp="Jezza"
           name="Root"
        />
      </div>
    </article>

  </section>
</template>
