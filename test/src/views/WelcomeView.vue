<script setup>
import axios from 'axios';
import { ref } from 'vue';
import { onMounted, onUnmounted } from 'vue';
import router from '@/router';

const name = ref('');
const id = ref(0);

let socket;

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

var users = ref([]);
const displayaccounts = async () => {
  console.log('displaying accounts');
  
  try {
    const response = await axios.get('http://127.0.0.1:8000/all/users', {
      withCredentials: true,  
    });
    users.value = await response.data;
    console.log(users);
  } catch (error) {
    console.error('Failed to display accounts:', error);
  }
}

const newUser = ref({
  FirstName: '',
  LastName: '',
  Email: '',
  phone: '',
  password: '',
});

const uploadusers = async () => {
  console.log(newUser.value);
  try {
    const response = await axios.post('http://127.0.0.1:8000/register', newUser.value, {
      withCredentials: true,  
    });
  } catch (error) {
    console.error('Failed to upload users:', error);
  }
}



onMounted(() => {
  socket = new WebSocket('ws://127.0.0.1:8000/ws');

  socket.addEventListener('message', (event) => {
    console.log('Message from server: ', event.data);
    const newUser = JSON.parse(event.data);
    users.value.push(newUser);
  });

  displayaccounts();
  accessname();
});


onUnmounted(() => {
  socket.close();
});
</script>



<template>
  <div>
    <h1>Welcome</h1>
    <p>Welcome to the app!{{ name }}</p>
    <p>your account id is {{ id }}</p>
  </div>
  <div>
    <h2>Accounts</h2>
    <ul>
      <li v-for="user in users" :key="user.accountid">
        {{ user.FirstName }}
      </li>
    </ul>
  </div>
  <div class="input">
    <label for="username">FirstName</label>
    <input type="text" id="username" name="email" v-model="newUser.FirstName" />
    <label for="username">LastName</label>
    <input type="text" id="username" name="email" v-model="newUser.LastName" />
    <label for="username">Email</label>
    <input type="text" id="username" name="email" v-model="newUser.Email" />
    <label for="username">Phone</label>
    <input type="text" id="username" name="email" v-model="newUser.phone" />
    <label for="password">Password</label>
    <input type="password" id="password" name="password" v-model="newUser.password" />
    <button @click="uploadusers">upload</button>
  </div>

  <div>
    <button @click="logout">logout</button>
    <button @click="router.push('/anotherpage')">toanother page</button>
  </div>
</template>

<style>
  .input {
    display: flex;
    flex-direction: column;
  }
</style>
