import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '/src/views/LoginView.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      // component: () => import('../views/AboutView.vue')
    },{
      path:'/timeline',
      name:"timeline",
      component: () => import('/src/views/TimelineView.vue')
    }
  ]
})
router.beforeEach((to,from,next)=>{
  const user =localStorage.getItem("user");
  //根据token判断当前访问界面的路由
  if(to.name=="login"){
    if(user!=null){
      next({"path":"/"});
    }else{
      next();
    }
  }else{
    if(user!=null){
      next();
    }else{
      next({"path":"/login"});
    }
  }
})

export default router
