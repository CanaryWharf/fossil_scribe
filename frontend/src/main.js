import { createApp } from 'vue'
import { createWebHistory, createRouter } from 'vue-router'
import './style.css';
import './sass.scss';
import App from './App.vue'
import Scribe from './components/Scribe.vue';

const routes = [
  { path: '/', component: Scribe },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
})

const app = createApp(App);
app.use(router);

app.mount('#app')
