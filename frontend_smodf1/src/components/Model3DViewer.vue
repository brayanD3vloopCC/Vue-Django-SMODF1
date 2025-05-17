<template>
  <div class="model-viewer" :class="{ fullscreen: isFullscreen }">
    <div class="model-container" ref="container"></div>
    
    <div class="model-controls">
      <button @click="toggleFullscreen" class="control-btn">
        <i :class="isFullscreen ? 'fas fa-compress' : 'fas fa-expand'"></i>
      </button>
      <button @click="resetView" class="control-btn">
        <i class="fas fa-sync"></i>
      </button>
      <button @click="toggleWireframe" class="control-btn">
        <i class="fas fa-border-all"></i>
      </button>
      <button @click="exportModel" class="control-btn">
        <i class="fas fa-download"></i>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Model3DViewer',
  props: {
    modelData: {
      type: Object,
      required: true
    },
    colorMode: {
      type: String,
      default: 'color'
    }
  },
  
  data() {
    return {
      scene: null,
      camera: null,
      renderer: null,
      controls: null,
      model: null,
      isFullscreen: false,
      isWireframe: false
    }
  },
  
  watch: {
    modelData: {
      handler(newData) {
        this.updateModel(newData);
      },
      deep: true
    },
    
    colorMode() {
      this.updateMaterial();
    }
  },
  
  mounted() {
    this.initScene();
    if (this.modelData) {
      this.updateModel(this.modelData);
    }
    
    window.addEventListener('resize', this.onResize);
  },
  
  beforeUnmount() {
    window.removeEventListener('resize', this.onResize);
    this.disposeScene();
  },
  
  methods: {
    initScene() {
      // Para esta implementación, simplificamos usando un canvas 2D como simulación
      // En una implementación real, usaríamos Three.js aquí
      
      const container = this.$refs.container;
      const canvas = document.createElement('canvas');
      canvas.width = container.clientWidth;
      canvas.height = container.clientHeight;
      
      container.innerHTML = '';
      container.appendChild(canvas);
      
      this.ctx = canvas.getContext('2d');
      
      // Dibujar modelo
      this.drawModel();
    },
    
    updateModel() {
      // Actualizar el modelo y redibujar
      this.drawModel();
    },
    
    drawModel() {
      if (!this.ctx) return;
      
      const canvas = this.ctx.canvas;
      
      // Limpiar canvas
      this.ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      // Fondo
      this.ctx.fillStyle = '#111';
      this.ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      // Dibujar un objeto 3D simulado (pirámide)
      this.ctx.beginPath();
      
      // Color según modo
      switch (this.colorMode) {
        case 'grayscale':
          this.ctx.fillStyle = this.isWireframe ? '#333' : '#ccc';
          this.ctx.strokeStyle = '#fff';
          break;
        case 'blueprint':
          this.ctx.fillStyle = this.isWireframe ? '#0a4d8f' : '#2389da';
          this.ctx.strokeStyle = '#56b0ff';
          break;
        case 'color':
        default:
          this.ctx.fillStyle = this.isWireframe ? '#333' : '#f0f0f0';
          this.ctx.strokeStyle = '#fff';
          break;
      }
      
      // Centro y tamaño
      const centerX = canvas.width / 2;
      const centerY = canvas.height / 2;
      const size = Math.min(canvas.width, canvas.height) * 0.4;
      
      // Dibujar cubo simple (simulado)
      if (this.isWireframe) {
        // Líneas frontales
        this.ctx.strokeRect(centerX - size/2, centerY - size/2, size, size);
        
        // Líneas traseras (simuladas con perspectiva)
        this.ctx.beginPath();
        this.ctx.moveTo(centerX - size/3, centerY - size/3);
        this.ctx.lineTo(centerX + size*2/3, centerY - size/3);
        this.ctx.lineTo(centerX + size*2/3, centerY + size*2/3);
        this.ctx.lineTo(centerX - size/3, centerY + size*2/3);
        this.ctx.closePath();
        this.ctx.stroke();
        
        // Líneas conectoras
        this.ctx.beginPath();
        this.ctx.moveTo(centerX - size/2, centerY - size/2);
        this.ctx.lineTo(centerX - size/3, centerY - size/3);
        this.ctx.moveTo(centerX + size/2, centerY - size/2);
        this.ctx.lineTo(centerX + size*2/3, centerY - size/3);
        this.ctx.moveTo(centerX + size/2, centerY + size/2);
        this.ctx.lineTo(centerX + size*2/3, centerY + size*2/3);
        this.ctx.moveTo(centerX - size/2, centerY + size/2);
        this.ctx.lineTo(centerX - size/3, centerY + size*2/3);
        this.ctx.stroke();
      } else {
        // Simulación simplificada de un modelo sólido
        // Cara frontal
        this.ctx.fillRect(centerX - size/2, centerY - size/2, size, size);
        
        // Lado derecho (simulado)
        this.ctx.beginPath();
        this.ctx.moveTo(centerX + size/2, centerY - size/2);
        this.ctx.lineTo(centerX + size*2/3, centerY - size/3);
        this.ctx.lineTo(centerX + size*2/3, centerY + size*2/3);
        this.ctx.lineTo(centerX + size/2, centerY + size/2);
        this.ctx.closePath();
        this.ctx.fillStyle = this.getDarkerColor(this.ctx.fillStyle);
        this.ctx.fill();
        
        // Lado superior (simulado)
        this.ctx.beginPath();
        this.ctx.moveTo(centerX - size/2, centerY - size/2);
        this.ctx.lineTo(centerX - size/3, centerY - size/3);
        this.ctx.lineTo(centerX + size*2/3, centerY - size/3);
        this.ctx.lineTo(centerX + size/2, centerY - size/2);
        this.ctx.closePath();
        this.ctx.fillStyle = this.getLighterColor(this.ctx.fillStyle);
        this.ctx.fill();
      }
      
      // Info de modelo
      this.ctx.fillStyle = '#fff';
      this.ctx.font = '14px Arial';
      const model = this.modelData || {};
      const vertexCount = model.vertices?.length || 0;
      this.ctx.fillText(`Vértices: ${vertexCount}`, 10, 20);
      
      if (this.isFullscreen) {
        this.ctx.fillText('Presiona ESC para salir de pantalla completa', 10, canvas.height - 20);
      }
    },
    
    getDarkerColor(color) {
      // Simplificación para este ejemplo
      return color === '#ccc' ? '#999' : 
             color === '#2389da' ? '#1a6aa9' : 
             color === '#f0f0f0' ? '#ccc' : '#444';
    },
    
    getLighterColor(color) {
      // Simplificación para este ejemplo
      return color === '#ccc' ? '#eee' : 
             color === '#2389da' ? '#56b0ff' : 
             color === '#f0f0f0' ? '#fff' : '#666';
    },
    
    toggleFullscreen() {
      this.isFullscreen = !this.isFullscreen;
      
      if (this.isFullscreen) {
        if (this.$el.requestFullscreen) {
          this.$el.requestFullscreen();
        }
      } else {
        if (document.exitFullscreen) {
          document.exitFullscreen();
        }
      }
      
      // Actualizar tamaño del canvas
      this.$nextTick(() => {
        this.onResize();
      });
    },
    
    resetView() {
      // Simulamos un reinicio de la vista
      this.drawModel();
    },
    
    toggleWireframe() {
      this.isWireframe = !this.isWireframe;
      this.drawModel();
    },
    
    exportModel() {
      // Simulamos exportación
      const json = JSON.stringify(this.modelData || {}, null, 2);
      const blob = new Blob([json], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      
      const a = document.createElement('a');
      a.href = url;
      a.download = 'model3d.json';
      a.click();
      
      URL.revokeObjectURL(url);
    },
    
    onResize() {
      if (!this.ctx) return;
      
      const container = this.$refs.container;
      const canvas = this.ctx.canvas;
      
      canvas.width = container.clientWidth;
      canvas.height = container.clientHeight;
      
      this.drawModel();
    },
    
    disposeScene() {
      // Limpiar recursos si es necesario
    }
  }
}
</script>

<style scoped>
.model-viewer {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 300px;
  background: #111;
  border-radius: 8px;
  overflow: hidden;
}

.model-container {
  width: 100%;
  height: 100%;
}

.model-controls {
  position: absolute;
  bottom: 10px;
  right: 10px;
  display: flex;
  gap: 8px;
}

.control-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.2s;
}

.control-btn:hover {
  background: rgba(30, 30, 30, 0.8);
}

.fullscreen {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 9999;
  background: #000;
  border-radius: 0;
}
</style> 