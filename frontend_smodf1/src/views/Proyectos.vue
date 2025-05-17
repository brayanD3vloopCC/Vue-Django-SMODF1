<template>
  <div class="proyectos-page">
    <!-- Cabecera para la versión standalone -->
    <div v-if="isStandalone" class="standalone-header">
      <div class="logo-container">
        <img src="@/assets/logo.png" alt="SMODF1 Logo" class="logo">
        <h1>SMODF1</h1>
      </div>
      <div class="header-actions">
        <button @click="goToHome" class="btn-home">
          <i class="fas fa-home"></i> Inicio
        </button>
        <button @click="toggleLoginModal" class="btn-login" v-if="!isLoggedIn">
          <i class="fas fa-sign-in-alt"></i> Iniciar Sesión
        </button>
        <button @click="logout" class="btn-logout" v-else>
          <i class="fas fa-sign-out-alt"></i> Cerrar Sesión
        </button>
      </div>
    </div>

    <div class="proyectos-container">
      <div class="proyectos-header">
        <h1>{{ isStandalone ? 'Explorar Proyectos' : 'Mis Proyectos' }}</h1>
        <div class="header-actions">
          <div class="search-box">
            <input 
              type="text" 
              v-model="searchQuery" 
              placeholder="Buscar proyectos..." 
              @input="filterProjects"
            >
            <i class="fas fa-search"></i>
          </div>
          <div class="view-toggle">
            <button 
              @click="viewMode = 'grid'" 
              :class="{ active: viewMode === 'grid' }"
              title="Vista de cuadrícula"
            >
              <i class="fas fa-th-large"></i>
            </button>
            <button 
              @click="viewMode = 'list'" 
              :class="{ active: viewMode === 'list' }"
              title="Vista de lista"
            >
              <i class="fas fa-list"></i>
            </button>
          </div>
          <button @click="showNewProjectModal = true" class="btn-new-project">
            <i class="fas fa-plus"></i> Nuevo Proyecto
          </button>
        </div>
      </div>

      <div class="proyectos-tools">
        <div class="filter-options">
          <select v-model="sortOption" @change="sortProjects">
            <option value="newest">Más recientes</option>
            <option value="oldest">Más antiguos</option>
            <option value="name-asc">Nombre (A-Z)</option>
            <option value="name-desc">Nombre (Z-A)</option>
            <option value="images-desc">Más imágenes</option>
          </select>
        </div>
        <div class="proyectos-stats" v-if="projects.length">
          <span><i class="fas fa-folder"></i> {{ projects.length }} proyectos</span>
          <span><i class="fas fa-image"></i> {{ totalImages }} imágenes</span>
        </div>
      </div>

      <!-- Lista de Proyectos - Vista de Cuadrícula -->
      <div class="proyectos-grid" v-if="filteredProjects.length && viewMode === 'grid'">
        <div v-for="project in filteredProjects" :key="project.id" class="proyecto-card">
          <div class="proyecto-header">
            <h3>{{ project.name }}</h3>
            <div class="proyecto-actions-menu">
              <button class="btn-menu" @click="toggleProjectMenu(project)">
                <i class="fas fa-ellipsis-v"></i>
              </button>
              <div class="dropdown-menu" v-if="project.showMenu">
                <button @click="editProject(project)">
                  <i class="fas fa-edit"></i> Editar
                </button>
                <button @click="deleteProject(project)">
                  <i class="fas fa-trash"></i> Eliminar
                </button>
              </div>
            </div>
          </div>
          <p class="proyecto-desc">{{ project.description || 'Sin descripción' }}</p>
          <div class="proyecto-preview">
            <div v-if="project.images && project.images.length" class="proyecto-images">
              <img :src="project.images[0].image" alt="Preview" class="preview-image">
              <div class="image-count" v-if="project.images.length > 1">+{{ project.images.length - 1 }}</div>
            </div>
            <div v-else class="no-images-preview">
              <i class="fas fa-images"></i>
              <span>Sin imágenes</span>
            </div>
          </div>
          <div class="proyecto-stats">
            <span><i class="fas fa-image"></i> {{ project.images ? project.images.length : 0 }} imágenes</span>
            <span><i class="fas fa-clock"></i> {{ formatDate(project.updated_at) }}</span>
          </div>
          <div class="proyecto-actions">
            <button @click="selectProject(project)" class="btn-upload">
              <i class="fas fa-upload"></i> Subir Imagen
            </button>
            <button @click="viewProject(project)" class="btn-view">
              <i class="fas fa-eye"></i> Ver
            </button>
          </div>
        </div>
      </div>

      <!-- Lista de Proyectos - Vista de Lista -->
      <div class="proyectos-list" v-if="filteredProjects.length && viewMode === 'list'">
        <table>
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Descripción</th>
              <th>Imágenes</th>
              <th>Fecha de creación</th>
              <th>Última actualización</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="project in filteredProjects" :key="project.id">
              <td class="project-name">{{ project.name }}</td>
              <td class="project-description">{{ project.description || 'Sin descripción' }}</td>
              <td class="project-images-count">{{ project.images ? project.images.length : 0 }}</td>
              <td>{{ formatDate(project.created_at) }}</td>
              <td>{{ formatDate(project.updated_at) }}</td>
              <td class="project-actions">
                <button @click="selectProject(project)" class="btn-upload-sm" title="Subir Imagen">
                  <i class="fas fa-upload"></i>
                </button>
                <button @click="viewProject(project)" class="btn-view-sm" title="Ver Proyecto">
                  <i class="fas fa-eye"></i>
                </button>
                <button @click="editProject(project)" class="btn-edit-sm" title="Editar Proyecto">
                  <i class="fas fa-edit"></i>
                </button>
                <button @click="deleteProject(project)" class="btn-delete-sm" title="Eliminar Proyecto">
                  <i class="fas fa-trash"></i>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-else-if="!loading" class="no-projects">
        <i class="fas fa-folder-open"></i>
        <p v-if="searchQuery">No se encontraron proyectos que coincidan con tu búsqueda</p>
        <p v-else>No tienes proyectos aún. ¡Crea uno nuevo!</p>
        <button @click="showNewProjectModal = true" class="btn-new-project-empty">
          <i class="fas fa-plus"></i> Crear Mi Primer Proyecto
        </button>
      </div>

      <!-- Modal Nuevo Proyecto -->
      <div v-if="showNewProjectModal" class="modal-overlay" @click="showNewProjectModal = false">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h2>{{ editingProject ? 'Editar Proyecto' : 'Nuevo Proyecto' }}</h2>
            <button @click="showNewProjectModal = false" class="btn-close">
              <i class="fas fa-times"></i>
            </button>
          </div>
          <form @submit.prevent="createOrUpdateProject">
            <div class="form-group">
              <label>Nombre del Proyecto</label>
              <input v-model="newProject.name" type="text" required>
            </div>
            <div class="form-group">
              <label>Descripción</label>
              <textarea v-model="newProject.description" rows="4"></textarea>
            </div>
            <div class="modal-actions">
              <button type="button" @click="showNewProjectModal = false" class="btn-cancel">Cancelar</button>
              <button type="submit" class="btn-create">
                {{ editingProject ? 'Guardar Cambios' : 'Crear Proyecto' }}
              </button>
            </div>
          </form>
        </div>
      </div>

      <!-- Modal Eliminar Proyecto -->
      <div v-if="showDeleteModal" class="modal-overlay" @click="showDeleteModal = false">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h2>Eliminar Proyecto</h2>
            <button @click="showDeleteModal = false" class="btn-close">
              <i class="fas fa-times"></i>
            </button>
          </div>
          <div class="delete-confirmation">
            <i class="fas fa-exclamation-triangle"></i>
            <p>¿Estás seguro de que deseas eliminar el proyecto <strong>{{ projectToDelete?.name }}</strong>?</p>
            <p class="warning">Esta acción no se puede deshacer y eliminará todas las imágenes asociadas.</p>
          </div>
          <div class="modal-actions">
            <button @click="showDeleteModal = false" class="btn-cancel">Cancelar</button>
            <button @click="confirmDeleteProject" class="btn-delete">Eliminar</button>
          </div>
        </div>
      </div>

      <!-- Modal Subir Imagen -->
      <div v-if="showUploadModal" class="modal-overlay" @click="showUploadModal = false">
        <div class="modal-content" @click.stop>
          <h2>Subir Imagen</h2>
          <div class="upload-area" @drop.prevent="handleDrop" @dragover.prevent>
            <input type="file" ref="fileInput" @change="handleFileSelect" accept="image/*" style="display: none">
            <div class="upload-placeholder" @click="$refs.fileInput.click()">
              <i class="fas fa-cloud-upload-alt"></i>
              <p>Arrastra una imagen aquí o haz clic para seleccionar</p>
            </div>
          </div>
          <div v-if="uploadPreview" class="upload-preview">
            <img :src="uploadPreview" alt="Preview">
            <div class="preview-info">
              <p>{{ selectedFile.name }}</p>
              <p>{{ formatSize(selectedFile.size) }}</p>
            </div>
          </div>
          <div class="modal-actions">
            <button @click="showUploadModal = false" class="btn-cancel">Cancelar</button>
            <button @click="uploadImage" :disabled="!selectedFile" class="btn-upload">
              Subir y Procesar
            </button>
          </div>
        </div>
      </div>

      <!-- Loading Overlay -->
      <div v-if="loading" class="loading-overlay">
        <div class="loading-content">
          <i class="fas fa-spinner fa-spin"></i>
          <p>{{ loadingMessage }}</p>
        </div>
      </div>
    </div>

    <!-- Login Modal -->
    <div v-if="showLoginModal" class="modal-overlay" @click="showLoginModal = false">
      <div class="modal-content login-modal" @click.stop>
        <div class="modal-header">
          <h2>Iniciar Sesión</h2>
          <button @click="showLoginModal = false" class="btn-close">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <form @submit.prevent="login">
          <div class="form-group">
            <label>Correo Electrónico</label>
            <input v-model="loginForm.email" type="email" required>
          </div>
          <div class="form-group">
            <label>Contraseña</label>
            <input v-model="loginForm.password" type="password" required>
          </div>
          <div class="login-actions">
            <button type="submit" class="btn-submit">Iniciar Sesión</button>
            <button type="button" @click="goToRegister" class="btn-register">Registrarse</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axiosInstance from '@/utils/axios';

