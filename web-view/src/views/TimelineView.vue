<script setup>
import { ref } from 'vue';
import { ElMessage } from 'element-plus'
import axios from 'axios';
import { Plus } from '@element-plus/icons-vue'
let value2 = ref('')
let isSearch = ref(false);
let iserro = ref(false)
const drawer = ref(false)
const textarea = ref('')
const dialogImageUrl = ref('')
const dialogVisible = ref(false)
const formData = new FormData();
const album_list = ref([{
  "time": "2024-4-30",
  "image_list": [
    'https://fuss10.elemecdn.com/a/3f/3302e58f9a181d2509f3dc0fa68b0jpeg.jpeg',
    'https://fuss10.elemecdn.com/1/34/19aa98b1fcb2781c4fba33d850549jpeg.jpeg',
    'https://fuss10.elemecdn.com/0/6f/e35ff375812e6b0020b6b4e8f9583jpeg.jpeg',
    'https://fuss10.elemecdn.com/9/bb/e27858e973f5d7d3904835f46abbdjpeg.jpeg',
    'https://fuss10.elemecdn.com/d/e6/c4d93a3805b3ce3f323f7974e6f78jpeg.jpeg',
    'https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg',
    'https://fuss10.elemecdn.com/2/11/6535bcfb26e4c79b48ddde44f4b6fjpeg.jpeg',
  ],
  "desc": "这是一组图片描述"
}, {
  "time": "2024-4-30",
  "image_list": [
    'https://fuss10.elemecdn.com/a/3f/3302e58f9a181d2509f3dc0fa68b0jpeg.jpeg',
    'https://fuss10.elemecdn.com/1/34/19aa98b1fcb2781c4fba33d850549jpeg.jpeg',
    'https://fuss10.elemecdn.com/0/6f/e35ff375812e6b0020b6b4e8f9583jpeg.jpeg',
    'https://fuss10.elemecdn.com/9/bb/e27858e973f5d7d3904835f46abbdjpeg.jpeg',
    'https://fuss10.elemecdn.com/d/e6/c4d93a3805b3ce3f323f7974e6f78jpeg.jpeg',
    'https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg',
    'https://fuss10.elemecdn.com/2/11/6535bcfb26e4c79b48ddde44f4b6fjpeg.jpeg',
  ],
  "desc": "这是一组图片描述"
}, {
  "time": "2024-4-30",
  "image_list": [
    'https://fuss10.elemecdn.com/a/3f/3302e58f9a181d2509f3dc0fa68b0jpeg.jpeg',
    'https://fuss10.elemecdn.com/1/34/19aa98b1fcb2781c4fba33d850549jpeg.jpeg',
    'https://fuss10.elemecdn.com/0/6f/e35ff375812e6b0020b6b4e8f9583jpeg.jpeg',
    'https://fuss10.elemecdn.com/9/bb/e27858e973f5d7d3904835f46abbdjpeg.jpeg',
    'https://fuss10.elemecdn.com/d/e6/c4d93a3805b3ce3f323f7974e6f78jpeg.jpeg',
    'https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg',
    'https://fuss10.elemecdn.com/2/11/6535bcfb26e4c79b48ddde44f4b6fjpeg.jpeg',
  ],
  "desc": "这是一组图片描述"
}, {
  "time": "2024-4-30",
  "image_list": [
    'https://fuss10.elemecdn.com/a/3f/3302e58f9a181d2509f3dc0fa68b0jpeg.jpeg',
    'https://fuss10.elemecdn.com/1/34/19aa98b1fcb2781c4fba33d850549jpeg.jpeg',
    'https://fuss10.elemecdn.com/0/6f/e35ff375812e6b0020b6b4e8f9583jpeg.jpeg',
    'https://fuss10.elemecdn.com/9/bb/e27858e973f5d7d3904835f46abbdjpeg.jpeg',
    'https://fuss10.elemecdn.com/d/e6/c4d93a3805b3ce3f323f7974e6f78jpeg.jpeg',
    'https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg',
    'https://fuss10.elemecdn.com/2/11/6535bcfb26e4c79b48ddde44f4b6fjpeg.jpeg',
  ],
  "desc": "这是一组图片描述"
}]);

//该函数用于接口请求图片数据
let startTime = value2.value['0']
let endTime = value2.value['1']
axios.get(`http://127.0.0.1:8080/timeline?start_time=${startTime}&end_time=${endTime}`).then((response) => {
  console.log(response)
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

async function finish_success(){
  console.log("开始上传")

  for (const item of fileList.value){
    console.log(item.raw)
    formData.append("file",item.raw);
  }
  console.log(formData);

  axios.post('http://127.0.0.1:8080/upload',formData,{
    headers: {
    'Content-Type': 'multipart/form-data'
    }
  }).then(response=>{
    console.log(response)
  })
    
}

function handleRemove(){

}
function handlePictureCardPreview(){
  
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
            <el-upload v-model:file-list="fileList" list-type="picture-card" :on-preview="handlePictureCardPreview"
              :on-remove="handleRemove" :multiple="true" :auto-upload="false">
              <el-icon>
                <Plus />
              </el-icon>
            </el-upload>
            <el-dialog v-model="dialogVisible">
              <img w-full :src="dialogImageUrl" alt="Preview Image" />
            </el-dialog>
          </div>
          <el-input v-model="textarea" :rows="2" type="textarea" placeholder="图片描述" />
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
            <div class="album">
              <el-image v-for="image, index in item.image_list" :src="image" style="width: 16%; height: 16%;"
                :preview-src-list="item.image_list" :initial-index="index" />
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
</style>