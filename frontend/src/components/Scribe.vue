<script setup>
import { ref } from 'vue';
import CauseCard from './CauseCard.vue';
import ConcernCard from './ConcernCard.vue';
import EmailCard from './EmailCard.vue';

const allPages = ref(['Causes', 'Concerns', 'Send email'])

const currentPage = ref(0);
// const currentPage = ref('Send email');

const currentCause = ref(null);

const currentConcerns = ref([]);

const mpName = ref('');


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
      <a 
        v-for="page, i in allPages"
        @click="() => updatePage(i)"
        :class="{'is-active' : i === currentPage}"
        >{{page}}</a>
      </p>
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
           mp="Jezza"
           name="Ya Boi"
        />
      </div>
    </article>

  </section>
</template>
