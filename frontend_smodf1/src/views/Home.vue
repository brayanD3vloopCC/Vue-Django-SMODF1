<!-- SModf1 pagina principal -->
<!-- alter: Brayan ronaldo -->
<!-- fecha: 04 mayo 2025 -->

<template>
  <div class="home">
    <NavBar />
    <section class="hero decorated-hero">
      <pre class="ascii-art ascii-black">
███████╗    ███╗   ███╗     ██████╗     ██████╗      ███████╗ ██╗
██╔════╝    ████╗ ████║    ██╔═══██╗    ██╔══██╗     ██╔════╝███║
███████╗    ██╔████╔██║    ██║   ██║    ██║  ██║     █████╗  ╚██║
╚════██║    ██║╚██╔╝██║    ██║   ██║    ██║  ██║     ██╔══╝   ██║
███████║    ██║ ╚═╝ ██║    ╚██████╔╝    ██████╔╝     ██║      ██║
╚══════╝    ╚═╝     ╚═╝     ╚═════╝     ╚═════╝      ╚═╝      ╚═╝
      </pre>
      <div class="ascii-underline"></div>
      <img src="@/assets/smodlogotype.jpg" alt="Logo" class="main-logo" />
      <h1 class="main-title hero-black">SMOD F1</h1>
      <h3 class="main-subtitle hero-black">Visión Artificial Web</h3>
      <p class="retro-subtitle hero-black">Sistema de versiones de modelos SMOD</p>
      <div class="hero-buttons">
        <button class="retro-button primary" @click="$router.push('/login')">
          <i class="fas fa-rocket"></i>
          Comenzar
        </button>
        <button class="retro-button secondary" @click="$router.push('/docusmodf1')">
          <i class="fas fa-book"></i>
          Documentación
        </button>
      </div>
    </section>



    <section class="analysis-section decorated-section">
      <div class="analysis-container">
        <!-- Sistema de modelos SMOD -->
        <div class="analysis-card analysis-card-unique tarjeta-analisis-imagen">
          <h2 class="main-title">Procesamiento de Imágenes SMOD</h2>
          <br>
          <i class="fas fa-image"></i>
          <h3>Sistema de Modelos de Visión</h3>
          <p>Con la identificacion de los metadatos de las imagen para que el Modelo SMODF1 mediante la referencia de analisis de data sheets pueda de detectar objetos, personas o escenas con precisión.</p>
          <div class="analysis-features">
            <span><i class="fas fa-tag"></i> Etiquetado automático</span>
            <span><i class="fas fa-tag"></i> Procesamiento de Referencia</span>
            <span><i class="fas fa-search"></i> Detección de objetos</span>
            <span><i class="fas fa-palette"></i> Análisis en tonalidades B/W</span>
          </div>
          <button class="retro-button primary" :disabled="!isLoggedIn">
            <i class="fas fa-upload"></i>
            Subir imagen
          </button>
          <p v-if="!isLoggedIn" class="login-required">Inicia sesión para acceder</p>
        </div>

        <!-- Análisis en tiempo real -->
        <div class="analysis-card analysis-realtime-unique tarjeta-analisis-tiempo-real">
          <h2 class="main-title">Visión Artificial Procesada</h2>
          <br>
          <i class="fas fa-camera"></i>
          <h3>Captura de Imagenes Identificando Objetos</h3>
          <p>Utiliza tu cámara web o móvil para identificar objetos en tiempo real (la camara no debe de tener ruido) con el algoritmo de identificacion de visión artificial.</p>
          <div class="analysis-features">
            <span><i class="fas fa-bolt"></i> Procesamiento instantáneo</span>
            <span><i class="fas fa-mobile-alt"></i> Analsis dependiente al Harware utilizable</span>
            <span><i class="fas fa-desktop"></i> Funciona con webcam - port Android</span>
          </div>
          <button class="retro-button primary" :disabled="!isLoggedIn">
            <i class="fas fa-video"></i>
            Activar cámara
          </button>
          <p v-if="!isLoggedIn" class="login-required">Inicia sesión para acceder</p>
        </div>

        <!-- Conversión 3D -->
        <div class="conversion-card conversion-card-unique tarjeta-conversion-3d">
          <h2 class="main-title">Modelado 3D Inteligente</h2>
          <br>
          <i class="fas fa-cube"></i>
          <h3>Reconstrucción 3D desde Imágenes</h3>
          <p>Transformacion de tus proyectos mediante los modelos MD2D-Analisis y DataSHeets de metadatos de imagenes a un modelo 3D tridimensionales interactivos utilizando el contenedor SMODF1.</p>
          <div class="conversion-details">
            <p>El rendimiento depende de tu hardware:</p>
            <ul class="hardware-requirements">
              <li><i class="fas fa-microchip"></i> <strong>CPU:</strong> Reconstrucción en calidad Media (Aceptable)</li>
              <li><i class="fas fa-microchip"></i> <strong>GPU dedicada:</strong> Reconstrucción en alta calidad</li>
              <li><i class="fas fa-laptop"></i> <strong>Dispositivos estándar:</strong> Reconstrucción optimizada</li>
              <li><i class="fas fa-mobile-alt"></i> <strong>Dispositivos móviles:</strong> Reconstrucción básica</li>
            </ul>
          </div>
          <button class="retro-button primary" :disabled="!isLoggedIn">
            <i class="fas fa-magic"></i>
            Convertir a 3D
          </button>
          <p v-if="!isLoggedIn" class="login-required">Inicia sesión para acceder</p>
        </div>
      </div>
    </section>

    <section class="datasheets-section decorated-section">
      <div class="datasheets-container">
        <!-- DataSheets -->
        <div class="datasheets-card datasheets-card-unique tarjeta-datasheets">
          <h2 class="main-title">Generación de DataSheets</h2>
          <br>
          <i class="fas fa-file-alt"></i>
          <h3>Procesamiento de Metadatos</h3>
          <p>Mediante data Jsons construtores de los metadatos del analisis de imagenes2D el contenedor genera de cada imagen dependiente de las dimenciones de cada IMG extraida, los modelos de visión artificial pendiente al desarrollo.</p>
          <div class="datasheets-features">
            <div class="datasheets-feature">
              <i class="fas fa-chart-bar"></i>
              <div>
                <h4>Algoritmos de Procesamiento</h4>
                <p>el modelo aplica para la extraccion de datos aplicando antes de construir los datos para el procesamiento 2D</p>
              </div>
            </div>
            <div class="datasheets-feature">
              <i class="fas fa-project-diagram"></i>
              <div>
                <h4>Arquitectura del Modelo</h4>
                <p>Documentación construida de la estructura y parámetros</p>
              </div>
            </div>
          </div>
          <button class="retro-button primary" :disabled="!isLoggedIn">
            <i class="fas fa-file-export"></i>
            Generar DataSheet
          </button>
          <p v-if="!isLoggedIn" class="login-required">Inicia sesión para acceder</p>
        </div>

        <!-- Referencia -->
        <div class="reference-card reference-card-unique tarjeta-referencia">
          <h2 class="main-title">Sistema de Referencias</h2>
          <br>
          <i class="fas fa-fingerprint"></i>
          <h3>Comparación de Imágenes</h3>
          <p>Compara mediante los bases de datos existentes de las imágenes con los de la biblioteca de referencia para identificar similitudes y diferencias con precisión.</p>
          <div class="reference-steps">
            <div class="reference-step">
              <span class="step-number">1</span>
              <p>Crea tu biblioteca de imágenes de referencia</p>
            </div>
            <div class="reference-step">
              <span class="step-number">2</span>
              <p>Sube una nueva imagen para comparar</p>
            </div>
            <div class="reference-step">
              <span class="step-number">3</span>
              <p>Obtén resultados detallados de similitud</p>
            </div>
          </div>
          <div class="reference-buttons">
            <button class="retro-button secondary" :disabled="!isLoggedIn">
              <i class="fas fa-plus-circle"></i>
              Añadir referencia
            </button>
            <button class="retro-button primary" :disabled="!isLoggedIn">
              <i class="fas fa-search"></i>
              Buscar coincidencias
            </button>
          </div>
          <p v-if="!isLoggedIn" class="login-required">Inicia sesión para acceder</p>
        </div>
      </div>
    </section>

    <section id="features" class="features decorated-section">
      <div class="feature-card decorated-card">
        <i class="fas fa-camera-retro"></i>
        <h3>Visión artificial distribuida</h3>
        <p>Análisis avanzado de imágenes en tiempo real</p>
      </div>
      <div class="feature-card decorated-card">
        <i class="fas fa-cube"></i>
        <h3>Reconstrucción 3D</h3>
        <p>Modelado tridimensional de objetos y espacios</p>
      </div>
      <div class="feature-card decorated-card">
        <i class="fas fa-brain"></i>
        <h3>DataSheets Patrones de Modelos</h3>
        <p>DataSheets de modelos de Informacion para análisis predictivo</p>
      </div>
    </section>

    <!-- ROADMAP SECTIONS VERTICAL -->
    <div class="roadmap">
      <div class="roadmap-line"></div>
      <div class="roadmap-step sobre">
        <div class="roadmap-icon"><i class="fa fa-info-circle"></i></div>
        <div class="roadmap-card roadmap-card-corner-shadow">
          <div class="roadmap-card-content">
            <div class="roadmap-card-text">
              <h2>Sobre SMOD</h2>
              <h4 class="subtitle">¿Qué es SMOD?</h4>
              <p>SMOD (Sistema de Modelos de Visión Artificial Distribuida) es una plataforma integral para la gestión, versionado y despliegue de modelos de visión artificial. Permite a empresas y desarrolladores organizar, probar y actualizar modelos de IA de manera segura y eficiente.</p>
              <ul>
                <li><i class="fa fa-check"></i> Control de versiones para modelos pre construidos.</li>
                <li><i class="fa fa-check"></i> Integración sencilla con sistemas existentes.</li>
                <li><i class="fa fa-check"></i> Seguridad y trazabilidad en cada actualización.</li>
              </ul>
            </div>
            <div class="roadmap-card-img">
              <img src="../assets/smodlogotype.jpg" alt="Sobre SMOD" />
            </div>
          </div>
        </div>
      </div>
      <div class="roadmap-step aplicaciones">
        <div class="roadmap-icon"><i class="fa fa-cogs"></i></div>
        <div class="roadmap-card roadmap-card-corner-shadow">
          <div class="roadmap-card-content">
            <div class="roadmap-card-text">
              <h2>Aplicaciones</h2>
              <h4 class="subtitle">SMOD MODELO DE VERSIONES F1</h4>
              <p>El sistema de Modelos SMOD funciona como contenedor de modelos en las versiones dependientes aplicando a cada seccion pendiente al proceso de identificacion mediante el contenido generado.</p>
              <ul>
                <li><i class="fa fa-industry"></i> <b>DataSHEETS:</b> modelos de referencias mediante metadatos en tablas de secciones compuestas de acceso</li>
                <li><i class="fa fa-user-secret"></i> <b>Reconocimiento Identificado 2D:</b> Esta seccion se compone mejor si tiene datos referentes que alimentan al modelo pre construido pendiente a una solida composicion </li>
                <li><i class="fa fa-cube"></i> <b>Reconstrucción 3D:</b> modelado de Objetos aplicados al renderizado pendiente al Hardware,la arquitectura del objeto se compone segun contenga mas datos que lo alimenten y referencie a modelos avanzados.</li>
                <li><i class="fa fa-video-camera"></i> <b>Monitoreo de seguridad:</b> análisis inteligente de video para prevención de incidentes.</li>
              </ul>
              <p>Internamente, SMOD mantiene compatibilidad WEB para alcanzar resultados pendientes al harware aun suficiente para la disponibilidad de memoria del navegador.</p>
            </div>
            <div class="roadmap-card-img">
              <img src="https://images.unsplash.com/photo-1464983953574-0892a716854b?auto=format&fit=crop&w=400&q=80" alt="Aplicaciones SMOD" />
            </div>
          </div>
        </div>
      </div>
      <div class="roadmap-step beneficios">
        <div class="roadmap-icon"><i class="fa fa-star"></i></div>
        <div class="roadmap-card roadmap-card-corner-shadow">
          <div class="roadmap-card-content">
            <div class="roadmap-card-text">
              <h2>Beneficios</h2>
              <h4 class="subtitle">Sistema MMODF1</h4>
              <ul>
                <li><i class="fa fa-plug"></i> <b>Proyectos en Almacen:</b>Componene almacen en gestion compresa de datos extraibles mas basicos.</li>
                <li><i class="fa fa-shield"></i> <b>Versionado seguro:</b> historial completo de cambios y restauración de versiones anteriores.</li>
                <li><i class="fa fa-desktop"></i> <b>Interfaz intuitiva:</b> panel web moderno y personalizable.</li>
                <li><i class="fa fa-brain"></i> <b>Soporte avanzado:</b> compatible con modelos de IA de última generación y frameworks populares.</li>
                <li><i class="fa fa-rocket"></i> <b>Escalabilidad:</b> despliegue en la nube, on-premise o híbrido.</li>
              </ul>
              <p>SMOD reduce costos operativos, acelera la innovación y mejora la calidad de los procesos automatizados.</p>
            </div>
            <div class="roadmap-card-img">
              <img src="https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=400&q=80" alt="Beneficios SMOD" />
            </div>
          </div>
        </div>
      </div>
      <div class="roadmap-step comparacion">
        <div class="roadmap-icon"><i class="fa fa-cube"></i></div>
        <div class="roadmap-card roadmap-card-corner-shadow">
          <div class="roadmap-card-content">
            <div class="roadmap-card-text">
              <h2>Imagen vs 3D</h2>
              <h4 class="subtitle">Comparativa visual</h4>
              <div class="compare-flex">
                <div class="compare-img-placeholder">
                  <span>Imagen Original</span>
                  <svg width="180" height="180" viewBox="0 0 180 180">
                    <circle cx="90" cy="90" r="80" fill="#fff" />
                  </svg>
                </div>
                <div class="compare-3d-placeholder" ref="smod3d">
                  <span>Reconstrucción 3D</span>
                </div>
              </div>
              <p style="text-align:center;font-size:1.15rem;max-width:600px;margin:0 auto;">La plataforma SMOD permite comparar visualmente los resultados de modelos 2D y 3D, facilitando la validación y mejora continua de los algoritmos de visión artificial.</p>
            </div>
          </div>
        </div>
      </div>
      <div class="roadmap-step comparacion-cubo">
        <div class="roadmap-icon"><i class="fa fa-cube"></i></div>
        <div class="roadmap-card roadmap-card-corner-shadow">
          <div class="roadmap-card-content">
            <div class="roadmap-card-text">
              <h2>Cubo</h2>
              <h4 class="subtitle">Comparativa 2D vs 3D</h4>
              <div class="compare-flex">
                <div class="compare-img-placeholder">
                  <span>Cubo 2D</span>
                  <svg width="180" height="180" viewBox="0 0 180 180">
                    <rect x="30" y="30" width="120" height="120" fill="#fff" stroke="#a3c9e2" stroke-width="6" rx="18" />
                  </svg>
                </div>
                <div class="compare-3d-placeholder" ref="cube3d">
                  <span>Cubo 3D</span>
                </div>
              </div>
              <p style="text-align:center;font-size:1.15rem;max-width:600px;margin:0 auto;">Visualiza la diferencia entre un cubo plano y su representación tridimensional interactiva.</p>
            </div>
          </div>
        </div>
      </div>
      <div class="roadmap-step comparacion-triangulo">
        <div class="roadmap-icon"><i class="fa fa-play"></i></div>
        <div class="roadmap-card roadmap-card-corner-shadow">
          <div class="roadmap-card-content">
            <div class="roadmap-card-text">
              <h2>Triángulo</h2>
              <h4 class="subtitle">Comparativa 2D vs 3D</h4>
              <div class="compare-flex">
                <div class="compare-img-placeholder">
                  <span>Triángulo 2D</span>
                  <svg width="180" height="180" viewBox="0 0 180 180">
                    <polygon points="90,30 150,150 30,150" fill="#fff" stroke="#a3c9e2" stroke-width="6" />
                  </svg>
                </div>
                <div class="compare-3d-placeholder" ref="triangulo3d">
                  <span>Tetraedro 3D</span>
                </div>
              </div>
              <p style="text-align:center;font-size:1.15rem;max-width:600px;margin:0 auto;">Compara un triángulo plano con su versión 3D: un tetraedro interactivo.</p>
            </div>
          </div>
        </div>
      </div>
      <div class="roadmap-step comparacion-pentagono">
        <div class="roadmap-icon"><i class="fa fa-stop"></i></div>
        <div class="roadmap-card roadmap-card-corner-shadow">
          <div class="roadmap-card-content">
            <div class="roadmap-card-text">
              <h2>Pentágono</h2>
              <h4 class="subtitle">Comparativa 2D vs 3D</h4>
              <div class="compare-flex">
                <div class="compare-img-placeholder">
                  <span>Pentágono 2D</span>
                  <svg width="180" height="180" viewBox="0 0 180 180">
                    <polygon points="90,30 162,78 132,162 48,162 18,78" fill="#fff" stroke="#a3c9e2" stroke-width="6" />
                  </svg>
                </div>
                <div class="compare-3d-placeholder" ref="pentagono3d">
                  <span>Prisma Pentagonal 3D</span>
                </div>
              </div>
              <p style="text-align:center;font-size:1.15rem;max-width:600px;margin:0 auto;">Observa la diferencia entre un pentágono plano y un prisma pentagonal 3D interactivo.</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <footer class="smod-footer elegant-footer">
      <div class="footer-container">
        <div class="footer-main-row">
          <div class="footer-brand-col">
            <img src="@/assets/smodlogotype.jpg" alt="Logo SMOD F1" class="footer-logo" />
            <div class="footer-brand-text">
              <span class="footer-title">SMOD F1</span>
              <span class="footer-lema">Visión artificial distribuida para el futuro</span>
            </div>
          </div>
          <div class="footer-links-col">
            <h4>Navegación</h4>
            <ul>
              <li><a href="#features"><i class="fa fa-camera-retro"></i> Características</a></li>
              <li><a href="#"><i class="fa fa-book"></i> Documentación</a></li>
              <li><a href="#"><i class="fa fa-file-text"></i> Términos</a></li>
              <li><a href="#"><i class="fa fa-shield"></i> Privacidad</a></li>
            </ul>
          </div>
          <div class="footer-docs-col">
            <h4>Documentación</h4>
            <ul>
              <li><a href="#"><i class="fa fa-file-pdf-o"></i> Guía de Usuario</a></li>
              <li><a href="#"><i class="fa fa-code"></i> API</a></li>
              <li><a href="#"><i class="fa fa-graduation-cap"></i> Tutoriales</a></li>
              <li><a href="#"><i class="fa fa-question-circle"></i> FAQ</a></li>
            </ul>
          </div>
          <div class="footer-socials-col">
            <h4>Síguenos</h4>
            <div class="footer-socials">
              <a href="#" aria-label="Twitter" class="footer-social-link"><i class="fa fa-x"></i></a>
              
              <a href="#" aria-label="Documentacion" class="footer-social-link"><i class="fa fa-book"></i></a>
              <a href="#" aria-label="YouTube" class="footer-social-link"><i class="fa fa-youtube-play"></i></a>
              <a href="#" aria-label="LinkedIn" class="footer-social-link"><i class="fa fa-linkedin"></i></a>
              <a href="#" aria-label="GitHub" class="footer-social-link"><i class="fa fa-github"></i></a>
              
            </div>
          </div>
        </div>
        <div class="footer-bottom-row">
          <span>© 2025 SMOD F1. Todos los derechos reservados.</span>
          <span>Desarrollado por R0TS</span>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';

