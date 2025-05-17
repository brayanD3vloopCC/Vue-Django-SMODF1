<template>
  <aside class="sidebar">
    <div class="sidebar-header">
      <img src="@/assets/smodlogotype.jpg" alt="Logo" class="sidebar-logo" />
      <span class="sidebar-title">SMOD F1</span>
    </div>
    <nav class="sidebar-nav">
      <router-link to="/sistema" class="sidebar-link" exact>
        <i class="fas fa-home"></i> Linea Inicial
      </router-link>
      
      <router-link to="/sistema/proyectos" class="sidebar-link">
        <i class="fas fa-project-diagram"></i> Proyectos
      </router-link>

      <router-link to="/constructorproyecto" class="sidebar-link">
        <i class="fas fa-tools"></i> Constructor
      </router-link>

      <router-link to="/sistema/analisis" class="sidebar-link">
        <i class="fas fa-search"></i> DataSheets
      </router-link>
      <router-link to="/sistema/imagenes" class="sidebar-link">
        <i class="fas fa-image"></i> Imagenes
      </router-link>
      <router-link to="/sistema/modelos" class="sidebar-link">
        <i class="fas fa-cubes"></i> Modelos
      </router-link>
    </nav>
    <div class="sidebar-divider"></div>
    <nav class="sidebar-nav sidebar-nav-bottom">
      <router-link to="/sistema/perfil" class="sidebar-link">
        <i class="fas fa-user"></i> Perfil
      </router-link>
    </nav>
    <div class="sidebar-user" v-if="usuario">
      <i class="fas fa-user-circle sidebar-user-icon"></i>
      <div class="sidebar-user-info">
        <div class="sidebar-user-nickname">{{ usuario.nickname || usuario.correo }}</div>
        <div class="sidebar-user-email">{{ usuario.correo }}</div>
      </div>
    </div>
  </aside>
</template>


<script>
export default {
  name: 'SmodSidebar',
  data() {
    return {
      usuario: null
    }
  },
  mounted() {
    this.loadUsuario()
  },
  methods: {
    loadUsuario() {
      const user = localStorage.getItem('usuario_smodf1')
      this.usuario = user ? JSON.parse(user) : null
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
.sidebar {
  width: 240px;
  background: linear-gradient(180deg, #181c22 70%, #232b36 100%);
  color: #fff;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-shadow: 2px 0 16px rgba(0,0,0,0.16);
  padding-top: 24px;
  position: relative;
}
.sidebar-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 32px;
}
.sidebar-logo {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  margin-bottom: 8px;
  box-shadow: 0 2px 8px #a3c9e244;
}
.sidebar-title {
  font-size: 1.3rem;
  color: #a3c9e2;
  font-weight: bold;
  letter-spacing: 0.08em;
}
.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
  padding: 0 0 0 0;
}
.sidebar-nav-bottom {
  margin-top: auto;
  margin-bottom: 16px;
}
.sidebar-link {
  color: #fff;
  text-decoration: none;
  font-size: 1.08rem;
  padding: 12px 28px 12px 22px;
  border-radius: 12px 0 0 12px;
  transition: background 0.18s, color 0.18s, box-shadow 0.18s;
  margin-left: 8px;
  display: flex;
  align-items: center;
  gap: 12px;
  font-weight: 500;
  position: relative;
}
.sidebar-link i {
  font-size: 1.18rem;
  color: #a3c9e2;
  min-width: 22px;
  text-align: center;
}
.sidebar-link.router-link-exact-active,
.sidebar-link.router-link-active {
  background: linear-gradient(90deg, #a3c9e2 80%, #fff 100%);
  color: #101010;
  box-shadow: 2px 2px 12px #a3c9e244;
  font-weight: bold;
}
.sidebar-link.router-link-exact-active i,
.sidebar-link.router-link-active i {
  color: #101010;
}
.sidebar-link:hover {
  background: #232b36;
  color: #a3c9e2;
  box-shadow: 0 2px 8px #a3c9e244;
}
.sidebar-divider {
  width: 80%;
  height: 1.5px;
  background: #a3c9e2;
  border-radius: 1px;
  margin: 24px 0 8px 0;
  opacity: 0.25;
}
.sidebar-user {
  width: 90%;
  background: #232b36;
  border-radius: 12px;
  padding: 14px 12px 12px 12px;
  margin-bottom: 18px;
  display: flex;
  align-items: center;
  gap: 12px;
  box-shadow: 0 2px 8px #a3c9e244;
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
}
.sidebar-user-icon {
  font-size: 2.1rem;
  color: #a3c9e2;
}
.sidebar-user-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.sidebar-user-nickname {
  font-size: 1.08rem;
  font-weight: bold;
  color: #fff;
}
.sidebar-user-email {
  font-size: 0.97rem;
  color: #a3c9e2;
}
</style> 