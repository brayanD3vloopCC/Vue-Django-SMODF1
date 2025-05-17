<template>
  <div class="register-container">
    <div class="register-card">
      <div class="register-header">
        <img src="@/assets/smodlogotype.jpg" alt="SMOD Logo" class="register-logo" />
        <h2 class="register-title">Crear Cuenta</h2>
        <p class="register-subtitle">Únete a SMOD F1</p>
      </div>

      <form @submit.prevent="handleRegister" class="register-form">
        <div class="form-group">
          <label for="nickname">Usuario (nickname)</label>
          <div class="input-group">
            <i class="fas fa-user"></i>
            <input
              type="text"
              id="nickname"
              v-model="nickname"
              placeholder="Tu usuario"
              required
            />
          </div>
        </div>

        <div class="form-group">
          <label for="nombre_completo">Nombre Completo</label>
          <div class="input-group">
            <i class="fas fa-id-card"></i>
            <input
              type="text"
              id="nombre_completo"
              v-model="nombre_completo"
              placeholder="Tu nombre completo"
              required
            />
          </div>
        </div>

        <div class="form-group">
          <label for="email">Correo Electrónico</label>
          <div class="input-group">
            <i class="fas fa-envelope"></i>
            <input
              type="email"
              id="email"
              v-model="email"
              placeholder="tu@email.com"
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
          <p class="password-requirements">
            La contraseña debe tener al menos 8 caracteres, incluir mayúsculas, minúsculas y números
          </p>
        </div>

        <div class="form-group">
          <label for="confirmPassword">Confirmar Contraseña</label>
          <div class="input-group">
            <i class="fas fa-lock"></i>
            <input
              :type="showConfirmPassword ? 'text' : 'password'"
              id="confirmPassword"
              v-model="confirmPassword"
              placeholder="••••••••"
              required
            />
            <i 
              class="fas"
              :class="showConfirmPassword ? 'fa-eye-slash' : 'fa-eye'"
              @click="toggleConfirmPassword"
            ></i>
          </div>
        </div>

        <div class="form-group">
          <label class="terms-checkbox">
            <input type="checkbox" v-model="acceptTerms" required />
            <span>Acepto los <a href="#">términos y condiciones</a> y la <a href="#">política de privacidad</a></span>
          </label>
        </div>

        <button type="submit" class="register-button" :disabled="loading">
          <span v-if="!loading">Crear Cuenta</span>
          <i v-else class="fas fa-spinner fa-spin"></i>
        </button>

        <div class="register-divider">
          <span>o</span>
        </div>


        <p class="login-link">
          ¿Ya tienes una cuenta? 
          <router-link to="/login">Inicia sesión aquí</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script>
import api from '@/plugins/axios'

export default {
  name: 'RegisterView',
  data() {
    return {
      nickname: '',
      nombre_completo: '',
      email: '',
      password: '',
      confirmPassword: '',
      acceptTerms: false,
      showPassword: false,
      showConfirmPassword: false,
      loading: false
    }
  },
  methods: {
    togglePassword() {
      this.showPassword = !this.showPassword
    },
    toggleConfirmPassword() {
      this.showConfirmPassword = !this.showConfirmPassword
    },
    async handleRegister() {
      if (this.password !== this.confirmPassword) {
        alert('Las contraseñas no coinciden')
        return
      }
      this.loading = true
      try {
        await api.post('registro/', {
          nickname: this.nickname,
          nombre_completo: this.nombre_completo,
          email: this.email,
          password: this.password,
          password2: this.confirmPassword
        })
        this.$router.push('/login')
      } catch (error) {
        alert('Error al registrar: ' + (error.response?.data?.email || error.message))
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  min-width: 100vw;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #101010 0%, #1a2a3a 100%);
  margin: -70px;
  padding: 0;
}

.register-card {
  background: #181c22;
  border-radius: 24px;
  padding: 40px;
  width: 100%;
  max-width: 480px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  border: 1px solid #2a3a4a;
}

.register-header {
  text-align: center;
  margin-bottom: 32px;
}

.register-logo {
  width: 80px;
  height: 80px;
  margin-bottom: 16px;
  border-radius: 12px;
}

.register-title {
  color: #fff;
  font-size: 2rem;
  margin-bottom: 8px;
  font-family: 'VT323', monospace;
}

.register-subtitle {
  color: #a3c9e2;
  font-size: 1.1rem;
}

.register-form {
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

.password-requirements {
  color: #a3c9e2;
  font-size: 0.8rem;
  margin-top: 4px;
}

.terms-checkbox {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  color: #fff;
  font-size: 0.9rem;
  cursor: pointer;
}

.terms-checkbox input {
  margin-top: 4px;
  accent-color: #a3c9e2;
}

.terms-checkbox a {
  color: #a3c9e2;
  text-decoration: none;
  transition: color 0.3s ease;
}

.terms-checkbox a:hover {
  color: #fff;
}

.register-button {
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

.register-button:hover {
  background: #8ab7d8;
  transform: translateY(-2px);
}

.register-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.register-divider {
  display: flex;
  align-items: center;
  text-align: center;
  color: #a3c9e2;
  margin: 16px 0;
}

.register-divider::before,
.register-divider::after {
  content: '';
  flex: 1;
  border-bottom: 1px solid #2a3a4a;
}

.register-divider span {
  padding: 0 16px;
}

.social-register {
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

.login-link {
  text-align: center;
  color: #a3c9e2;
  font-size: 0.9rem;
}

.login-link a {
  color: #fff;
  text-decoration: none;
  font-weight: bold;
  transition: color 0.3s ease;
}

.login-link a:hover {
  color: #a3c9e2;
}

@media (max-width: 480px) {
  .register-card {
    padding: 32px 24px;
  }
  
  .register-title {
    font-size: 1.8rem;
  }
  
  .social-button {
    font-size: 0.9rem;
  }
}
</style> 