export default {
  name: 'HomeView',
  components: {
    NavBar
  },
  data() {
    return {
      smod3dResources: [],
      resizeListeners: [],
      isLoggedIn: false
    };
  },
  methods: {
    isMobile() {
      return window.innerWidth <= 900;
    },
    init3DViewer(refName, geometryFactory) {
      const container = this.$refs[refName];
      if (!container) return;

      const getDims = () => {
        if (this.isMobile()) return { w: 180, h: 180, camPos: [2, 2, 4] };
        return { w: 320, h: 320, camPos: [2, 2, 3] };
      };

      let { w, h, camPos } = getDims();
      const scene = new THREE.Scene();
      scene.background = new THREE.Color(0x181c22);
      const camera = new THREE.PerspectiveCamera(45, w / h, 0.1, 1000);
      camera.position.set(...camPos);
      const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
      renderer.setSize(w, h);
      container.appendChild(renderer.domElement);

      const light = new THREE.PointLight(0xffffff, 1);
      light.position.set(5, 5, 5);
      scene.add(light);

      const mesh = geometryFactory(this.isMobile());
      scene.add(mesh);

      const controls = new OrbitControls(camera, renderer.domElement);
      controls.enableDamping = true;
      controls.dampingFactor = 0.08;
      controls.enablePan = false;
      controls.minDistance = 2;
      controls.maxDistance = 8;

      const animate = () => {
        controls.update();
        renderer.render(scene, camera);
        requestAnimationFrame(animate);
      };
      animate();

      const resizeListener = () => {
        ({ w, h, camPos } = getDims());
        camera.aspect = w / h;
        camera.position.set(...camPos);
        camera.updateProjectionMatrix();
        renderer.setSize(w, h);
      };
      window.addEventListener('resize', resizeListener);

      this.smod3dResources.push({ renderer, controls, container });
      this.resizeListeners.push(resizeListener);
    }
  },
  mounted() {
    this.isLoggedIn = !!localStorage.getItem('usuario_smodf1');
    
    // Inicializar visualizadores 3D
    this.init3DViewer('smod3d', (mobile) => {
      const geometry = new THREE.SphereGeometry(1.5, mobile ? 16 : 32, mobile ? 16 : 32);
      const material = new THREE.MeshBasicMaterial({ color: 0xffffff, wireframe: true });
      return new THREE.Mesh(geometry, material);
    });

    this.init3DViewer('cube3d', (mobile) => {
      const geometry = new THREE.BoxGeometry(1.5, 1.5, 1.5, mobile ? 1 : 2, mobile ? 1 : 2, mobile ? 1 : 2);
      const material = new THREE.MeshBasicMaterial({ color: 0xffffff, wireframe: true });
      return new THREE.Mesh(geometry, material);
    });

    this.init3DViewer('triangulo3d', (mobile) => {
      const size = mobile ? 1.1 : 1.5;
      const geometry = new THREE.TetrahedronGeometry(size);
      const material = new THREE.MeshBasicMaterial({ color: 0xffffff, wireframe: true });
      return new THREE.Mesh(geometry, material);
    });

    this.init3DViewer('pentagono3d', (mobile) => {
      const shape = new THREE.Shape();
      const radius = mobile ? 1.0 : 1.2;
      for (let i = 0; i < 5; i++) {
        const angle = (i / 5) * Math.PI * 2 - Math.PI / 2;
        const x = Math.cos(angle) * radius;
        const y = Math.sin(angle) * radius;
        if (i === 0) shape.moveTo(x, y);
        else shape.lineTo(x, y);
      }
      shape.closePath();
      const extrudeSettings = { depth: mobile ? 1.0 : 1.5, bevelEnabled: false };
      const geometry = new THREE.ExtrudeGeometry(shape, extrudeSettings);
      const material = new THREE.MeshBasicMaterial({ color: 0xffffff, wireframe: true });
      return new THREE.Mesh(geometry, material);
    });
  },
  beforeUnmount() {
    this.resizeListeners.forEach(listener => {
      window.removeEventListener('resize', listener);
    });
    this.smod3dResources.forEach(({ renderer, container }) => {
      if (renderer && renderer.domElement && container) {
        if (container.contains(renderer.domElement)) {
          container.removeChild(renderer.domElement);
        }
        if (renderer.dispose) renderer.dispose();
      }
    });
    this.resizeListeners = [];
    this.smod3dResources = [];
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
@import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');

/* Agregar al inicio del <style> */
:root {
  --main-bg: #101010;
  --main-text: #ffffff;
  --accent-celeste: #a3c9e2;
}

/* Agregar la animación faltante */
@keyframes iconPulse {
  from {
    transform: scale(1);
    box-shadow: 0 0 0 rgba(163, 201, 226, 0.4);
  }
  to {
    transform: scale(1.1);
    box-shadow: 0 0 20px rgba(163, 201, 226, 0.8);
  }
}

.home {
  min-height: 100vh;
  background: var(--main-bg);
  color: var(--main-text);
  font-family: 'Share Tech Mono', monospace;
  margin: 0;
  padding: 0;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
  overflow-x: hidden;
}

.navbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 64px;
  background: #000;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 40px;
  z-index: 1000;
  box-shadow: 0 2px 12px rgba(0,0,0,0.18);
  border-bottom: 2px solid var(--accent-celeste);
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
  color: var(--accent-celeste);
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
  font-size: 1.5rem;
  font-family: 'Share Tech Mono', monospace;
  transition: color 0.2s;
  padding: 6px 0;
  border-bottom: 2px solid transparent;
}
.nav-link.active,
.nav-link:hover {
  color: var(--accent-celeste);
  border-bottom: 2px solid var(--accent-celeste);
}

.decorated-hero {
  background: linear-gradient(180deg, #fff 80%, #f3f7fa 100%);
  color: #101010;
  border-radius: 0 0 24px 24px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.08);
  margin-bottom: 40px;
  margin-top: 64px;
  padding: 32px 0;
  text-align: center;
  position: relative;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
  overflow-x: hidden;
  padding-left: 0;
  padding-right: 0;
}

.ascii-art.ascii-black {
  font-family: 'Share Tech Mono', monospace;
  font-size: 1.5rem;
  color: #101010;
  background: none;
  text-align: center;
  padding: 32px 0;
  line-height: 1.05;
  letter-spacing: 0.04em;
  white-space: pre;
  user-select: text;
}

.ascii-underline {
  width: 60%;
  height: 4px;
  
  margin: 0 auto 18px auto;
  border-radius: 2px;
  
}

.hero-black {
  color: #101010 !important;
  letter-spacing: 0.04em;
  text-shadow: 1px 1px 4px #a3c9e244;
}

.main-logo {
  width: 90px;
  margin: 0 auto 18px auto;
  display: block;
  border-radius: 8px;
}

.main-title, .main-subtitle, .retro-subtitle, .hero-black {
  font-family: 'VT323', monospace !important;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.main-title {
  font-size: 3.2rem;
  color: #000000;
  margin-bottom: 16px;
  text-align: center;
  letter-spacing: 0.04em;
  line-height: 1.1;
  text-shadow: 1px 2px 6px #00000033, 0 2px 8px #a3c9e244;
}

.main-subtitle {
  font-size: 1.5rem;
  color: #a3c9e2;
  margin-bottom: 12px;
  text-align: center;
  letter-spacing: 0.03em;
  line-height: 1.15;
  text-shadow: 1px 1px 4px #00000022;
}

.retro-subtitle {
  font-size: 1.1rem;
  color: #e0e0e0;
  margin-bottom: 28px;
  text-align: center;
  letter-spacing: 0.02em;
  line-height: 1.18;
  text-shadow: 1px 1px 2px #00000011;
}

.hero-black {
  color: #101010 !important;
  letter-spacing: 0.02em;
  text-shadow: 1px 1px 2px #a3c9e222;
}

.hero-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 24px;
}

.retro-button {
  padding: 12px 28px;
  border: 2px solid #a3c9e2;
  background: #a3c9e2;
  color: #101010;
  font-family: 'Share Tech Mono', monospace;
  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.2s;
  border-radius: 8px;
  font-weight: bold;
  box-shadow: 0 2px 8px rgba(163,201,226,0.08);
}
.retro-button.primary {
  background: #a3c9e2;
  color: #101010;
}
.retro-button.secondary {
  background: #fff;
  color: #101010;
  border: 2px solid #a3c9e2;
}
.retro-button:hover {
  background: #101010;
  color: #a3c9e2;
  border-color: #fff;
}

.decorated-section {
  background: #fff;
  color: #101010;
  border-radius: 24px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.18), 0 1.5px 0 var(--accent-celeste);
  padding: 48px 5vw 32px 5vw;
  display: flex;
  justify-content: center;
  gap: 32px;
}

