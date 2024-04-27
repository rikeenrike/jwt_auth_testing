<script setup>
import axios from 'axios';
import { ref } from 'vue';
import { onMounted } from 'vue';
import router from '@/router';

const name = ref('');
const id = ref(0);

const accessname = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/users/me', {
      withCredentials: true,  
    });
    const data = await response.data;
    if (data) {
      console.log(data);
      name.value = data.username;
      id.value = data.accountid;
    }
  } catch (error) {
    console.error('Failed to access name:', error);
    router.push('/');
  }
}

const logout = async () => {
  try {
    const response = await axios.post('http://127.0.0.1:8000/logout', {
      withCredentials: true,  
    });
    if (response.status === 200) {
      router.push('/');
    }
  } catch (error) {
    console.error('Failed to logout:', error);
  }
}

onMounted(() => {
  accessname();
});
</script>



<template>
  <div>
    <h1>Welcome</h1>
    <p>Welcome to the app!{{ name }}</p>
    <p>your account id is {{ id }}</p>
  </div>
  <div>
    <button @click="logout">logout</button>
  </div>
</template>

<style>

</style>
