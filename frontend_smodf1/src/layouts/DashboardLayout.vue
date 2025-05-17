<template>
  <div class="dashboard-layout">
    <Sidebar />
    <div class="main-content">
      <NavBarSistema />
      <div class="dashboard-content">
        <h2 class="dashboard-section-title">{{ sectionTitle }}</h2>
        <transition name="fade" mode="out-in">
          <router-view />
        </transition>
      </div>
    </div>
  </div>
</template>

<script>
import Sidebar from '@/components/Sidebar.vue'
import NavBarSistema from '@/components/NavBarSistema.vue'
export default {
  name: 'DashboardLayout',
  components: { Sidebar, NavBarSistema },
  computed: {
    sectionTitle() {
      const route = this.$route;
      switch (route.name) {
        case 'sistema': return 'Linea Inicial';
        case 'analisis': return 'Análisis';
        case 'proyectos': return 'Proyectos';
        case 'imagenes': return 'Imágenes';
        case 'modelos': return 'Modelos';
        case 'perfil': return 'Perfil';
        default: return '';
      }
    }
  }
}
</script>

<style scoped>
.dashboard-layout {
  display: flex;
  min-height: 100vh;
  background: linear-gradient(135deg, #101010 0%, #1a2a3a 100%);
}
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}
.dashboard-content {
  flex: 1;
  padding: 32px 24px 24px 24px;
  background: transparent;
}
.dashboard-section-title {
  color: #a3c9e2;
  font-size: 1.5rem;
  margin-bottom: 18px;
  margin-top: 8px;
  text-align: left;
  font-family: 'VT323', monospace;
  letter-spacing: 0.04em;
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.25s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style> 