<template>
  <div class="perfil-view">
    <h1>Perfil de Usuario</h1>
    <form class="perfil-form" @submit.prevent="guardarPerfil">
      <div class="form-row">
        <label>Correo electrónico</label>
        <input type="email" v-model="perfil.correo" disabled />
      </div>
      <div class="form-row">
        <label>Nombre completo</label>
        <input type="text" v-model="perfil.nombre_completo" required />
      </div>
      <div class="form-row">
        <label>Nickname</label>
        <input type="text" v-model="perfil.nickname" required />
      </div>
      <div class="form-row">
        <label>Nueva contraseña</label>
        <input type="password" v-model="nuevaPassword" placeholder="Dejar en blanco para no cambiar" />
      </div>
      <div class="form-row">
        <label>Confirmar contraseña</label>
        <input type="password" v-model="confirmarPassword" placeholder="Repite la nueva contraseña" />
      </div>
      <button class="btn-guardar" type="submit">Guardar cambios</button>
      <div v-if="mensaje" :class="{'msg-ok': exito, 'msg-error': !exito}" class="msg">{{ mensaje }}</div>
    </form>
  </div>
</template>

<script>
const API_URL = process.env.VUE_APP_API_URL || 'http://localhost:8000/api/usuarios';
export default {
  name: 'PerfilView',
  data() {
    return {
      perfil: {
        correo: '',
        nombre_completo: '',
        nickname: ''
      },
      nuevaPassword: '',
      confirmarPassword: '',
      mensaje: '',
      exito: false
    }
  },
  mounted() {
    this.cargarPerfil()
  },
  methods: {
    async cargarPerfil() {
      try {
        const token = localStorage.getItem('token');
        const res = await fetch(`${API_URL}/usuario-actual/`, {
          headers: { 'Authorization': token ? `Bearer ${token}` : undefined }
        });
        if (!res.ok) throw new Error('No se pudo cargar el perfil');
        const data = await res.json();
        this.perfil = {
          correo: data.correo,
          nombre_completo: data.nombre_completo,
          nickname: data.nickname
        };
      } catch (e) {
        this.mensaje = 'Error al cargar perfil';
        this.exito = false;
      }
    },
    async guardarPerfil() {
      if (this.nuevaPassword && this.nuevaPassword !== this.confirmarPassword) {
        this.mensaje = 'Las contraseñas no coinciden';
        this.exito = false;
        return;
      }
      try {
        const token = localStorage.getItem('token');
        const body = {
          nombre_completo: this.perfil.nombre_completo,
          nickname: this.perfil.nickname
        };
        if (this.nuevaPassword) body.password = this.nuevaPassword;
        const res = await fetch(`${API_URL}/perfil/`, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': token ? `Bearer ${token}` : undefined
          },
          body: JSON.stringify(body)
        });
        if (!res.ok) throw new Error('No se pudo actualizar el perfil');
        this.mensaje = 'Perfil actualizado correctamente';
        this.exito = true;
        this.nuevaPassword = '';
        this.confirmarPassword = '';
      } catch (e) {
        this.mensaje = 'Error al actualizar perfil';
        this.exito = false;
      }
    }
  }
}
</script>

<style scoped>
.perfil-view {
  color: #fff;
  padding: 32px;
  max-width: 480px;
  margin: 0 auto;
}
.perfil-form {
  background: #232b36;
  border-radius: 16px;
  padding: 32px 24px 24px 24px;
  box-shadow: 0 2px 12px #a3c9e244;
  display: flex;
  flex-direction: column;
  gap: 18px;
}
.form-row {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.form-row label {
  color: #a3c9e2;
  font-size: 1.05rem;
  font-weight: 500;
}
.form-row input {
  background: #181c22;
  color: #fff;
  border: 1.5px solid #a3c9e2;
  border-radius: 8px;
  padding: 8px 12px;
  font-size: 1.08rem;
  outline: none;
  transition: border 0.2s;
}
.form-row input:focus {
  border: 1.5px solid #7fff7f;
}
.btn-guardar {
  background: #a3c9e2;
  color: #101010;
  border: none;
  border-radius: 8px;
  padding: 12px 0;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  margin-top: 8px;
  transition: background 0.2s, color 0.2s;
}
.btn-guardar:hover {
  background: #7fff7f;
  color: #101010;
}
.msg {
  margin-top: 10px;
  padding: 8px 0;
  border-radius: 8px;
  text-align: center;
  font-size: 1.05rem;
}
.msg-ok {
  background: #7fff7f33;
  color: #7fff7f;
}
.msg-error {
  background: #ff7fa333;
  color: #ff7fa3;
}
</style> 