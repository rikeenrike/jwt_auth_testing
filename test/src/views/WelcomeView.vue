<script setup>
import axios from 'axios';
import { ref } from 'vue';
import { onMounted } from 'vue';
import router from '@/router';

const name = ref('');

const accessname = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/users/me', {
      withCredentials: true,  
    });
    const data = await response.data;
    if (data) {
      console.log(data);
      name.value = data.username;
    }
  } catch (error) {
    console.error('Failed to access name:', error);
    router.push('/');
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
  </div>
</template>

<style>

</style>