export default {
  name: 'ProyectosView',
  data() {
    return {
      projects: [],
      filteredProjects: [],
      showNewProjectModal: false,
      showUploadModal: false,
      showDeleteModal: false,
      selectedProject: null,
      projectToDelete: null,
      editingProject: null,
      viewMode: 'grid',
      searchQuery: '',
      sortOption: 'newest',
      newProject: {
        name: '',
        description: ''
      },
      selectedFile: null,
      uploadPreview: null,
      loading: false,
      loadingMessage: '',
      error: null,
      isLoggedIn: !!localStorage.getItem('usuario_smodf1'),
      showLoginModal: false,
      loginForm: {
        email: '',
        password: ''
      }
    }
  },
  computed: {
    totalImages() {
      return this.projects.reduce((total, project) => {
        return total + (project.images ? project.images.length : 0);
      }, 0);
    },
    isStandalone() {
      return this.$route.name === 'proyectos-standalone';
    }
  },
  async created() {
    await this.loadProjects();
  },
  methods: {
    async loadProjects() {
      try {
        this.loading = true;
        this.loadingMessage = 'Cargando proyectos...';
        const response = await axiosInstance.get('/api/projects/');
        this.projects = response.data;
        this.filterProjects();
        this.sortProjects();
      } catch (error) {
        console.error('Error cargando proyectos:', error);
        this.error = 'Error al cargar los proyectos. Por favor, intenta de nuevo.';
      } finally {
        this.loading = false;
      }
    },
    async createOrUpdateProject() {
      if (!this.newProject.name.trim()) {
        alert('El nombre del proyecto es obligatorio');
        return;
      }

      this.loading = true;
      
      if (this.editingProject) {
        this.loadingMessage = 'Actualizando proyecto...';
        try {
          const response = await axiosInstance.put(`/api/projects/${this.editingProject.id}/`, this.newProject);
          const index = this.projects.findIndex(p => p.id === this.editingProject.id);
          if (index !== -1) {
            this.projects[index] = response.data;
          }
          this.showNewProjectModal = false;
          this.editingProject = null;
          this.newProject = { name: '', description: '' };
          this.filterProjects();
          this.sortProjects();
        } catch (error) {
          console.error('Error actualizando proyecto:', error);
          alert('Error al actualizar el proyecto. Por favor, intenta de nuevo.');
        } finally {
          this.loading = false;
        }
      } else {
        this.loadingMessage = 'Creando proyecto...';
        try {
          const response = await axiosInstance.post('/api/projects/', this.newProject);
          this.projects.unshift(response.data);
          this.showNewProjectModal = false;
          this.newProject = { name: '', description: '' };
          this.filterProjects();
          this.sortProjects();
        } catch (error) {
          console.error('Error creando proyecto:', error);
          alert('Error al crear el proyecto. Por favor, intenta de nuevo.');
        } finally {
          this.loading = false;
        }
      }
    },
    editProject(project) {
      this.editingProject = project;
      this.newProject = {
        name: project.name,
        description: project.description || ''
      };
      this.showNewProjectModal = true;
      // Cerrar el menú desplegable si está abierto
      project.showMenu = false;
    },
    deleteProject(project) {
      this.projectToDelete = project;
      this.showDeleteModal = true;
      // Cerrar el menú desplegable si está abierto
      project.showMenu = false;
    },
    async confirmDeleteProject() {
      if (!this.projectToDelete) return;
      
      this.loading = true;
      this.loadingMessage = 'Eliminando proyecto...';
      
      try {
        await axiosInstance.delete(`/api/projects/${this.projectToDelete.id}/`);
        this.projects = this.projects.filter(p => p.id !== this.projectToDelete.id);
        this.showDeleteModal = false;
        this.projectToDelete = null;
        this.filterProjects();
        this.sortProjects();
      } catch (error) {
        console.error('Error eliminando proyecto:', error);
        alert('Error al eliminar el proyecto. Por favor, intenta de nuevo.');
      } finally {
        this.loading = false;
      }
    },
    toggleProjectMenu(project) {
      // Cerrar todos los otros menús primero
      this.projects.forEach(p => {
        if (p !== project) {
          p.showMenu = false;
        }
      });
      
      // Toggle el menú del proyecto actual
      project.showMenu = !project.showMenu;
    },
    filterProjects() {
      if (!this.searchQuery) {
        this.filteredProjects = [...this.projects];
      } else {
        const query = this.searchQuery.toLowerCase();
        this.filteredProjects = this.projects.filter(project => {
          return (
            project.name.toLowerCase().includes(query) ||
            (project.description && project.description.toLowerCase().includes(query))
          );
        });
      }
      this.sortProjects();
    },
    sortProjects() {
      switch (this.sortOption) {
        case 'newest':
          this.filteredProjects.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
          break;
        case 'oldest':
          this.filteredProjects.sort((a, b) => new Date(a.created_at) - new Date(b.created_at));
          break;
        case 'name-asc':
          this.filteredProjects.sort((a, b) => a.name.localeCompare(b.name));
          break;
        case 'name-desc':
          this.filteredProjects.sort((a, b) => b.name.localeCompare(a.name));
          break;
        case 'images-desc':
          this.filteredProjects.sort((a, b) => {
            const aCount = a.images ? a.images.length : 0;
            const bCount = b.images ? b.images.length : 0;
            return bCount - aCount;
          });
          break;
        default:
          break;
      }
    },
    selectProject(project) {
      this.selectedProject = project;
      this.showUploadModal = true;
    },
    handleFileSelect(event) {
      const file = event.target.files[0];
      this.handleFile(file);
    },
    handleDrop(event) {
      const file = event.dataTransfer.files[0];
      this.handleFile(file);
    },
    handleFile(file) {
      if (file && file.type.startsWith('image/')) {
        this.selectedFile = file;
        const reader = new FileReader();
        reader.onload = e => this.uploadPreview = e.target.result;
        reader.readAsDataURL(file);
      }
    },
    async uploadImage() {
      if (!this.selectedFile || !this.selectedProject) return;

      this.loading = true;
      this.loadingMessage = 'Subiendo y procesando imagen...';
      
      const formData = new FormData();
      formData.append('image', this.selectedFile);

      try {
        const response = await axiosInstance.post(
          `/api/projects/${this.selectedProject.id}/upload_image/`,
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          }
        );
        
        console.log('Respuesta de subida:', response.data);
        
        // Recargar el proyecto específico
        const projectResponse = await axiosInstance.get(`/api/projects/${this.selectedProject.id}/`);
        const projectIndex = this.projects.findIndex(p => p.id === this.selectedProject.id);
        if (projectIndex !== -1) {
          this.projects[projectIndex] = projectResponse.data;
        }
        
        this.showUploadModal = false;
        this.selectedFile = null;
        this.uploadPreview = null;
        
        // Mostrar mensaje de éxito
        alert('Imagen subida exitosamente');
      } catch (error) {
        console.error('Error detallado:', error.response || error);
        let errorMessage = 'Error al subir la imagen. ';
        if (error.response) {
          errorMessage += error.response.data.error || JSON.stringify(error.response.data);
        }
        alert(errorMessage);
      } finally {
        this.loading = false;
      }
    },
    formatDate(date) {
      return new Date(date).toLocaleDateString();
    },
    formatSize(bytes) {
      const kb = bytes / 1024;
      return kb > 1024 ? `${(kb/1024).toFixed(2)} MB` : `${kb.toFixed(2)} KB`;
    },
    viewProject(project) {
      const routeName = this.isStandalone ? 'project-detail-standalone' : 'project-detail';
      this.$router.push({
        name: routeName,
        params: { id: project.id }
      });
    },
    goToHome() {
      this.$router.push('/');
    },
    goToRegister() {
      this.$router.push('/register');
    },
    toggleLoginModal() {
      this.showLoginModal = !this.showLoginModal;
    },
    async login() {
      try {
        this.loading = true;
        const response = await axiosInstance.post('/api/usuarios/login/', this.loginForm);
        localStorage.setItem('usuario_smodf1', JSON.stringify(response.data));
        this.isLoggedIn = true;
        this.showLoginModal = false;
        // Reload projects after login
        await this.loadProjects();
      } catch (error) {
        console.error('Error de inicio de sesión:', error);
        alert('Error al iniciar sesión. Verifica tus credenciales.');
      } finally {
        this.loading = false;
      }
    },
    logout() {
      localStorage.removeItem('usuario_smodf1');
      this.isLoggedIn = false;
      this.$router.push('/'); // Redirigir a la página principal
    }
  }
}
</script>

