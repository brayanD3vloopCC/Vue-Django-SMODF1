<template>
  <div class="documentation">
    <NavBar />
    <div class="doc-container">
      <aside class="doc-sidebar">
        <nav>
          <h3>Documentación SMOD F1</h3>
          <ul>
            <li><a href="#introduccion">Introducción</a></li>
            <li><a href="#instalacion">Instalación</a></li>
            <li><a href="#modelos">Modelos</a></li>
            <li><a href="#procesamiento">Procesamiento de Imágenes</a></li>
            <li><a href="#analisis">Análisis en Tiempo Real</a></li>
            <li><a href="#conversion">Conversión 3D</a></li>
            <li><a href="#datasheets">DataSheets</a></li>
            <li><a href="#api">API Reference</a></li>
          </ul>
        </nav>
      </aside>

      <main class="doc-content">
        <section id="introduccion">
          <h1>Documentación SMOD F1</h1>
          <p>Bienvenido a la documentación oficial de SMOD F1, un sistema avanzado de visión artificial para procesamiento de imágenes y modelado 3D.</p>
          
          <h2>¿Qué es SMOD F1?</h2>
          <p>SMOD F1 es una plataforma integral que combina procesamiento de imágenes, análisis en tiempo real y modelado 3D para proporcionar soluciones avanzadas de visión artificial.</p>
        </section>

        <section id="instalacion">
          <h2>Instalación</h2>
          <pre><code>
# Clonar el repositorio
git clone https://github.com/tu-usuario/smod-f1.git

# Instalar dependencias
cd smod-f1
npm install

# Iniciar el servidor de desarrollo
npm run serve
          </code></pre>
        </section>

        <section id="modelos">
          <h2>Modelos</h2>
          <p>SMOD F1 utiliza modelos de aprendizaje profundo para el análisis de imágenes y la reconstrucción 3D.</p>
          <!-- Más contenido de documentación aquí -->
        </section>

        <!-- Más secciones de documentación aquí -->
      </main>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'

export default {
  name: 'DocuSMODF1',
  components: {
    NavBar
  }
}
</script>

<style scoped>
.documentation {
  min-height: 100vh;
  background: #f8fafc;
}

.doc-container {
  display: flex;
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
  gap: 2rem;
  margin-top: 64px;
}

.doc-sidebar {
  width: 250px;
  position: sticky;
  top: 80px;
  height: calc(100vh - 80px);
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.doc-sidebar h3 {
  color: #1a202c;
  margin-bottom: 1rem;
  font-size: 1.2rem;
  font-weight: 600;
}

.doc-sidebar ul {
  list-style: none;
  padding: 0;
}

.doc-sidebar li {
  margin-bottom: 0.5rem;
}

.doc-sidebar a {
  color: #4a5568;
  text-decoration: none;
  font-size: 0.95rem;
  display: block;
  padding: 0.5rem;
  border-radius: 4px;
  transition: all 0.2s;
}

.doc-sidebar a:hover {
  background: #edf2f7;
  color: #2d3748;
}

.doc-content {
  flex: 1;
  max-width: 800px;
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.doc-content h1 {
  color: #1a202c;
  font-size: 2.5rem;
  margin-bottom: 1.5rem;
}

.doc-content h2 {
  color: #2d3748;
  font-size: 1.8rem;
  margin: 2rem 0 1rem;
}

.doc-content p {
  color: #4a5568;
  line-height: 1.7;
  margin-bottom: 1rem;
}

pre {
  background: #2d3748;
  color: #e2e8f0;
  padding: 1rem;
  border-radius: 8px;
  overflow-x: auto;
  margin: 1rem 0;
}

code {
  font-family: 'Fira Code', monospace;
}

@media (max-width: 768px) {
  .doc-container {
    flex-direction: column;
    padding: 1rem;
  }

  .doc-sidebar {
    width: 100%;
    position: static;
    height: auto;
    margin-bottom: 1rem;
  }

  .doc-content {
    padding: 1rem;
  }
}
</style> 