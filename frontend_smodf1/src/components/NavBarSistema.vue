<template>
  <nav class="navbar-sistema">
    <div class="navbar-sistema-logo">
      <img src="@/assets/smodlogotype.jpg" alt="Logo" class="navbar-sistema-img" />
      <span class="navbar-sistema-title">SMOD F1</span>
    </div>
    <ul class="navbar-sistema-links">
      <li><router-link to="/sistema" class="nav-link" exact>LÍNEA INICIAL</router-link></li>
      <li><router-link to="/sistema/analisis" class="nav-link">Análisis</router-link></li>
      <li><router-link to="/sistema/proyectos" class="nav-link">Proyectos</router-link></li>
      <li><router-link to="/constructorproyecto" class="nav-link">Constructor</router-link></li>
      <li><router-link to="/sistema/imagenes" class="nav-link">Imágenes</router-link></li>
      <li><router-link to="/sistema/modelos" class="nav-link">Modelos</router-link></li>
    </ul>
    <div class="navbar-sistema-actions">
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
    </div>
  </nav>
</template>

<script>
export default {
  name: 'NavBarSistema',
  data() {
    return {
      usuario: {},
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
      this.usuario = user ? JSON.parse(user) : {}
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
    '$route'() {
      this.loadUsuario()
    }
  }
}
</script>

<style scoped>
.navbar-sistema {
  width: 100vw;
  max-width: 100vw;
  height: 64px;
  background: linear-gradient(90deg, #181c22 60%, #2a3a4a 100%);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
  z-index: 2000;
  box-shadow: 0 2px 12px rgba(0,0,0,0.18);
  border-bottom: 2px solid #a3c9e2;
  position: fixed;
  top: 0;
  left: 0;
  box-sizing: border-box;
  overflow-x: hidden;
}

.navbar-sistema-logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.navbar-sistema-img {
  width: 38px;
  height: 38px;
  border-radius: 8px;
  background: #fff;
  object-fit: contain;
}

.navbar-sistema-title {
  font-size: 1.5rem;
  color: #a3c9e2;
  font-weight: bold;
  letter-spacing: 0.08em;
}

.navbar-sistema-links {
  list-style: none;
  display: flex;
  gap: 28px;
  margin: 0;
  padding: 0;
}

.nav-link {
  color: #fff;
  text-decoration: none;
  font-size: 1.08rem;
  font-family: 'Share Tech Mono', monospace;
  transition: color 0.2s;
  padding: 6px 0;
  border-bottom: 2px solid transparent;
}
.nav-link.router-link-exact-active,
.nav-link.router-link-active,
.nav-link:hover {
  color: #a3c9e2;
  border-bottom: 2px solid #a3c9e2;
}

.navbar-sistema-actions {
  display: flex;
  gap: 18px;
  align-items: center;
}

.user-menu-container {
  position: relative;
}

.user-panel {
  display: flex;
  align-items: center;
  background: #232b36;
  border-radius: 8px;
  padding: 6px 14px;
  cursor: pointer;
  gap: 8px;
  font-size: 1.08rem;
  transition: background 0.2s;
}
.user-panel:hover {
  background: #2a3a4a;
}
.user-icon {
  font-size: 1.5rem;
  color: #a3c9e2;
}
.chevron {
  margin-left: 6px;
  transition: transform 0.2s;
}
.chevron.open {
  transform: rotate(180deg);
}
.user-dropdown {
  position: absolute;
  right: 0;
  top: 110%;
  background: #232b36;
  border-radius: 10px;
  box-shadow: 0 2px 12px #00000033;
  min-width: 180px;
  z-index: 10;
  padding: 12px 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 16px;
  border-bottom: 1px solid #a3c9e2;
  margin-bottom: 6px;
}
.user-nickname-main {
  font-weight: bold;
  color: #a3c9e2;
}
.user-email {
  font-size: 0.95rem;
  color: #e0e0e0;
}
.dropdown-link {
  background: none;
  border: none;
  color: #fff;
  text-align: left;
  padding: 10px 18px;
  font-size: 1.05rem;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
}
.dropdown-link.logout {
  color: #ff7fa3;
}
.dropdown-link:hover {
  background: #181c22;
  color: #a3c9e2;
}
</style> 