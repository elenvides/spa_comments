<template>
  <div class="header">
    <div class="user-info">
      <span>{{ username }}</span>
      <span>(ID: {{ userId }})</span>
    </div>
    <button @click="logout" class="logout-button">Logout</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      userId: null,
    };
  },
  mounted() {
    this.username = localStorage.getItem('username') || '';
    this.userId = localStorage.getItem('user_id') || null;
  },
  methods: {
    logout() {
      localStorage.removeItem('username');
      localStorage.removeItem('user_id');

      const API_BASE_URL = process.env.VUE_APP_API_BASE_URL;
      fetch(`${API_BASE_URL}users/logout/`, {
        method: 'GET',
      })
        .then((response) => {
          if (response.ok) {
            this.username = '';
            this.userId = null;
          } else {
            console.error('Logout failed');
          }
        })
        .catch((error) => {
          console.error('An unexpected error happened:', error);
        });
    },
  },
};
</script>
