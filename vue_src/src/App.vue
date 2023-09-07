<style src="./assets/styles.css"></style>

<template>
  <div id="app">
    <div v-if="showRegister">
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

      <!-- Btn: show login -->
      <button class="button-secondary" @click="showLogin = true; showRegister = false">Login</button>

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

    <!-- Login component -->
    <div v-if="showLogin">
      <login-component @loginSuccess="handleLoginSuccess" @close="showLogin = false; showRegister = true" />
    </div>

    <div v-else-if="showHeader">
      <header-bar @logout="handleLogout" />
    </div>
  </div>
</template>

<script>
import LoginComponent from './components/Login.vue';
import HeaderBar from './components/HeaderBar.vue';

export default {
  data() {
    return {
      username: '',
      email: '',
      password1: '',
      password2: '',
      message: '',
      errors: {},
      showLogin: false,
      showRegister: true,
      showHeader: false,
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
    handleLoginSuccess() {
      this.showLogin = false;
      this.showRegister = false;
      this.showHeader = true;
    },
    handleLogout() {
      this.showHeader = false;
    },
  },
  components: {
    LoginComponent,
    HeaderBar,
  },
};
</script>