.decorated-card, .roadmap-card {
  background: #101010;
  color: #fff;
  border: 3px solid var(--accent-celeste);
  border-radius: 38px;
  padding: 48px 36px;
  min-width: 280px;
  max-width: 420px;
  text-align: center;
  position: relative;
  overflow: hidden;
  opacity: 1;
  transform: perspective(800px) rotateY(0deg) scale(1);
}
.decorated-card *, .roadmap-card * {
  color: #fff !important;
}
.decorated-card:hover, .roadmap-card:hover {
  border-color: #fff;
  background: #181c22;
}
.decorated-card i, .roadmap-icon {
  font-size: 2.8rem;
  color: var(--accent-celeste);
  margin-bottom: 18px;
  padding: 18px;
  border-radius: 50%;
  background: #101010;
  box-shadow: 0 4px 24px #a3c9e288;
  transition: all 0.4s;
  display: inline-block;
  margin-right: 24px;
}
.decorated-card:hover i, .roadmap-card:hover .roadmap-icon {
  background: #222;
  color: #fff;
  box-shadow: 0 0 32px #a3c9e2cc;
  transform: scale(1.1) rotate(10deg);
}
.decorated-card h3 {
  
  font-size: 1.4rem;
  color: var(--accent-celeste);
  margin-bottom: 12px;
  position: relative;
  display: inline-block;
  transition: all 0.3s ease;
}
.decorated-card:hover h3 {
  color: #fff;
  text-shadow: 0 0 12px rgba(163, 201, 226, 0.8), 0 0 20px rgba(163, 201, 226, 0.4);
  transform: scale(1.05);
}
.decorated-card:hover h3:after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 0;
  width: 100%;
  height: 2px;
  background: #fff;
  animation: slideIn 0.3s forwards;
}
.decorated-card p {
  color: #444;
  font-size: 1rem;
  transition: all 0.3s ease;
  position: relative;
  z-index: 1;
}
.decorated-card:hover p {
  color: #f0f0f0;
  transform: translateY(2px);
}
@keyframes slideIn {
  from { transform: scaleX(0); }
  to { transform: scaleX(1); }
}

