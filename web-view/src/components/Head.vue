<script setup>
import { store } from "/src/stores/counter.js"
import { UserFilled } from '@element-plus/icons-vue'
import { ref } from "vue";
import { useRouter } from "vue-router";
// const username = ref()
// console.log(store.username)
// username.value = store.username
const isclick = ref(false);
const router = useRouter();
function usernameOnlick(){
	isclick.value=!isclick.value;
	router.push("/login")
	localStorage.clear();
	store.islogin = false
}
</script>
<template>
<!----------------------------------------------------------------------
NAVBAR (remove topnav if you don't want changed nav background on scroll)
------------------------------------------------------------------------>
<el-affix>
<nav class="topnav navbar navbar-expand-lg navbar-dark bg-primary fixed-top" style="position:none; background: none;">
<div class="container-fluid">
	<a class="navbar-brand" href="/"><i class="fas fa-anchor mr-2"></i><strong>K C Y</strong>  web</a>
	<button class="navbar-toggler collapsed" type="button" data-toggle="collapse" data-target="#navbarColor02" aria-controls="navbarColor02" aria-expanded="false" aria-label="Toggle navigation">
	<span class="navbar-toggler-icon"></span>
	</button>
	<div class="navbar-collapse collapse" id="navbarColor02" style="">
		<ul class="navbar-nav mr-auto d-flex align-items-center">
			<li class="nav-item">
			<a class="nav-link" @click="router.push('timeline')" style="cursor: pointer">时间线</a>
			</li>
			<li class="nav-item dropdown">
			<a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
			Examples </a>
			<div class="dropdown-menu" aria-labelledby="navbarDropdown">
				<a class="dropdown-item" href="./landing.html">Home Landing</a>
				<a class="dropdown-item" href="./login.html">User Login</a>
				<a class="dropdown-item" href="./blog.html">Blog Index</a>
				<a class="dropdown-item" href="./page.html">Sample Page</a>
			</div>
			</li>
			<li class="nav-item">
			<a class="nav-link" href="./docs.html">Docs</a>
			</li>
		</ul>
		<ul class="navbar-nav ml-auto d-flex align-items-center">
			<li class="nav-item">
				<el-dropdown>
					<span class="nav-link" href="#" style="width: 8rem; outline: none;">
							<a class="btn btn-info btn-round shadow-sm" href="#" data-toggle="modal" data-target="#modal_newsletter" style="display: flex; width: 100%; padding: 0; align-items: center;" @click="usernameOnlick">
								<div class="demo-type">
									<div style="height: 40px;">
										<el-avatar src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png" fit="fill"/>
									</div>
								</div>

								<span>
									&nbsp;
									&nbsp;
								{{store.username}}
								</span>
							</a>
						</span>
					<template #dropdown>
						<el-dropdown-menu>
						<el-dropdown-item>个人中心</el-dropdown-item>
						<el-dropdown-item>账号设置</el-dropdown-item>
						<el-dropdown-item>意见反馈</el-dropdown-item>
						</el-dropdown-menu>
					</template>
				</el-dropdown>
			</li>
		</ul>
	</div>
</div>
</nav>
</el-affix>
<!-- End Navbar -->
</template>
<style scoped>
	.demo-type {
	display: flex;
	}
	.demo-type > div {
	flex: 1;
	text-align: center;
	}

	.demo-type > div:not(:last-child) {
	border-right: 1px solid var(--el-border-color);
	}
	.shadow_sm_active{
		justify-content: flex-end;
		background-color: rgb(173, 171, 171);
	}
	.dispaly_name{
		display: none;
	}
	.fixed-top {
    position: static !important;
	}
	.bg-primary {
    background:none !important;
	}
	.navbar-light .navbar-brand {
    color: #fff ;
	}
	.navbar-dark .navbar-nav .nav-link {
    color: rgba(255, 255, 255, 0.85);
	}
</style>

