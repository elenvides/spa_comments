<template>
  <form @submit.prevent="login">
    <div>
      <label for="username">Email:</label>
      <input v-model="email" id="email" name="email" type="email">
    </div>
    <div>
      <label for="password">Password:</label>
      <input v-model="password" id="password" name="password" type="password">
    </div>
    <button type="submit">Login</button>
  </form>
  <div v-if="message">
    {{ message }}
  </div>
  <div v-if="Object.keys(errors).length">
    <ul>
      <li v-for="(error, key) in errors" :key="key">
        {{ key }}: {{ Array.isArray(error) ? error.join(', ') : error }}
      </li>
    </ul>
  </div>
  <button class="button-secondary" @click="goToRegister">Back to Register</button>
</template>

<script>
export default {
  name: 'LoginComponent',
  data() {
    return {
      email: '',
      password: '',
      message: '',
      errors: {},
    };
  },
  methods: {
    async login() {
      try {
        const API_BASE_URL = process.env.VUE_APP_API_BASE_URL;
        const response = await fetch(`${API_BASE_URL}users/login/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            email: this.email,
            password: this.password,
          }),
        });
        if (response.ok) {
          const userData = await response.json();
          this.message = 'User logged in successfully';
          this.errors = {};


          this.$emit('loginSuccess');
          localStorage.setItem('username', userData.username);
          localStorage.setItem('user_id', userData.user_id);
        } else {
          this.errors = await response.json();
          this.message = null;
        }
      } catch (error) {
        console.error('An unexpected error happened:', error);
      }
    },
    goToRegister() {
      this.$emit('close');
    },
  },
};
</script>
