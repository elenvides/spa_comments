<style src="./assets/styles.css"></style>

<template>
  <div id="app">
    <form @submit.prevent="register">
        <div>
          <label for="username">Username:</label>
          <input v-model="username" id="username" name="username">
        </div>
        <div>
          <label for="email">Email:</label>
          <input v-model="email" id="email" name="email">
        </div>
        <div>
          <label for="password1">Password:</label>
          <input v-model="password1" type="password" id="password1" name="password1">
        </div>
        <div>
          <label for="password2">Confirm Password:</label>
          <input v-model="password2" type="password" id="password2" name="password2">
        </div>
        <button type="submit">Register</button>
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
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      email: '',
      password1: '',
      password2: '',
      message: '',
      errors: {},
    };
  },
  methods: {
    async register() {
      try {
        const API_BASE_URL = process.env.VUE_APP_API_BASE_URL;
        const response = await fetch(`${API_BASE_URL}users/register/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username: this.username,
            email: this.email,
            password1: this.password1,
            password2: this.password2,
          }),
        });
        if (response.ok) {
          this.message = 'User registered successfully';
          this.errors = {};
        } else {
          this.errors = await response.json();
          this.message = null;
        }
      } catch (error) {
        console.error('An unexpected error happened:', error);
      }
    },
  },
};
</script>
