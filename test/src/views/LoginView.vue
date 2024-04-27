<script>
import router from '@/router';

export default {
  data() {
    return {
      username: '',
      password: '',
    };
  },
  methods: {
    async loginUser() {
      try {
        const response = await fetch('http://127.0.0.1:8000/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ username: this.username, password: this.password }),
        });
        const data = await response.json();
        if (data) {
          localStorage.setItem('access_token', data.access_token);
          router.push('/welcome');
        }

      } catch (error) {
        console.error('Login failed:', error);
        // Handle login error (e.g., display error message)
      }
    },
  },
};
</script>

<template>
  <div>
    <h1>Login</h1>
    <form @submit.prevent="login">
      <label for="username">Username</label>
      <input type="text" id="username" name="email" v-model="username" />
      <label for="password">Password</label>
      <input type="password" id="password" name="password" v-model="password" />
      <button type="submit" @click="loginUser">Login</button>
    </form>
  </div>
</template>
