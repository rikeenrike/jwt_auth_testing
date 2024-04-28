import { createRouter, createWebHistory } from 'vue-router'
import axios from 'axios';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/welcome',
      name: 'welcome',
      component: () => import('../views/WelcomeView.vue'),
      meta: { requiresAuth: true }, 
    },
    {
      path : '/anotherpage',
      name : 'another page',
      component : () => import('../views/anotherpage.vue'),
      meta: { requiresAuth: true }, 
    }
  ]
})

router.beforeEach(async (to, from, next) => {
  if (to.meta.requiresAuth) {
    try {
      const response = await axios.get('http://127.0.0.1:8000/autheticate', {
        withCredentials: true,
      });
      const data = await response.data;
      if (data) {
        next(); 
      } else {
        next('/'); 
      }
    } catch (error) {
      next('/'); 
    }
  } else {
    next(); 
  }
});

export default router;