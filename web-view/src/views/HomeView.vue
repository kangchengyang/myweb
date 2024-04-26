<script setup>
import TheWelcome from '../components/TheWelcome.vue'
// import Carousel from '@/components/Carousel.vue';
import TestView from './TestView.vue';
import WelcomeItem from '/src/components/WelcomeItem.vue';
import Time from '/src/components/Time.vue';
import { useRouter } from 'vue-router';
  const router = useRouter()
  const user = JSON.parse(localStorage.getItem('user'));
  if(user==null){
    router.push("/login")
  }
</script>

<template>
  <div class="background-imag">
    <main class="container">
      <TestView/>
    </main>
    <WelcomeItem/>
    <Time></Time>
  </div>
  <!-- <Carousel/> -->
</template>
<style scoped>
  main{
    margin-top: 4.4rem;
    margin-right: 14rem;
  }
</style>
