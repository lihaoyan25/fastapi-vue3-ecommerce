import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/user'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/auth/Login.vue'),
    meta: { guest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/auth/Register.vue'),
    meta: { guest: true }
  },
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/product/:id',
    name: 'ProductDetail',
    component: () => import('../views/ProductDetail.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/cart',
    name: 'Cart',
    component: () => import('../views/Cart.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/Profile.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/admin/products',
    name: 'ProductManage',
    component: () => import('../views/admin/ProductManage.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0, behavior: 'smooth' }
  }
})

// 全局路由守卫
router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore()

  // 游客页，已登录跳首页
  if (to.meta.guest && userStore.isLoggedIn) {
    return next('/')
  }

  // 需要登录的页面
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    return next('/login')
  }

  // 需要管理员权限
  if (to.meta.requiresAdmin) {
    if (!userStore.userInfo) {
      try {
        await userStore.fetchUserInfo()
      } catch (e) {
        return next('/login')
      }
    }
    if (!userStore.isAdmin) {
      return next('/')
    }
  }

  // 已登录但无用户信息，自动拉取
  if (userStore.isLoggedIn && !userStore.userInfo) {
    try {
      await userStore.fetchUserInfo()
    } catch (e) {}
  }

  next()
})

export default router
