<script setup>
import { ref } from 'vue';
import { ElMessage } from 'element-plus'
const value2 = ref('')
let isSearch = ref(false);
let iserro = ref(false)
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
const searchTime = () => {
  if (value2.value == null) {
    iserro.value = true
    setTimeout(function () {
      iserro.value = false
    }, 3000)
    return
  }
  console.log(value2.value)
  const startTime = value2.value['0']
  const endTime = value2.value['1']
  console.log("选择的开始时间为:", startTime, "----结束时间为:", endTime)
  if (startTime == null || endTime == null) {
    ElMessage.error('错误：请选择时间')
  } else {
    //改变搜索按钮样式
    isSearch.value = !isSearch.value;
    setTimeout(function () {
      isSearch.value = false;
    }, 3000)
  }
}
</script>

<template>
  <div class="timelien-left">
    <!--时间选择-->
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
    <!--时间线-->
    <div style="display: flex; justify-content: space-evenly;">
      <el-timeline style="width:85rem;">
        <el-timeline-item v-for="item in album_list" :timestamp="item.time" placement="top">
          <el-card>
            <el-text tag="i">{{ item.desc }}</el-text>
            <!--旧版 <el-image v-for="image,index in item.image_list" :src="image" style="width: 4rem; height: 4rem;"
              :preview-src-list="item.image_list" :initial-index="index" /> -->
            <div class="album">  
              <el-image v-for="image,index in item.image_list" :src="image" style="width: 16%; height: 16%;" :preview-src-list="item.image_list" :initial-index="index" />  
              <!-- 注意：如果您想要图片预览功能，您可能需要一个不同的解决方案 -->  
            </div>           
          </el-card>
        </el-timeline-item>
      </el-timeline>
    </div>
  </div>
</template>

<style scoped>

.fade-enter-active, .fade-leave-active {
	transition: opacity 0.5s;
	}
	.fade-enter, .fade-leave-to /* .fade-leave-active 在 Vue 2.1.8 或更高版本中 */ {
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