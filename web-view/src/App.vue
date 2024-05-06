<script setup>
import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router'
import Head from './components/Head.vue'
import { onMounted, ref, watch } from 'vue';
import { store } from '/src/stores/counter.js';

const user = JSON.parse(localStorage.getItem('user'));
const back_image = ref(
  {
    "home": '/src/assets/img/background-imag1.jpg',
    "timeline": "/src/assets/img/background-imag2.png"
  });
  
const route = useRoute();
const router = useRouter();
const pathname = ref();
let islogin = ref(true)
//路由跳转前执行的
router.beforeEach((to, from, next) => {
  if (to.name == "login") {
    islogin.value = false;
  } else {
    islogin.value = true;
    pathname.value = to.name;
  //   document.querySelector(".background").setAttribute("class","animate__animated  animate__fadeIn animate__delay-0.9s");
  //   setTimeout(() => {
  // }, 1000);
  //   document.querySelector(".background").removeAttribute("class","animate__animated  animate__fadeIn animate__delay-0.9s");
  }
  next();
})
</script>
<template>

  <div class="background" :style="{ 'background-image': 'url(' + back_image[pathname] + ')', height: '100%' }">
    <el-scrollbar height="100vh">
    <Head v-if="islogin"/>
    <RouterView class="animate__animated  animate__fadeIn animate__delay-0.9s"/>
    </el-scrollbar>
  </div>
</template>
<style scoped>

</style>
<!-- animate__animated  animate__fadeIn animate__delay-0.9s -->