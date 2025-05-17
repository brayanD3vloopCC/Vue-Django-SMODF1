import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/Home.vue'
import SistemaView from '../views/Sistema.vue'
import LoginView from '../views/Login.vue'
import RegisterView from '../views/Register.vue'
import DashboardLayout from '../layouts/DashboardLayout.vue'
import DocuSMODF1View from '../views/DocuSMODF1.vue'
import ProjectDetail from '../views/ProjectDetail.vue'
import ProyectosView from '../views/Proyectos.vue'
import ConstructorProyecto from '../views/ConstructorProyecto.vue'
import EstudioThreeView from '../views/EstudioThree.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: { requiresAuth: false }
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView,
    meta: { requiresAuth: false }
  },
  {
    path: '/docusmodf1',
    name: 'docusmodf1',
    component: DocuSMODF1View,
    meta: { requiresAuth: false }
  },
  {
    path: '/proyectos',
    name: 'proyectos-standalone',
    component: ProyectosView,
    meta: { requiresAuth: false }
  },
  {
    path: '/proyectos/:id',
    name: 'project-detail-standalone',
    component: ProjectDetail,
    meta: { requiresAuth: false }
  },
  {
    path: '/constructorproyecto',
    name: 'constructor-proyecto',
    component: ConstructorProyecto,
    meta: { requiresAuth: true }
  },
  {
    path: '/EstudioThree',
    name: 'estudio-three-standalone',
    component: EstudioThreeView,
    meta: { requiresAuth: false }
  },
  {
    path: '/sistema',
    component: DashboardLayout,
    meta: { requiresAuth: true },
    children: [
      { path: '', name: 'sistema', component: SistemaView },
      { path: 'analisis', name: 'analisis', component: () => import('../views/Analisis.vue') },
      { path: 'proyectos', name: 'proyectos', component: () => import('../views/Proyectos.vue') },
      { path: 'proyectos/:id', name: 'project-detail', component: ProjectDetail },
      { path: 'imagenes', name: 'imagenes', component: () => import('../views/Imagenes.vue') },
      { path: 'modelos', name: 'modelos', component: () => import('../views/Modelos.vue') },
      { path: 'estudio-three', name: 'estudio-three', component: () => import('../views/EstudioThree.vue') },
      { path: 'perfil', name: 'perfil', component: () => import('../views/Perfil.vue') },
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Guard de navegación para proteger rutas
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('usuario_smodf1')
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else if ((to.path === '/login' || to.path === '/register') && isAuthenticated) {
    next('/sistema')
  } else {
    next()
  }
})

export default router
