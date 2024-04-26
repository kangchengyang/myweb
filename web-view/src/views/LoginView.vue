<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router';
import { store } from "/src/stores/counter.js"
let formData = new FormData();
const router = useRouter()
const username = ref();
const password = ref();

const login =(event)=>{
    event.preventDefault();
    formData.append("username",username.value)
    formData.append("password",password.value)
    axios.post('http://127.0.0.1:8080/login',formData).then((response)=>{
        console.log(response)
        if(response.data["code"]===2000){
            ElMessage({
                message: response.data["message"],
                type: 'success',
            })
            localStorage.setItem('user', JSON.stringify(response.data.data));
            store.username = username.value
            store.islogin = true;
            router.push("/")
            //登录成功
        }else{
            //登录失败
            ElMessage.error(response.data["message"])
        }
    })
}
</script>
<template> 
    <!-- Main -->
    <div class="d-md-flex h-md-100 align-items-center">
        <div class="col-md-6 p-0 bg-indigo h-md-100 loginarea">
            <div class="text-white d-md-flex align-items-center h-100 p-5 text-center justify-content-center">
                <div class="logoarea pt-5 pb-5">
                    <p>
                        <i class="fa fa-anchor fa-3x"></i>
                    </p>
                    <div style="width:100%; display: flex;align-items: center;">
                        <h1 class="mb-0 mt-3 display-4">K C Y </h1>
                        <i class="fab fa-sass fa-2x text-cyan" style=" margin-top: 1rem;"></i>
                    </div>
                    <h5 class="mb-4 font-weight-light">this is my web</h5>
                </div>
            </div>
        </div>
        <div class="col-md-6 p-0 bg-white h-md-100 loginarea">
            <div class="d-md-flex align-items-center h-md-100 p-5 justify-content-center">
                <form class="border rounded p-5" method="post">
                    <h3 class="mb-4 text-center">登 录</h3>
                    <div class="form-group">
                        <input type="text" v-model="username" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="user" required="">
                    </div>
                    <div class="form-group">
                        <input type="password" v-model="password" class="form-control" id="exampleInputPassword1" placeholder="Password" required="">
                    </div>
                    <div class="form-group form-check">
                        <!-- <input type="checkbox" class="form-check-input" id="exampleCheck1"> -->
                        <!-- <label class="form-check-label small text-muted" for="exampleCheck1">Remember me</label> -->
                    </div>
                    <button @click="login" class="btn btn-success btn-round btn-block shadow-sm">Sign in</button>
                    <!-- <small class="d-block mt-4 text-center"><a class="text-gray" href="#">Forgot your password?</a></small> -->
                </form>
            </div>
        </div>
    </div>
    <!-- End Main -->
    <!--咖啡-->
    <div style="position:fixed; bottom:20px;left:20px; z-index: 1111;">
        <a href="#" target="_blank"><img class="rounded-circle shadow-lg" src="/src/assets/img/demo/coffee.png" width="70" data-toggle="tooltip" data-placement="top" title="" data-original-title="Buy me a coffee!"></a>
    </div>
</template>
<style scoped>
</style>