/* Ocultar scrollbar pero mantener funcionalidad */
.home::-webkit-scrollbar {
  width: 0 !important;
  background: transparent;
}

.home {
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE and Edge */
}

/* Asegurar que el contenedor principal no tenga overflow visible */
.features {
  overflow: hidden;
}

/* Prevenir scroll horizontal */
html, body {
  max-width: 100%;
  overflow-x: hidden;
}

/* Asegura que el contenido no quede debajo del navbar fijo */
.hero {
  margin-top: 64px;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
  overflow-x: hidden;
  padding-left: 0;
  padding-right: 0;
}

/* NUEVAS SECCIONES Y FOOTER */
.smod-section {
  background: #101010;
  color: #fff;
  border: 2.5px solid var(--accent-celeste);
  border-radius: 18px;
  margin: 32px auto;
  padding: 36px 6vw;
  max-width: 900px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.18);
  font-size: 1.15rem;
  display: flex;
  align-items: center;
  gap: 32px;
}
.smod-section.zigzag.reverse {
  flex-direction: row-reverse;
}
.smod-icon {
  flex: 0 0 90px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.smod-content {
  flex: 1;
}
.smod-section h2 {
  color: var(--accent-celeste);
  margin-bottom: 18px;
  font-size: 2rem;
}
.smod-section ul {
  padding-left: 24px;
}
.smod-link {
  color: var(--accent-celeste);
  text-decoration: underline;
  margin-right: 12px;
}
.smod-socials a {
  margin-right: 10px;
  font-size: 1.5rem;
}
/* Sección comparación Imagen vs 3D */
.compare-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 48px;
}
.compare-col {
  flex: 1;
  text-align: center;
}
.compare-img-placeholder, .compare-3d-placeholder {
  background: #181c22;
  border: 4px solid var(--accent-celeste);
  border-radius: 32px;
  width: 260px;
  height: 260px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  box-shadow: none;
  position: relative;
}
.compare-img-placeholder span,
.compare-3d-placeholder span {
  color: #fff;
  font-size: 1.15rem;
  margin-bottom: 12px;
  margin-top: 18px;
  text-align: center;
  width: 100%;
  display: block;
  font-family: 'VT323', monospace;
  letter-spacing: 0.04em;
}
.compare-img-placeholder svg {
  width: 180px;
  height: 180px;
  display: block;
}
/* Footer elegante y completo */
.elegant-footer {
  background: #000000;
  color: #fff;
  border-top: 2.5px solid var(--accent-celeste, #a3c9e2);
  padding: 0;
  margin-top: 64px;
  font-size: 1.1rem;
  box-shadow: 0 -2px 24px #00000033;
}
.footer-container {
  max-width: 1300px;
  margin: 0 auto;
  padding: 0 32px;
}
.footer-main-row {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: flex-start;
  gap: 32px;
  padding: 48px 0 18px 0;
  border-bottom: 1.5px solid #222c;
  flex-wrap: wrap;
}
.footer-brand-col {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 18px;
  min-width: 220px;
}
.footer-logo {
  width: 64px;
  border-radius: 10px;
  box-shadow: 0 2px 12px #a3c9e244;
}
.footer-brand-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.footer-title {
  font-size: 2.1rem;
  color: var(--accent-celeste, #a3c9e2);
  font-weight: bold;
  letter-spacing: 0.04em;
}
.footer-lema {
  font-size: 1.05rem;
  color: #e0e0e0;
  font-family: 'Share Tech Mono', monospace;
  letter-spacing: 0.02em;
}
.footer-links-col {
  min-width: 160px;
}
.footer-links-col h4 {
  color: var(--accent-celeste, #a3c9e2);
  margin-bottom: 10px;
  font-size: 1.1rem;
}
.footer-links-col ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.footer-links-col li {
  margin-bottom: 8px;
}
.footer-links-col a {
  color: #fff;
  text-decoration: none;
  border-bottom: 1.5px solid #a3c9e2;
  transition: color 0.2s, border-color 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
}
.footer-links-col a i {
  color: var(--accent-celeste, #a3c9e2);
  font-size: 1.1rem;
}
.footer-links-col a:hover {
  color: var(--accent-celeste, #a3c9e2);
  border-color: #fff;
}
.footer-docs-col {
  min-width: 200px;
}
.footer-docs-col h4 {
  color: var(--accent-celeste, #a3c9e2);
  margin-bottom: 10px;
  font-size: 1.1rem;
}
.footer-docs-col ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.footer-docs-col li {
  margin-bottom: 8px;
}
.footer-docs-col a {
  color: #fff;
  text-decoration: none;
  border-bottom: 1.5px solid #a3c9e2;
  transition: color 0.2s, border-color 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
}
.footer-docs-col a i {
  color: var(--accent-celeste, #a3c9e2);
  font-size: 1.1rem;
}
.footer-docs-col a:hover {
  color: var(--accent-celeste, #a3c9e2);
  border-color: #fff;
}
.footer-socials-col {
  min-width: 160px;
}
.footer-socials-col h4 {
  color: var(--accent-celeste, #a3c9e2);
  margin-bottom: 10px;
  font-size: 1.1rem;
}
.footer-socials {
  display: flex;
  flex-direction: row;
  gap: 18px;
  margin-top: 4px;
}
.footer-social-link {
  color: #fff;
  font-size: 2.1rem;
  transition: color 0.2s, transform 0.2s;
  border-radius: 50%;
  padding: 6px;
  background: #181c22;
  box-shadow: 0 2px 8px #a3c9e244;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.footer-social-link:hover {
  color: var(--accent-celeste, #a3c9e2);
  background: #fff;
  transform: scale(1.13) rotate(-8deg);
}
.footer-bottom-row {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  padding: 18px 0 12px 0;
  color: #e0e0e0;
  font-size: 1rem;
  letter-spacing: 0.04em;
  gap: 12px;
}

/* ROADMAP VERTICAL MODERNO */
.roadmap {
  position: relative;
  max-width: 1600px;
  margin: 0 auto;
  padding: 0 4vw 64px 4vw;
  display: block;
}
.roadmap-line {
  position: absolute;
  left: 50%;
  top: 0;
  width: 6px;
  height: 100%;
  background: linear-gradient(180deg, var(--accent-celeste), #222 80%);
  transform: translateX(-50%);
  z-index: 0;
  border-radius: 8px;
}
.roadmap-step {
  position: relative;
  width: 70%;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-bottom: 100px;
  z-index: 1;
  margin-left: auto;
  margin-right: auto;
}
.roadmap-icon {
  width: 90px;
  height: 90px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.8rem;
  margin-bottom: 18px;
  box-shadow: none;
  border: 4px solid var(--accent-celeste);
  background: #101010;
  color: var(--accent-celeste);
  transition: box-shadow 0.3s, background 0.3s, color 0.3s;
}
.roadmap-step.sobre .roadmap-icon {
  background: linear-gradient(135deg, #101010 60%, #1a2a3a 100%);
  color: #a3c9e2;
  border-color: #a3c9e2;
}
.roadmap-step.aplicaciones .roadmap-icon {
  background: linear-gradient(135deg, #101010 60%, #2a1a3a 100%);
  color: #ffb347;
  border-color: #ffb347;
}
.roadmap-step.beneficios .roadmap-icon {
  background: linear-gradient(135deg, #101010 60%, #1a3a2a 100%);
  color: #7fff7f;
  border-color: #7fff7f;
}
.roadmap-step.comparacion .roadmap-icon {
  background: linear-gradient(135deg, #101010 60%, #3a1a2a 100%);
  color: #ff7fa3;
  border-color: #ff7fa3;
}

.roadmap-step.cubo .roadmap-card {
  border-color: #ff7fa3;
  background: linear-gradient(120deg, #101010 80%, #3a1a2a 100%);
}

.roadmap-step.triangulo .roadmap-card {
  border-color: #ff7fa3;
  background: linear-gradient(120deg, #101010 80%, #3a1a2a 100%);
}

.roadmap-step.pentagono .roadmap-card {
  border-color: #ff7fa3;
  background: linear-gradient(120deg, #101010 80%, #3a1a2a 100%);
}
.roadmap-card h2 {
  color: #fff;
  font-size: 2rem;
  margin-bottom: 12px;
  letter-spacing: 0.04em;
  font-family: 'VT323', monospace;
}
.roadmap-card ul, .roadmap-card p {
  color: #fff;
  margin-bottom: 8px;
  font-size: 1.08rem;
}
.roadmap-card li {
  margin-bottom: 8px;
  position: relative;
  padding-left: 28px;
  font-size: 1.08rem;
  color: #fff;
}
.roadmap-card li i {
  position: absolute;
  left: 0;
  top: 2px;
  color: var(--accent-celeste);
  font-size: 1.2rem;
  transition: color 0.3s, text-shadow 0.3s;
}
.roadmap-step.sobre .roadmap-card li i { color: #a3c9e2; }
.roadmap-step.aplicaciones .roadmap-card li i { color: #ffb347; }
.roadmap-step.beneficios .roadmap-card li i { color: #7fff7f; }
.roadmap-step.comparacion .roadmap-card li i { color: #ff7fa3; }
.roadmap-step.cubo .roadmap-card li i { color: #ff7fa3; }
.roadmap-step.triangulo .roadmap-card li i { color: #ff7fa3; }
.roadmap-step.pentagono .roadmap-card li i { color: #ff7fa3; }
.roadmap-card:hover {
  border-color: #fff;
  background: #181c22;
}
.roadmap-step .roadmap-icon {
  animation: iconPulse 2.5s infinite alternate;
}
@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.roadmap-card-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 32px;
  justify-content: center;
  padding: 0 24px;
}
.roadmap-card-text {
  flex: 2;
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
}
.roadmap-card-text h2 {
  margin-bottom: 16px;
  text-align: center;
}
.roadmap-card-text .subtitle {
  margin-bottom: 24px;
  text-align: center;
  font-size: 1.2rem;
  color: #a3c9e2;
}
.roadmap-card-text p {
  margin-bottom: 20px;
  line-height: 1.6;
  text-align: justify;
}
.roadmap-card-text ul {
  margin: 24px 0;
  padding-left: 24px;
}
.roadmap-card-text li {
  margin-bottom: 12px;
  line-height: 1.5;
}
.roadmap-step.comparacion .compare-flex,
.roadmap-step.comparacion-cubo .compare-flex,
.roadmap-step.comparacion-triangulo .compare-flex,
.roadmap-step.comparacion-pentagono .compare-flex {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 48px;
  margin: 32px auto;
  max-width: 900px;
  width: 100%;
  min-height: 320px;
}
.roadmap-step.comparacion .compare-img-placeholder,
.roadmap-step.comparacion .compare-3d-placeholder,
.roadmap-step.comparacion-cubo .compare-img-placeholder,
.roadmap-step.comparacion-cubo .compare-3d-placeholder,
.roadmap-step.comparacion-triangulo .compare-img-placeholder,
.roadmap-step.comparacion-triangulo .compare-3d-placeholder,
.roadmap-step.comparacion-pentagono .compare-img-placeholder,
.roadmap-step.comparacion-pentagono .compare-3d-placeholder {
  flex: 1;
  min-width: 260px;
  max-width: 320px;
  height: 320px;
  min-height: 320px;
  background: #0b0d0f;
  border-radius: 32px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  margin: 0;
  box-shadow: none !important;
}
.roadmap-step.comparacion .compare-img-placeholder span,
.roadmap-step.comparacion .compare-3d-placeholder span,
.roadmap-step.comparacion-cubo .compare-img-placeholder span,
.roadmap-step.comparacion-cubo .compare-3d-placeholder span,
.roadmap-step.comparacion-triangulo .compare-img-placeholder span,
.roadmap-step.comparacion-triangulo .compare-3d-placeholder span,
.roadmap-step.comparacion-pentagono .compare-img-placeholder span,
.roadmap-step.comparacion-pentagono .compare-3d-placeholder span {
  position: static;
  margin-bottom: 12px;
  margin-top: 0;
}
.roadmap-step.comparacion .compare-img-placeholder svg,
.roadmap-step.comparacion .compare-3d-placeholder svg,
.roadmap-step.comparacion-cubo .compare-img-placeholder svg,
.roadmap-step.comparacion-cubo .compare-3d-placeholder svg,
.roadmap-step.comparacion-triangulo .compare-img-placeholder svg,
.roadmap-step.comparacion-triangulo .compare-3d-placeholder svg,
.roadmap-step.comparacion-pentagono .compare-img-placeholder svg,
.roadmap-step.comparacion-pentagono .compare-3d-placeholder svg {
  margin-top: 0 !important;
  align-self: center;
  display: block;
}
.roadmap-step.comparacion .compare-img-placeholder,
.roadmap-step.comparacion .compare-3d-placeholder,
.roadmap-step.comparacion-cubo .compare-img-placeholder,
.roadmap-step.comparacion-cubo .compare-3d-placeholder,
.roadmap-step.comparacion-triangulo .compare-img-placeholder,
.roadmap-step.comparacion-triangulo .compare-3d-placeholder,
.roadmap-step.comparacion-pentagono .compare-img-placeholder,
.roadmap-step.comparacion-pentagono .compare-3d-placeholder {
  box-shadow: none !important;
}

/* Eliminar pseudoelementos ::after para puntos/glows */
.roadmap-step.sobre .roadmap-card::after,
.roadmap-step.aplicaciones .roadmap-card::after,
.roadmap-step.beneficios .roadmap-card::after,
.roadmap-step.comparacion .roadmap-card::after,
.roadmap-step.comparacion-cubo .roadmap-card::after,
.roadmap-step.comparacion-triangulo .roadmap-card::after,
.roadmap-step.comparacion-pentagono .roadmap-card::after {
  display: none !important;
}

/* Borde y glow del color correspondiente para cada roadmap-card */
.roadmap-step.sobre .roadmap-card {
  border: 4px solid #a3c9e2;
  box-shadow: 0 0 24px 0 #a3c9e288;
}
.roadmap-step.aplicaciones .roadmap-card {
  border: 4px solid #ffb347;
  box-shadow: 0 0 24px 0 #ffb34788;
}
.roadmap-step.beneficios .roadmap-card {
  border: 4px solid #7fff7f;
  box-shadow: 0 0 24px 0 #7fff7f88;
}
.roadmap-step.comparacion .roadmap-card,
.roadmap-step.comparacion-cubo .roadmap-card,
.roadmap-step.comparacion-triangulo .roadmap-card,
.roadmap-step.comparacion-pentagono .roadmap-card {
  border: 4px solid #7f96ff;
  box-shadow: 0 0 24px 0 #857fff88;
}

/* ROADMAP VERTICAL - VERSIÓN DESKTOP */
@media (min-width: 901px) {
  .roadmap {
    max-width: 1600px;
    margin: 0 auto;
    padding: 0 4vw 64px 4vw;
    display: block;
  }

  .roadmap-step {
    width: 70%;
    margin-bottom: 100px;
    align-items: center;
    margin-left: auto;
    margin-right: auto;
    flex-direction: column;
    text-align: center;
  }

  /* Eliminar alternancia zigzag */
  .roadmap-step:nth-child(odd),
  .roadmap-step:nth-child(even) {
    padding-left: 0;
    padding-right: 0;
    flex-direction: column;
    text-align: center;
  }

  .roadmap-card {
    max-width: 1100px;
    width: 100%;
    margin: 0 auto;
  }

  .roadmap-card-content {
    flex-direction: row;
    gap: 40px;
    padding: 0;
  }

  .roadmap-card-text {
    flex: 1;
    text-align: left;
  }

  .roadmap-card-img {
    flex: 0 0 300px;
  }

  .roadmap-card-img img {
    width: 100%;
    height: auto;
    border-radius: 12px;
  }

  .roadmap-step.comparacion .compare-flex,
  .roadmap-step.comparacion-cubo .compare-flex {
    flex-direction: row;
    gap: 60px;
  }
}

/* Ajustes para mantener versión móvil */
@media (max-width: 900px) {
  .roadmap-card-content {
    flex-direction: column;
  }
  
  .roadmap-card-img {
    max-width: 100%;
  }
}

/* Mejoras generales de layout */
.roadmap-card-content {
  display: flex;
  gap: 20px;
  width: 100%;
}

.roadmap-card-text {
  flex: 1;
  min-width: 300px;
}

.roadmap-card-img {
  flex: 0 0 40%;
  max-width: 400px;
  position: relative;
}

/* Ajuste de la línea central */
.roadmap-line {
  background: linear-gradient(180deg, var(--accent-celeste), transparent 90%);
  height: calc(100% - 120px);
  top: 60px;
}

/* Animaciones suaves */
.roadmap-step {
  transition: all 0.3s ease;
}

@media (max-width: 900px) {
  .decorated-section {
    flex-direction: column;
    align-items: center;
    gap: 24px;
    padding: 32px 2vw 24px 2vw;
  }
  .navbar {
    padding: 0 12px;
  }
  .ascii-art {
    font-size: 1.2rem;
  }
  .main-title {
    font-size: 2.2rem;
  }
  .decorated-card i, .roadmap-icon {
    margin-right: 0 !important;
    margin-bottom: 18px !important;
  }
  .roadmap-card-content {
    flex-direction: column;
  }
  .roadmap-card-img {
    max-width: 100%;
  }
  .tarjeta-analisis-imagen,
  .tarjeta-analisis-tiempo-real,
  .tarjeta-conversion-3d,
  .tarjeta-datasheets,
  .tarjeta-referencia {
    max-width: 100%;
    padding: 32px 24px;
  }
  .tarjeta-analisis-imagen .main-title,
  .tarjeta-analisis-tiempo-real .main-title,
  .tarjeta-conversion-3d .main-title,
  .tarjeta-datasheets .main-title,
  .tarjeta-referencia .main-title {
    font-size: 2rem;
    margin-bottom: 24px;
    padding-bottom: 12px;
  }
}
@media (max-width: 1200px) {
  .roadmap-card {
    width: 95%;
    max-width: 98vw;
    padding: 32px 8px;
    min-width: unset;
  }
  .roadmap {
    max-width: 98vw;
    padding: 0 0 32px 0;
  }
}

/* ESTILOS ÚNICOS PARA CADA BLOQUE */
.analysis-card-unique {
  background: linear-gradient(135deg, #e8f4ff 60%, #c5e3ff 100%);
  border-radius: 32px;
  box-shadow: 0 4px 32px #a3c9e288;
  padding: 40px 32px 32px 32px;
  color: #101010;
  margin: 0 16px;
  max-width: 420px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.analysis-card-unique i {
  font-size: 2.8rem;
  color: #3a7ca5;
  margin-bottom: 18px;
}
.analysis-card-unique .analysis-features span {
  background: #fff;
  color: #3a7ca5;
  border-radius: 12px;
  padding: 4px 12px;
  margin: 0 4px 8px 0;
  font-size: 1rem;
  display: inline-block;
  box-shadow: 0 2px 8px #a3c9e244;
}

.analysis-realtime-unique {
  background: linear-gradient(135deg, #f0e8ff 60%, #e2d3ff 100%);
  border-radius: 32px;
  box-shadow: 0 4px 32px #b39ddb88;
  padding: 40px 32px 32px 32px;
  color: #101010;
  margin: 0 16px;
  max-width: 420px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.analysis-realtime-unique i {
  font-size: 2.8rem;
  color: #6c4fbb;
  margin-bottom: 18px;
}
.analysis-realtime-unique .analysis-features span {
  background: #fff;
  color: #6c4fbb;
  border-radius: 12px;
  padding: 4px 12px;
  margin: 0 4px 8px 0;
  font-size: 1rem;
  display: inline-block;
  box-shadow: 0 2px 8px #b39ddb44;
}

.conversion-card-unique {
  background: linear-gradient(135deg, #ffe8f4 60%, #ffd3e8 100%);
  border-radius: 32px;
  box-shadow: 0 4px 32px #ffd58088;
  padding: 40px 32px 32px 32px;
  color: #101010;
  margin: 0 16px;
  max-width: 420px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.conversion-card-unique i {
  font-size: 2.8rem;
  color: #ff9800;
  margin-bottom: 18px;
}
.conversion-card-unique .hardware-requirements li {
  background: #fff;
  color: #ff9800;
  border-radius: 12px;
  padding: 4px 12px;
  margin: 0 0 8px 0;
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 2px 8px #ffd58044;
}

.datasheets-card-unique {
  background: linear-gradient(135deg, #e8fff0 60%, #d3ffe2 100%);
  border-radius: 32px;
  box-shadow: 0 4px 32px #7fff7f88;
  padding: 40px 32px 32px 32px;
  color: #101010;
  margin: 0 16px;
  max-width: 420px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.datasheets-card-unique i {
  font-size: 2.8rem;
  color: #43a047;
  margin-bottom: 18px;
}
.datasheets-card-unique .datasheets-feature {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  background: #fff;
  border-radius: 12px;
  padding: 8px 12px;
  margin-bottom: 10px;
  box-shadow: 0 2px 8px #7fff7f22;
}
.datasheets-card-unique .datasheets-feature i {
  font-size: 1.5rem;
  color: #43a047;
  margin-top: 4px;
}

.reference-card-unique {
  background: linear-gradient(135deg, #fff0e8 60%, #ffe2d3 100%);
  border-radius: 32px;
  box-shadow: 0 4px 32px #ff7fa388;
  padding: 40px 32px 32px 32px;
  color: #101010;
  margin: 0 16px;
  max-width: 420px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.reference-card-unique i {
  font-size: 2.8rem;
  color: #d81b60;
  margin-bottom: 18px;
}
.reference-card-unique .reference-step {
  display: flex;
  align-items: center;
  gap: 12px;
  background: #fff;
  border-radius: 12px;
  padding: 8px 12px;
  margin-bottom: 10px;
  box-shadow: 0 2px 8px #ff7fa322;
}
.reference-card-unique .step-number {
  background: #d81b60;
  color: #fff;
  border-radius: 50%;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.1rem;
}

/* Estilos base para todas las tarjetas */
.tarjeta-base {
  color: #fff;
  text-align: center;
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  padding: 48px 40px;
  border-radius: 24px;
  gap: 24px;
}

.tarjeta-base i {
  font-size: 2.8rem;
  margin: 16px 0 24px;
}

.tarjeta-base h3 {
  margin: 24px 0 16px;
}

.tarjeta-base p {
  margin-bottom: 24px;
  line-height: 1.6;
}

.tarjeta-base .retro-button {
  margin-top: 32px;
}

/* Estilos específicos para cada tipo de tarjeta */
.tarjeta-analisis-imagen.tarjeta-base {
  background: linear-gradient(135deg, #101010 60%, #1a2a3a 100%);
}

.tarjeta-analisis-tiempo-real.tarjeta-base {
  background: linear-gradient(135deg, #101010 60%, #2a1a3a 100%);
}

.tarjeta-conversion-3d.tarjeta-base {
  background: linear-gradient(135deg, #101010 60%, #3a2a1a 100%);
}

.tarjeta-datasheets.tarjeta-base {
  background: linear-gradient(135deg, #101010 60%, #1a3a2a 100%);
}

.tarjeta-referencia.tarjeta-base {
  background: linear-gradient(135deg, #101010 60%, #3a1a2a 100%);
}

/* Contenedores expandidos */
.analysis-container,
.conversion-container,
.datasheets-container,
.reference-container {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  padding: 0 20px;
}

.datasheets-container,
.reference-container {
  grid-template-columns: repeat(2, 1fr);
  margin-top: 20px;
}

/* Ajustes responsive */
@media (max-width: 1200px) {
  .analysis-container,
  .conversion-container {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .analysis-container,
  .conversion-container,
  .datasheets-container,
  .reference-container {
    grid-template-columns: 1fr;
  }
}

/* Estilos para títulos principales dentro de las tarjetas */
.tarjeta-analisis-imagen .main-title,
.tarjeta-analisis-tiempo-real .main-title,
.tarjeta-conversion-3d .main-title,
.tarjeta-datasheets .main-title,
.tarjeta-referencia .main-title {
  font-size: 2.4rem;
  color: #fff;
  margin-bottom: 32px;
  padding-bottom: 16px;
  border-bottom: 2px solid;
  width: 100%;
  text-align: center;
  font-family: 'VT323', monospace;
  letter-spacing: 0.04em;
  text-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

.tarjeta-analisis-imagen .main-title {
  border-bottom-color: #a3c9e2;
}

.tarjeta-analisis-tiempo-real .main-title {
  border-bottom-color: #b39ddb;
}

.tarjeta-conversion-3d .main-title {
  border-bottom-color: #ffd580;
}

.tarjeta-datasheets .main-title {
  border-bottom-color: #7fff7f;
}

.tarjeta-referencia .main-title {
  color: #000000;
  font-size: 1.8rem;
  margin-bottom: 1rem;
}

/* Ajuste del espaciado general de las tarjetas */
.tarjeta-analisis-imagen,
.tarjeta-analisis-tiempo-real,
.tarjeta-conversion-3d,
.tarjeta-datasheets,
.tarjeta-referencia {
  padding: 48px 40px;
  gap: 24px;
}

/* Ajuste del espaciado entre elementos */
.tarjeta-analisis-imagen h3,
.tarjeta-analisis-tiempo-real h3,
.tarjeta-conversion-3d h3,
.tarjeta-datasheets h3,
.tarjeta-referencia h3 {
  margin-top: 24px;
  margin-bottom: 16px;
}

/* Ajuste del espaciado para los iconos */
.tarjeta-analisis-imagen i,
.tarjeta-analisis-tiempo-real i,
.tarjeta-conversion-3d i,
.tarjeta-datasheets i,
.tarjeta-referencia i {
  margin-top: 16px;
  margin-bottom: 24px;
}

/* Ajuste del espaciado para los párrafos */
.tarjeta-analisis-imagen p,
.tarjeta-analisis-tiempo-real p,
.tarjeta-conversion-3d p,
.tarjeta-datasheets p,
.tarjeta-referencia p {
  margin-bottom: 24px;
  line-height: 1.6;
}

/* Ajuste del espaciado para los botones */
.tarjeta-analisis-imagen .retro-button,
.tarjeta-analisis-tiempo-real .retro-button,
.tarjeta-conversion-3d .retro-button,
.tarjeta-datasheets .retro-button,
.tarjeta-referencia .retro-button {
  margin-top: 32px;
}

/* Ajuste responsive */
@media (max-width: 900px) {
  .tarjeta-analisis-imagen .main-title,
  .tarjeta-analisis-tiempo-real .main-title,
  .tarjeta-conversion-3d .main-title,
  .tarjeta-datasheets .main-title,
  .tarjeta-referencia .main-title {
    font-size: 2rem;
    margin-bottom: 24px;
    padding-bottom: 12px;
  }
  
  .tarjeta-analisis-imagen,
  .tarjeta-analisis-tiempo-real,
  .tarjeta-conversion-3d,
  .tarjeta-datasheets,
  .tarjeta-referencia {
    padding: 32px 24px;
    gap: 16px;
  }
}

/* Asegurar que los títulos sean negros */
.main-title {
  color: #000000 !important;
  font-weight: bold;
}

.analysis-card-unique .main-title,
.analysis-realtime-unique .main-title,
.conversion-card-unique .main-title,
.datasheets-card-unique .main-title,
.reference-card-unique .main-title {
  color: #000000 !important;
  font-weight: bold;
  font-size: 2.2rem;
  margin-bottom: 1rem;
}

.analysis-card-unique h3,
.analysis-realtime-unique h3,
.conversion-card-unique h3,
.datasheets-card-unique h3,
.reference-card-unique h3 {
  color: #000000;
  font-size: 1.6rem;
  margin-top: 1rem;
}
</style>
  