<style scoped>
.proyectos-page {
  min-height: 100vh;
  background: transparent;
}

.standalone-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: #2c3e50;
  color: white;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logo {
  height: 40px;
  width: auto;
}

.btn-home, .btn-login, .btn-logout {
  background: none;
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 4px;
  color: white;
  padding: 0.5rem 1rem;
  margin-left: 1rem;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-home:hover, .btn-login:hover, .btn-logout:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.login-modal {
  max-width: 400px;
}

.login-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.btn-submit, .btn-register {
  flex: 1;
  padding: 0.8rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-submit {
  background-color: #2c3e50;
  color: white;
}

.btn-register {
  background-color: #232b36;
  color: #a3c9e2;
}

.proyectos-container {
  padding: 1rem 2rem;
  width: 100%;
}

.proyectos-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.proyectos-header h1 {
  color: #a3c9e2;
  font-size: 1.5rem;
  font-family: 'VT323', monospace;
  letter-spacing: 0.04em;
  margin: 0;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.search-box {
  position: relative;
  width: 300px;
}

.search-box input {
  width: 100%;
  padding: 0.5rem 1rem;
  padding-left: 2.5rem;
  border: 1px solid #3a4553;
  border-radius: 4px;
  background-color: #232b36;
  color: #fff;
  font-size: 0.9rem;
}

.search-box input::placeholder {
  color: #bfc9d1;
}

.search-box i {
  position: absolute;
  left: 0.8rem;
  top: 50%;
  transform: translateY(-50%);
  color: #a3c9e2;
}

.view-toggle {
  display: flex;
  border: 1px solid #3a4553;
  border-radius: 4px;
  overflow: hidden;
}

.view-toggle button {
  background: #232b36;
  border: none;
  padding: 0.5rem;
  width: 40px;
  cursor: pointer;
  color: #bfc9d1;
}

.view-toggle button.active {
  background: #a3c9e2;
  color: #101010;
}

.btn-new-project {
  background: linear-gradient(135deg, #232b36 60%, #2a3a4a 100%);
  color: #a3c9e2;
  border: 1px solid #a3c9e2;
  border-radius: 8px;
  padding: 0.5rem 1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.18s;
}

.btn-new-project:hover {
  background: #a3c9e2;
  color: #232b36;
  transform: translateY(-2px);
}

.proyectos-tools {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.filter-options select {
  padding: 0.5rem;
  border: 1px solid #3a4553;
  border-radius: 4px;
  background-color: #232b36;
  color: #fff;
}

.proyectos-stats {
  display: flex;
  gap: 1rem;
  color: #bfc9d1;
  font-size: 0.9rem;
}

.proyectos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.proyecto-card {
  background: linear-gradient(135deg, #181c22 60%, #232b36 100%);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.13);
  padding: 1.5rem;
  transition: all 0.18s;
  border: 1px solid #3a4553;
}

.proyecto-card:hover {
  box-shadow: 0 8px 16px rgba(163,201,226,0.18);
  transform: translateY(-3px);
}

.proyecto-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.proyecto-header h3 {
  margin: 0;
  font-size: 1.2rem;
  color: #a3c9e2;
}

.proyecto-actions-menu {
  position: relative;
}

.btn-menu {
  background: none;
  border: none;
  color: #a3c9e2;
  cursor: pointer;
  padding: 0.3rem;
}

.dropdown-menu {
  position: absolute;
  right: 0;
  top: 100%;
  background: #232b36;
  border: 1px solid #3a4553;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
  z-index: 10;
  min-width: 150px;
  overflow: hidden;
}

.dropdown-menu button {
  display: block;
  width: 100%;
  text-align: left;
  padding: 0.8rem 1rem;
  border: none;
  background: none;
  cursor: pointer;
  color: #fff;
  transition: background 0.2s;
}

.dropdown-menu button:hover {
  background: #2a3a4a;
  color: #a3c9e2;
}

.proyecto-desc {
  color: #bfc9d1;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  min-height: 40px;
  max-height: 60px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.proyecto-preview {
  height: 150px;
  margin-bottom: 1rem;
  border-radius: 8px;
  overflow: hidden;
  position: relative;
  border: 1px solid #3a4553;
}

.proyecto-images {
  width: 100%;
  height: 100%;
  position: relative;
}

.preview-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-count {
  position: absolute;
  bottom: 0.5rem;
  right: 0.5rem;
  background: rgba(0, 0, 0, 0.6);
  color: #a3c9e2;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
}

.no-images-preview {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: #232b36;
  color: #a3c9e2;
}

.no-images-preview i {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.proyecto-stats {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  color: #bfc9d1;
}

.proyecto-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-upload, .btn-view {
  flex: 1;
  padding: 0.7rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.18s;
}

.btn-upload {
  background-color: #232b36;
  color: #a3c9e2;
  border: 1px solid #a3c9e2;
}

.btn-upload:hover {
  background-color: #a3c9e2;
  color: #232b36;
}

.btn-view {
  background-color: #232b36;
  color: #7fff7f;
  border: 1px solid #7fff7f;
}

.btn-view:hover {
  background-color: #7fff7f;
  color: #232b36;
}

/* Vista de lista */
.proyectos-list {
  margin-bottom: 2rem;
}

.proyectos-list table {
  width: 100%;
  border-collapse: collapse;
  background: linear-gradient(135deg, #181c22 60%, #232b36 100%);
  box-shadow: 0 4px 12px rgba(0,0,0,0.13);
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid #3a4553;
}

.proyectos-list th, .proyectos-list td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #3a4553;
}

.proyectos-list th {
  background: #232b36;
  color: #a3c9e2;
  font-weight: 500;
  letter-spacing: 0.04em;
  font-family: 'VT323', monospace;
}

.proyectos-list tr:last-child td {
  border-bottom: none;
}

.project-name {
  font-weight: bold;
  color: #a3c9e2;
}

.project-description {
  color: #bfc9d1;
  max-width: 300px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.project-images-count {
  text-align: center;
  color: #bfc9d1;
}

.project-actions {
  white-space: nowrap;
}

.btn-upload-sm, .btn-view-sm, .btn-edit-sm, .btn-delete-sm {
  border: 1px solid;
  border-radius: 6px;
  width: 30px;
  height: 30px;
  display: inline-flex;
  justify-content: center;
  align-items: center;
  margin: 0 0.2rem;
  cursor: pointer;
  background: transparent;
  transition: all 0.18s;
}

.btn-upload-sm {
  color: #a3c9e2;
  border-color: #a3c9e2;
}

.btn-upload-sm:hover {
  background-color: #a3c9e2;
  color: #232b36;
}

.btn-view-sm {
  color: #7fff7f;
  border-color: #7fff7f;
}

.btn-view-sm:hover {
  background-color: #7fff7f;
  color: #232b36;
}

.btn-edit-sm {
  color: #f39c12;
  border-color: #f39c12;
}

.btn-edit-sm:hover {
  background-color: #f39c12;
  color: #232b36;
}

.btn-delete-sm {
  color: #ff7fa3;
  border-color: #ff7fa3;
}

.btn-delete-sm:hover {
  background-color: #ff7fa3;
  color: #232b36;
}

.no-projects {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  background: linear-gradient(135deg, #181c22 60%, #232b36 100%);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.13);
  text-align: center;
  border: 1px solid #3a4553;
}

.no-projects i {
  font-size: 4rem;
  color: #a3c9e2;
  margin-bottom: 1rem;
}

.no-projects p {
  color: #bfc9d1;
}

.btn-new-project-empty {
  background: linear-gradient(135deg, #232b36 60%, #2a3a4a 100%);
  color: #a3c9e2;
  border: 1px solid #a3c9e2;
  border-radius: 8px;
  padding: 0.8rem 1.5rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 1.5rem;
  transition: all 0.18s;
}

.btn-new-project-empty:hover {
  background: #a3c9e2;
  color: #232b36;
  transform: translateY(-2px);
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: linear-gradient(135deg, #232b36 60%, #1a2a3a 100%);
  border-radius: 12px;
  padding: 2rem;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  border: 1px solid #3a4553;
  box-shadow: 0 8px 32px rgba(0,0,0,0.25);
  color: #fff;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.modal-header h2 {
  margin: 0;
  color: #a3c9e2;
  font-family: 'VT323', monospace;
  letter-spacing: 0.04em;
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  color: #a3c9e2;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #a3c9e2;
}

.form-group input, .form-group textarea {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #3a4553;
  border-radius: 8px;
  font-size: 1rem;
  background: #181c22;
  color: #fff;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.8rem;
  margin-top: 1.5rem;
}

.btn-cancel, .btn-create, .btn-delete {
  padding: 0.8rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.18s;
}

.btn-cancel {
  background-color: #232b36;
  color: #a3c9e2;
  border: 1px solid #a3c9e2;
}

.btn-cancel:hover {
  background-color: #a3c9e2;
  color: #232b36;
}

.btn-create {
  background-color: #232b36;
  color: #7fff7f;
  border: 1px solid #7fff7f;
}

.btn-create:hover {
  background-color: #7fff7f;
  color: #232b36;
}

.btn-delete {
  background-color: #232b36;
  color: #ff7fa3;
  border: 1px solid #ff7fa3;
}

.btn-delete:hover {
  background-color: #ff7fa3;
  color: #232b36;
}

.delete-confirmation {
  text-align: center;
  padding: 1rem 0;
}

.delete-confirmation i {
  font-size: 3rem;
  color: #ff7fa3;
  margin-bottom: 1rem;
}

.delete-confirmation p {
  color: #bfc9d1;
}

.delete-confirmation .warning {
  color: #ff7fa3;
  font-size: 0.9rem;
  margin-top: 0.5rem;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1100;
  color: white;
}

.loading-content {
  text-align: center;
}

.loading-content i {
  font-size: 3rem;
  margin-bottom: 1rem;
  color: #a3c9e2;
}

@media (max-width: 768px) {
  .proyectos-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .header-actions {
    margin-top: 1rem;
    width: 100%;
    flex-wrap: wrap;
  }
  
  .search-box {
    width: 100%;
  }
  
  .proyectos-tools {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .proyectos-stats {
    margin-top: 0.5rem;
  }
  
  .proyectos-list th:nth-child(2), 
  .proyectos-list td:nth-child(2) {
    display: none;
  }
  
  .modal-content {
    padding: 1.5rem;
  }
}
</style> 