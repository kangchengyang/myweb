<script setup>
import { ref } from 'vue';
import { ElMessage } from 'element-plus'
import axios from 'axios';
import { Plus } from '@element-plus/icons-vue'
import {ErrorPicture, CloseOne} from '@icon-park/vue-next'
let value2 = ref('')
let isSearch = ref(false);
let iserro = ref(false)
const drawer = ref(false)
const textarea = ref('')
const dialogImageUrl = ref('')
const dialogVisible = ref(false)
const str_token = JSON.parse(ref(localStorage.getItem('user')).value)['Token']['access_token']
const uploadRef = ref();
const textareaValue = ref('')
const album_list = ref([]);
const loading = ref(true);

//该函数用于接口请求图片数据
let startTime = value2.value['0']
let endTime = value2.value['1']
axios.get(`http://127.0.0.1:8080/timeline?start_time=${startTime}&end_time=${endTime}`).then((response) => {
  console.log(response)
  album_list.value = response.data.data
  // console.log(response.data.data[0].image_list)
  // response.data.data[0].image_list.forEach(element => {
  //   console.log(element)
  // });
})
const searchTime = () => {
  if (value2.value == null) {
    iserro.value = true
    setTimeout(function () {
      iserro.value = false
    }, 3000)
    return
  }
  startTime = value2.value['0']
  endTime = value2.value['1']
  console.log("选择的开始时间为:", startTime, "----结束时间为:", endTime)
  if (startTime == null || endTime == null) {
    ElMessage.error('错误：请选择时间')
  } else {
    //改变搜索按钮样式
    isSearch.value = !isSearch.value;
    axios.get(`http://127.0.0.1:8080/timeline?start_time=${startTime}&end_time=${endTime}`).then((response) => {
      console.log(response)
    })
    setTimeout(function () {
      isSearch.value = false;
    }, 3000)
  }
}
const fileList = ref([])


const finish_success = () => {
  console.log(str_token)
  console.log(textareaValue.value)
  uploadRef.value.submit()
}

function handleRemove() {

}
function handlePictureCardPreview() {

}

async function file_success(response) {
  if (response.code == 2000) {
    console.log('上传成功');
    const time = response.data['time']
    const file_path = response.data['file_path']
    console.log(time)
    album_list.value[time]['image_list'].push(file_path)
    drawer.value = false
  }
}
function file_error() {
  ElMessage.error('上传失败！')
}
async function load_function(image) {
  console.log(image);
}

</script>

<template>
  <div class="timelien-left">
    <!--时间选择-->
    <div style="display: flex;">
      <div class="demo-datetime-picker">
        <div class="block" style="display: flex;">
          <div><span class="select-time-text">时间:</span></div>
          <el-date-picker v-model="value2" type="datetimerange" start-placeholder="开始时间" end-placeholder="结束时间"
            format="YYYY-MM-DD" value-format="YYYY-MM-DD" />
          <el-button type="primary" :disabled=isSearch style="margin-left: 0.8rem; width:5.2rem; outline: none;"
            @click="searchTime">
            <el-icon v-if="!isSearch" style="vertical-align: middle">
              <Search />
              <span style="vertical-align: middle"> 搜索 </span>
            </el-icon>
            <el-icon v-else class="is-loading">
              <Loading />
            </el-icon>
          </el-button>
        </div>
      </div>
      <div class="upload_albums_butn">
        <el-button type="primary" style="margin-left: 16px" @click="drawer = true">
          <el-icon>
            <upload />
          </el-icon>
          <span> 上传 </span>
        </el-button>
        <el-drawer v-model="drawer" title="上传图片" :with-header="false" size="35%">
          <div class="upload_albums">
            <el-upload ref="uploadRef" v-model:file-list="fileList" list-type="picture-card"
              :on-preview="handlePictureCardPreview" action="http://127.0.0.1:8080/upload"
              :headers="{ 'token': str_token }" :data="{ 'desc': textareaValue }" :on-remove="handleRemove"
              :multiple="true" :auto-upload="false" :on-success="file_success" :on-error="file_error">
              <el-icon>
                <Plus />
              </el-icon>
            </el-upload>
            <el-dialog v-model="dialogVisible">
              <img w-full :src="dialogImageUrl" alt="Preview Image" />
            </el-dialog>
          </div>
          <el-input v-model="textareaValue" :rows="2" type="textarea" placeholder="图片描述" />
          <div class="finish" style="margin-top: 0.8rem; display: flex; justify-content: center;">
            <el-button @click="finish_success" type="success" round>完成</el-button>
          </div>
        </el-drawer>
      </div>
    </div>
    <!--时间线-->
    <div style="display: flex; justify-content: space-evenly;">
      <el-timeline style="width:85rem;">
        <el-timeline-item v-for="item in album_list" :timestamp="item.time" placement="top">
          <el-card>
            <el-text tag="i">{{ item.desc }}</el-text>
            <!--旧版 <el-image v-for="image,index in item.image_list" :src="image" style="width: 4rem; height: 4rem;"
              :preview-src-list="item.image_list" :initial-index="index" /> -->
            <div class="album" style="z-index: 100;">
              <el-image v-for="image, index in item.image_list" :src="image" style="width: 16%; height: 16%;"
                :preview-src-list="item.image_list" :initial-index="index" lazy>
                <template #placeholder>
                  <el-skeleton animated style="width: 100%">
                    <template #template>
                      <el-skeleton-item variant="image" style="width: 100%; height: 113px;" />
                    </template>
                  </el-skeleton>
                </template>
                <template #error>
                  <div class="image-slot">
                    <error-picture theme="outline" size="36" fill="#888888" />
                  </div>
                </template>
              </el-image>
                <!-- 注意：如果您想要图片预览功能，您可能需要一个不同的解决方案 -->
            </div>
          </el-card>
        </el-timeline-item>
      </el-timeline>
    </div>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter,
.fade-leave-to

/* .fade-leave-active 在 Vue 2.1.8 或更高版本中 */
  {
  opacity: 0;
}




/**以下是实现图片自动布局 */
.album {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  flex-direction: row;
}


/* 如果需要更精细的控制，可以添加媒体查询（Media Queries）来适应不同屏幕尺寸 */
/* 例如，在小屏幕上缩小图片的最大宽度 */
/**@media (max-width: 600px) {  
  .album-image {  
    max-width: 50%; /* 在小屏幕上，每行最多显示两个图片 */
/* }  
} */


.upload_albums_butn {
  display: flex;
  justify-content: flex-end;
  align-content: flex-end;
  margin-left: -20rem;
  align-items: center;
}



.select-erro-time {
  text-align: center;
  display: flex;
  justify-content: space-evenly;
}

.timelien-left {
  position: static;
}

.select-time-text {
  color: white;
  font-weight: bold;
  margin-right: 0.8rem;
  font-size: 1.2rem;
}

.demo-datetime-picker {
  display: flex;
  width: 100%;
  padding: 0;
  flex-wrap: wrap;
  justify-content: space-around;
  align-items: stretch;
}

.demo-datetime-picker .block {
  padding: 30px 0;
  text-align: center;
}

:deep(.el-image-viewer__close) {
  background-color: var(--el-text-color-regular);
  border-color: #fff;
  color: #fff;
  font-size: 24px;
  height: 44px;
  width: 44px;
  left: 92rem;
  top: 6.8rem;
}
:deep(.el-image >img) {
  height: 113px !important;
}
.image-slot {
  display: flex;
  justify-content: center;
  height: 113px;
  align-items: center;
  background: #f7f7f7;
}
:deep(img.el-image-viewer__img) {
    height: 70% !important;
}
</style>