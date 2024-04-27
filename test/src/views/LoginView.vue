<script setup>
import router from '@/router';
import { ref, onMounted} from 'vue';
import axios from 'axios';


const userlogin = ref({
  username: '',
  password: '',
});

const login = async () => {
  try {
    const response = await axios.post('http://127.0.0.1:8000/login', userlogin.value, { withCredentials: true });
    const data = await response.data;
    if (data) {
      router.push('/welcome');
    }
  } catch (error) {
    console.error('Failed to login:', error);
  }
}





onMounted(() => {
});


</script>

<template>
  <div>
    <h1>Login</h1>
    <form @submit.prevent="login">
      <label for="username">Username</label>
      <input type="text" id="username" name="email" v-model="userlogin.username" />
      <label for="password">Password</label>
      <input type="password" id="password" name="password" v-model="userlogin.password" />
      <button type="submit" @click="loginUser">Login</button>
    </form>
  </div>
</template>
