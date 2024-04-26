
<script setup>
//这只是一个轮播
const imag_list = ["/src/assets/img/temp/imag1.jpg",
                    "/src/assets/img/temp/imag2.jpg",
                    "/src/assets/img/temp/imag3.jpg",
                    "/src/assets/img/temp/imag4.jpg",
                    "/src/assets/img/temp/imag5.jpg"
                    ]
</script>
<template>
    <el-carousel :interval="4000" type="card" height="20rem">
      <el-carousel-item v-for="item in imag_list" :key="item">
        <!-- <h3 text="2xl" justify="center">{{ item }}</h3> -->
        <el-image  :src="item" style="width: 100%; height: 100%; margin:0" fit="cover"/>
      </el-carousel-item>
    </el-carousel>
  </template>
  
  <style scoped>
  .el-carousel{
    margin: 0 auto;
  }
  /* .el-carousel__item h3 {
    color: #475669;
    opacity: 0.75;
    line-height: 200px;
    margin: 0;
    text-align: center;
  } */
  
  .el-carousel__item:nth-child(2n) {
    background-color: ""
  }
  
  .el-carousel__item:nth-child(2n + 1) {
    background-color: ""
  }
  </style>