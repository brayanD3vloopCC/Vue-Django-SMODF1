<template>
  <div class="sistema-dashboard">
    <h1 class="dashboard-title">Panel Principal SMOD F1</h1>
    <div class="dashboard-grid">
      <router-link to="/ConstructorProyecto" class="dashboard-card" @mouseenter="hovered = 'proyectos'" @mouseleave="hovered = ''">
        <i v-if="hovered !== 'proyectos'" class="fas fa-folder-open"></i>
        <span v-else class="plus-icon">+</span>
        <h2>Proyectos</h2>
        <p>Gestiona y organiza tus proyectos en SMOD F1.</p>
      </router-link>
      <router-link to="/ConstructorProyecto" class="dashboard-card" @mouseenter="hovered = 'constructor'" @mouseleave="hovered = ''">
        <i v-if="hovered !== 'constructor'" class="fas fa-tools"></i>
        <span v-else class="plus-icon">+</span>
        <h2>Constructor</h2>
        <p>Entorno de trabajo para procesamiento de visión artificial.</p>
      </router-link>
      <router-link to="/analisis" class="dashboard-card" @mouseenter="hovered = 'analisis'" @mouseleave="hovered = ''">
        <i v-if="hovered !== 'analisis'" class="fas fa-brain"></i>
        <span v-else class="plus-icon">+</span>
        <h2>Análisis</h2>
        <p>Procesamiento de imágenes mediante datos DATASHEETS o archivos JSON.</p>
      </router-link>
      <router-link to="/imagenes" class="dashboard-card" @mouseenter="hovered = 'imagenes'" @mouseleave="hovered = ''">
        <i v-if="hovered !== 'imagenes'" class="fas fa-image"></i>
        <span v-else class="plus-icon">+</span>
        <h2>Imágenes</h2>
        <p>Sube, visualiza y administra tus imágenes.</p>
      </router-link>
      <router-link to="/EstudioThree" class="dashboard-card" @mouseenter="hovered = 'modelos'" @mouseleave="hovered = ''">
        <i v-if="hovered !== 'modelos'" class="fas fa-cube"></i>
        <span v-else class="plus-icon">+</span>
        <h2>Modelos 3D</h2>
        <p>Entorno de modelado y visualización 3D para tus proyectos.</p>
      </router-link>
      <router-link to="/sistema/perfil" class="dashboard-card" @mouseenter="hovered = 'perfil'" @mouseleave="hovered = ''">
        <i v-if="hovered !== 'perfil'" class="fas fa-user"></i>
        <span v-else class="plus-icon">+</span>
        <h2>Perfil</h2>
        <p>Configura tu cuenta y preferencias.</p>
      </router-link>
    </div>
    <div v-if="showProfile" class="profile-section">
      <div v-if="!userData" class="profile-loading">
        <i class="fas fa-spinner fa-spin"></i> Cargando perfil...
      </div>
      <div v-else class="perfil-admin-layout">
        <div class="perfil-admin-avatar-col">
          <div class="perfil-admin-avatar">
            <i class="fas fa-user-tie"></i>
          </div>
        </div>
        <div class="perfil-admin-data-col">
          <h2 class="perfil-admin-title">Información Básica del Usuario</h2>
          <div class="perfil-admin-block">
            <div class="perfil-admin-row">
              <label>Nombre completo:</label>
              <span v-if="!editMode">{{ userData.name || '-' }}</span>
              <input v-else v-model="editData.name" type="text" />
            </div>
            <div class="perfil-admin-row">
              <label>Nickname:</label>
              <span v-if="!editMode">{{ userData.nickname || '-' }}</span>
              <input v-else v-model="editData.nickname" type="text" />
            </div>
            <div class="perfil-admin-row">
              <label>Correo electrónico:</label>
              <span>{{ userData.email || '-' }}</span>
            </div>
            <div class="perfil-admin-row">
              <label>Rol:</label>
              <span class="perfil-admin-role-badge">{{ userData.role || '-' }}</span>
            </div>
          </div>
          <div class="perfil-admin-actions">
            <button v-if="!editMode" @click="editMode = true; editData = { ...userData }" class="perfil-admin-btn perfil-admin-btn-edit"><i class="fas fa-pen"></i> Editar</button>
            <div v-else>
              <button @click="saveProfile" class="perfil-admin-btn perfil-admin-btn-save"><i class="fas fa-save"></i> Guardar</button>
              <button @click="cancelEdit" class="perfil-admin-btn perfil-admin-btn-cancel"><i class="fas fa-times"></i> Cancelar</button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="dashboard-descriptions">
      <div class="desc-item"><b>Análisis:</b> Permite aplicar modelos de visión artificial para detectar, clasificar y extraer información relevante de tus imágenes. Ideal para tareas de reconocimiento, segmentación y más.</div>
      <div class="desc-item"><b>Proyectos:</b> Centraliza y administra todos tus experimentos, prototipos y desarrollos de visión artificial. Lleva un seguimiento de avances, resultados y colaboraciones.</div>
      <div class="desc-item"><b>Imágenes:</b> Gestiona tu repositorio de imágenes, sube nuevos archivos, visualiza resultados y organiza tus datos para análisis y entrenamiento de modelos.</div>
      <div class="desc-item"><b>Modelos:</b> Accede a tus modelos de visión artificial, consulta detalles técnicos, versiones y resultados de pruebas. Administra tanto modelos 2D como reconstrucciones 3D.</div>
      <div class="desc-item"><b>Perfil:</b> Personaliza tu información, gestiona credenciales y ajusta preferencias de notificación y privacidad en la plataforma.</div>
    </div>
  </div>
