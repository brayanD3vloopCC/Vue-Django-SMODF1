<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <img src="@/assets/smodlogotype.jpg" alt="SMOD Logo" class="login-logo" />
        <h2 class="login-title">Iniciar Sesión</h2>
        <p class="login-subtitle">Bienvenido a SMOD F1</p>
      </div>

      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="correo">Correo Electrónico</label>
          <div class="input-group">
            <i class="fas fa-envelope"></i>
            <input
              type="email"
              id="correo"
              v-model="correo"
              placeholder="tucorreo@correo.com"
              required
            />
          </div>
        </div>

        <div class="form-group">
          <label for="password">Contraseña</label>
          <div class="input-group">
            <i class="fas fa-lock"></i>
            <input
              :type="showPassword ? 'text' : 'password'"
              id="password"
              v-model="password"
              placeholder="••••••••"
              required
            />
            <i 
              class="fas"
              :class="showPassword ? 'fa-eye-slash' : 'fa-eye'"
              @click="togglePassword"
            ></i>
          </div>
        </div>

        <div class="form-options">
          <label class="remember-me">
            <input type="checkbox" v-model="rememberMe" />
            <span>Recordarme</span>
          </label>
          <a href="#" class="forgot-password">¿Olvidaste tu contraseña?</a>
        </div>

        <button type="submit" class="login-button" :disabled="loading">
          <span v-if="!loading">Iniciar Sesión</span>
          <i v-else class="fas fa-spinner fa-spin"></i>
        </button>

        <div class="login-divider">
          <span>o</span>
        </div>
        

        <p class="register-link">
          ¿No tienes una cuenta? 
          <router-link to="/register">Regístrate aquí</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script>
import api from '@/plugins/axios'
export default {
  name: 'LoginView',
  data() {
    return {
      correo: '',
      password: '',
      rememberMe: false,
      showPassword: false,
      loading: false
    }
  },
  methods: {
    togglePassword() {
      this.showPassword = !this.showPassword
    },
    async handleLogin() {
      this.loading = true
      try {
        const response = await api.post('login/', {
          correo: this.correo,
          password: this.password
        })
        localStorage.setItem('usuario_smodf1', JSON.stringify(response.data))
        this.$router.push('/sistema')
      } catch (error) {
        alert('Error de login: ' + (error.response?.data?.error || error.message))
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>


.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #101010 0%, #1a2a3a 100%);
  padding: 20px;
  margin-top: -70px;
}

.login-card {
  background: #181c22;
  border-radius: 24px;
  padding: 40px;
  width: 100%;
  max-width: 480px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  border: 1px solid #2a3a4a;
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.login-logo {
  width: 80px;
  height: 80px;
  margin-bottom: 16px;
  border-radius: 12px;
}

.login-title {
  color: #fff;
  font-size: 2rem;
  margin-bottom: 8px;
  font-family: 'VT323', monospace;
}

.login-subtitle {
  color: #a3c9e2;
  font-size: 1.1rem;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  color: #fff;
  font-size: 0.9rem;
}

.input-group {
  position: relative;
  display: flex;
  align-items: center;
}

.input-group i {
  position: absolute;
  left: 16px;
  color: #a3c9e2;
}

.input-group input {
  width: 100%;
  padding: 12px 16px 12px 48px;
  background: #222c38;
  border: 1px solid #2a3a4a;
  border-radius: 12px;
  color: #fff;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.input-group input:focus {
  outline: none;
  border-color: #a3c9e2;
  box-shadow: 0 0 0 2px rgba(163, 201, 226, 0.2);
}

.input-group i:last-child {
  left: auto;
  right: 16px;
  cursor: pointer;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.9rem;
}

.remember-me {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #fff;
  cursor: pointer;
}

.remember-me input {
  width: 16px;
  height: 16px;
  accent-color: #a3c9e2;
}

.forgot-password {
  color: #a3c9e2;
  text-decoration: none;
  transition: color 0.3s ease;
}

.forgot-password:hover {
  color: #fff;
}

.login-button {
  background: #a3c9e2;
  color: #101010;
  border: none;
  padding: 12px;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.login-button:hover {
  background: #8ab7d8;
  transform: translateY(-2px);
}

.login-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.login-divider {
  display: flex;
  align-items: center;
  text-align: center;
  color: #a3c9e2;
  margin: 16px 0;
}

.login-divider::before,
.login-divider::after {
  content: '';
  flex: 1;
  border-bottom: 1px solid #2a3a4a;
}

.login-divider span {
  padding: 0 16px;
}

.social-login {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.social-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 12px;
  border-radius: 12px;
  border: 1px solid #2a3a4a;
  background: #222c38;
  color: #fff;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.social-button:hover {
  background: #2a3a4a;
  transform: translateY(-2px);
}

.social-button i {
  font-size: 1.2rem;
}

.social-button.google i {
  color: #ea4335;
}

.social-button.github i {
  color: #fff;
}

.register-link {
  text-align: center;
  color: #a3c9e2;
  font-size: 0.9rem;
}

.register-link a {
  color: #fff;
  text-decoration: none;
  font-weight: bold;
  transition: color 0.3s ease;
}

.register-link a:hover {
  color: #a3c9e2;
}

@media (max-width: 480px) {
  .login-card {
    padding: 32px 24px;
  }
  
  .login-title {
    font-size: 1.8rem;
  }
  
  .social-button {
    font-size: 0.9rem;
  }
}
</style> 