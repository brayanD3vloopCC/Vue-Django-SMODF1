<template>
  <nav class="navbar">
    <div class="navbar-logo">
      <img src="@/assets/smodlogotype.jpg" alt="Logo" class="navbar-img" />
      <span class="navbar-title">SMOD F1</span>
    </div>
    <ul class="navbar-links">
      <li><a href="#" class="nav-link active">Inicio</a></li>
      <li><a href="#features" class="nav-link">Características</a></li>
      <li><a href="#roadmap" class="nav-link">Roadmap</a></li>
      <li><a href="#contacto" class="nav-link">Contacto</a></li>
    </ul>
    <div class="navbar-actions">
      <template v-if="!usuario">
        <a href="/register" class="nav-btn nav-btn-outline">Registrarse</a>
        <a href="/login" class="nav-btn nav-btn-filled">Iniciar Sesión</a>
      </template>
      <template v-else>
        <div class="user-menu-container">
          <div class="user-panel" @click="toggleUserPanel">
            <i class="fas fa-user-circle user-icon"></i>
            <span class="user-nickname">{{ usuario.nickname || usuario.correo }}</span>
            <i class="fas fa-chevron-down chevron" :class="{ open: showUserPanel }"></i>
          </div>
          <div v-if="showUserPanel" class="user-dropdown">
            <div class="user-info">
              <i class="fas fa-user"></i>
              <div>
                <div class="user-nickname-main">{{ usuario.nickname || usuario.correo }}</div>
                <div class="user-email">{{ usuario.correo }}</div>
              </div>
            </div>
            <router-link to="/sistema/perfil" class="dropdown-link"><i class="fas fa-id-badge"></i> Perfil</router-link>
            <button class="dropdown-link logout" @click="handleLogout"><i class="fas fa-sign-out-alt"></i> Cerrar Sesión</button>
          </div>
        </div>
      </template>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'NavBar',
  data() {
    return {
      usuario: null,
      showUserPanel: false
    }
  },
  mounted() {
    this.loadUsuario()
    document.addEventListener('click', this.handleClickOutside)
  },
  beforeUnmount() {
    document.removeEventListener('click', this.handleClickOutside)
  },
  methods: {
    loadUsuario() {
      const user = localStorage.getItem('usuario_smodf1')
      this.usuario = user ? JSON.parse(user) : null
    },
    handleLogout() {
      localStorage.removeItem('usuario_smodf1');
      this.$router.push('/login');
    },
    toggleUserPanel(e) {
      this.showUserPanel = !this.showUserPanel
      if (e) e.stopPropagation()
    },
    handleClickOutside(e) {
      if (!this.$el.contains(e.target)) {
        this.showUserPanel = false
      }
    }
  },
  watch: {
    // Si el usuario cambia en localStorage, recarga
    '$route'() {
      this.loadUsuario()
    }
  }
}
</script>

<style scoped>
.navbar {
  width: 100vw;
  max-width: 100vw;
  height: 64px;
  background: linear-gradient(90deg, #101010 60%, #1a2a3a 100%);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 40px;
  z-index: 1000;
  box-shadow: 0 2px 12px rgba(0,0,0,0.18);
  border-bottom: 2px solid #a3c9e2;
  position: fixed;
  top: 0;
  left: 0;
  box-sizing: border-box;
  overflow-x: hidden;
}

.navbar-logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.navbar-img {
  width: 38px;
  height: 38px;
  border-radius: 8px;
  background: #fff;
  object-fit: contain;
}

.navbar-title {
  font-size: 1.5rem;
  color: #a3c9e2;
  font-weight: bold;
  letter-spacing: 0.08em;
}

.navbar-links {
  list-style: none;
  display: flex;
  gap: 32px;
  margin: 0;
  padding: 0;
}

.nav-link {
  color: #fff;
  text-decoration: none;
  font-size: 1.1rem;
  font-family: 'Share Tech Mono', monospace;
  transition: color 0.2s;
  padding: 6px 0;
  border-bottom: 2px solid transparent;
}
.nav-link.active,
.nav-link:hover {
  color: #a3c9e2;
  border-bottom: 2px solid #a3c9e2;
}

.navbar-actions {
  display: flex;
  gap: 16px;
  align-items: center;
}

.nav-btn {
  font-family: 'Share Tech Mono', monospace;
  font-size: 1.05rem;
  padding: 7px 22px;
  border-radius: 8px;
  border: 2px solid #a3c9e2;
  text-decoration: none;
  font-weight: bold;
  transition: all 0.2s;
  margin-left: 4px;
  box-shadow: 0 2px 8px rgba(163,201,226,0.08);
}

.nav-btn-outline {
  background: transparent;
  color: #a3c9e2;
}

.nav-btn-outline:hover {
  background: #a3c9e2;
  color: #101010;
  border-color: #fff;
}

.nav-btn-filled {
  background: #a3c9e2;
  color: #101010;
  border: 2px solid #a3c9e2;
}

.nav-btn-filled:hover {
  background: #101010;
  color: #a3c9e2;
  border-color: #fff;
}

.user-menu-container {
  position: relative;
}

.user-panel {
  display: flex;
  align-items: center;
  background: #232b36;
  border-radius: 18px;
  padding: 6px 16px;
  cursor: pointer;
  position: relative;
  gap: 10px;
  min-width: 120px;
  box-shadow: 0 2px 8px #a3c9e244;
  transition: background 0.2s;
}
.user-panel:hover, .user-panel:focus {
  background: #2a3a4a;
}
.user-icon {
  font-size: 1.5rem;
  color: #a3c9e2;
}
.user-nickname {
  font-size: 1.08rem;
  font-weight: bold;
  color: #fff;
  margin-right: 4px;
}
.chevron {
  font-size: 1rem;
  color: #a3c9e2;
  transition: transform 0.2s;
}
.chevron.open {
  transform: rotate(180deg);
}
.user-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  z-index: 9999;
  background: #222e3c;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  border-radius: 8px;
  min-width: 210px;
  padding: 16px 0 8px 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
  animation: fadeIn 0.2s;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}
.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 18px 8px 18px;
  border-bottom: 1px solid #2a3a4a;
  margin-bottom: 8px;
}
.user-info i {
  font-size: 1.5rem;
  color: #a3c9e2;
}
.user-nickname-main {
  font-size: 1.1rem;
  font-weight: bold;
  color: #fff;
}
.user-email {
  font-size: 0.95rem;
  color: #a3c9e2;
}
.dropdown-link {
  background: none;
  border: none;
  color: #fff;
  text-align: left;
  padding: 10px 18px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
}
.dropdown-link:hover {
  background: #232b36;
  color: #a3c9e2;
}
.logout {
  color: #ff4d4d;
}
.logout:hover {
  background: #fff;
  color: #ff4d4d;
}
@media (max-width: 900px) {
  .navbar {
    padding: 0 8px;
  }
  .navbar-links {
    gap: 12px;
  }
  .navbar-actions {
    gap: 8px;
  }
  .nav-btn {
    font-size: 0.95rem;
    padding: 6px 12px;
  }
  .user-panel {
    min-width: 80px;
    padding: 6px 8px;
  }
  .user-dropdown {
    min-width: 150px;
    padding: 10px 0 6px 0;
  }
}
</style> 