</template>

<script>
import { userService } from '@/services/userService';

export default {
  name: 'SistemaView',
  data() {
    return {
      hovered: '',
      userData: null,
      showProfile: false,
      editMode: false,
      editData: {}
    }
  },
  async created() {
    try {
      this.userData = await userService.getCurrentUser();
    } catch (error) {
      console.error('Error loading user data:', error);
    }
  },
  watch: {
    '$route'(to) {
      this.showProfile = to.path === '/sistema/perfil';
    }
  },
  methods: {
    enableEdit() {
      this.editMode = true;
      this.editData = { ...this.userData };
      this.$nextTick(() => {
        const input = this.$el.querySelector('.profile-edit-input');
        if (input) input.focus();
      });
    },
    async saveProfile() {
      try {
        await userService.updateUserProfile(this.editData);
        this.userData = { ...this.editData };
        this.editMode = false;
        alert('Perfil actualizado exitosamente');
      } catch (error) {
        alert('Error al actualizar el perfil');
      }
    },
    cancelEdit() {
      this.editMode = false;
      this.editData = {};
    }
  }
}
</script>

<style scoped>
.sistema-dashboard {
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 32px;
}
.dashboard-title {
  color: #fff;
  font-size: 2.2rem;
  margin-bottom: 18px;
  font-family: 'VT323', monospace;
  letter-spacing: 0.04em;
}
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 32px;
  width: 100%;
  max-width: 1100px;
}
.dashboard-card {
  background: linear-gradient(135deg, #181c22 60%, #232b36 100%);
  color: #fff;
  border-radius: 18px;
  padding: 32px 24px;
  text-align: center;
  text-decoration: none;
  box-shadow: 0 4px 24px rgba(0,0,0,0.13);
  transition: transform 0.18s, box-shadow 0.18s;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  position: relative;
}
.dashboard-card:hover {
  transform: translateY(-6px) scale(1.03);
  box-shadow: 0 8px 32px rgba(163,201,226,0.18);
  background: linear-gradient(135deg, #232b36 60%, #181c22 100%);
  color: #a3c9e2;
}
.dashboard-card i {
  font-size: 2.5rem;
  margin-bottom: 10px;
  color: #a3c9e2;
  transition: opacity 0.18s;
}
.plus-icon {
  font-size: 2.7rem;
  color: #7fff7f;
  font-weight: bold;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: #232b36;
  box-shadow: 0 2px 8px #a3c9e244;
  animation: plusPop 0.18s;
  transition: transform 0.18s, background 0.18s, color 0.18s;
}
.dashboard-card:hover .plus-icon {
  background: #a3c9e2;
  color: #101010;
  transform: scale(1.18) rotate(12deg);
}
@keyframes plusPop {
  0% { transform: scale(0.7); opacity: 0.2; }
  100% { transform: scale(1); opacity: 1; }
}
.dashboard-card h2 {
  font-size: 1.3rem;
  margin-bottom: 6px;
}
.dashboard-card p {
  font-size: 1rem;
  color: #bfc9d1;
}
.dashboard-descriptions {
  margin-top: 38px;
  max-width: 900px;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 8px;
  color: #bfc9d1;
  font-size: 1.08rem;
  padding: 18px 12px 0 12px;
  text-align: left;
}
.desc-item {
  margin-bottom: 2px;
}
.profile-section {
  margin-top: 32px;
  width: 100%;
  max-width: 700px;
  padding: 0 20px;
  display: flex;
  justify-content: center;
}
.perfil-admin-layout {
  display: flex;
  flex-direction: row;
  background: linear-gradient(135deg, #181c22 60%, #232b36 100%);
  border-radius: 18px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.18);
  width: 100%;
  max-width: 800px;
  min-height: 320px;
  margin: 0 auto;
  padding: 32px 0;
}
.perfil-admin-avatar-col {
  flex: 0 0 180px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  padding: 0 24px;
  border-right: 1px solid #263040;
}
.perfil-admin-avatar {
  width: 120px;
  height: 120px;
  background: #232b36;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 18px;
  box-shadow: 0 2px 12px #a3c9e244;
}
.perfil-admin-avatar i {
  font-size: 80px;
  color: #a3c9e2;
}
.perfil-admin-data-col {
  flex: 1;
  padding: 0 32px;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}
.perfil-admin-title {
  color: #a3c9e2;
  font-size: 1.3rem;
  margin-bottom: 18px;
  font-family: 'VT323', monospace;
}
.perfil-admin-block {
  background: rgba(35, 43, 54, 0.5);
  border-radius: 12px;
  padding: 24px 18px;
  margin-bottom: 18px;
  border: 1px solid #263040;
}
.perfil-admin-row {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}
.perfil-admin-row label {
  flex: 0 0 160px;
  color: #bfc9d1;
  font-weight: 500;
  font-size: 1rem;
  margin-right: 12px;
}
.perfil-admin-row span {
  color: #fff;
  font-size: 1.05rem;
}
.perfil-admin-row input {
  background: #181c22;
  border: 1px solid #3a4553;
  border-radius: 8px;
  padding: 7px 12px;
  color: #fff;
  font-size: 1.05rem;
  min-width: 180px;
}
.perfil-admin-role-badge {
  background: #232b36;
  color: #a3c9e2;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 0.95rem;
  border: 1px solid #a3c9e2;
}
.perfil-admin-actions {
  display: flex;
  gap: 12px;
  margin-top: 8px;
}
.perfil-admin-btn {
  background: #a3c9e2;
  color: #101010;
  border: none;
  border-radius: 8px;
  padding: 10px 22px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.2s, color 0.2s, transform 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1rem;
}
.perfil-admin-btn-edit:hover, .perfil-admin-btn-save:hover {
  background: #7fff7f;
  color: #101010;
  transform: translateY(-2px);
}
.perfil-admin-btn-cancel {
  background: #232b36;
  color: #a3c9e2;
  border: 1px solid #a3c9e2;
}
.perfil-admin-btn-cancel:hover {
  background: #a3c9e2;
  color: #232b36;
}
@media (max-width: 800px) {
  .perfil-admin-layout {
    flex-direction: column;
    align-items: center;
    padding: 18px 0;
  }
  .perfil-admin-avatar-col {
    border-right: none;
    border-bottom: 1px solid #263040;
    padding-bottom: 18px;
    margin-bottom: 18px;
  }
  .perfil-admin-data-col {
    padding: 0 12px;
  }
  .perfil-admin-row label {
    flex: 0 0 100px;
    font-size: 0.95rem;
  }
}
.profile-loading {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #a3c9e2;
  font-size: 1.2rem;
  min-height: 180px;
  gap: 12px;
}
</style> 