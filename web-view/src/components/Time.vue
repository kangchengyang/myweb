<script setup>
import {onMounted, onUnmounted } from "vue";
    let  intervalId;
    function setDate() {  
        const now = new Date();  
        const secondsRatio = now.getSeconds() / 60;  
        const minutesRatio = (secondsRatio + now.getMinutes()) / 60;  
        const hoursRatio = (minutesRatio + now.getHours()) / 12;  
        const secondsDegrees = secondsRatio * 360;  
        const minutesDegrees = minutesRatio * 360;  
        const hoursDegrees = hoursRatio * 360;  
        // console.log(secondsDegrees)
        // console.log(minutesDegrees)
        // console.log(hoursDegrees)
        setTransformation('.second-hand', secondsDegrees+90);  
        setTransformation('.minute-hand', minutesDegrees+90);  
        setTransformation('.hour-hand', hoursDegrees+90);  
    }
    
    function setTransformation(element, degrees) {  
        document.querySelector(element).style.transform = `rotate(${degrees}deg)`;  
    }
    onMounted(()=>{
        setDate();  
        intervalId = setInterval(setDate, 1000);
    })
    onUnmounted(()=>{
        clearInterval(intervalId)
    })
</script>
<template>
    <div class="clock">  
        <div class="hand hour-hand"></div>  
        <div class="hand minute-hand"></div>  
        <div class="hand second-hand"></div>  
    </div> 
</template>
<style scoped>
body {  
    display: flex;  
    justify-content: center;  
    align-items: center;  
    height: 100vh;  
    margin: 0;  
    background-color: #333;  
    font-family: Arial, sans-serif;  
}  
  
.clock {  
    width: 300px;  
    height: 300px;      
    /* border: 15px solid #464858;   */
    border-radius: 50%;  
    position: relative;  
    /* background-image: url("/src/assets/img/background-imag1.jpg"); */
    top:-40rem;
}  
  
.hand {  
    width: 50%;  
    height: 6px;  
    background-color: #fff;  
    position: absolute;  
    top: 50%;   
    transform-origin: 100%;  
    transform: rotate(90deg);  
    transition: transform 0.05s;  
}  
  
.hour-hand {  
    width: 40%;
    left: 10%
}  
  
.minute-hand {  
    width: 45%;
    left: 6%;
}  
  
.second-hand {  
    width: 50%;  
    background-color: red;  
}
</style>
 