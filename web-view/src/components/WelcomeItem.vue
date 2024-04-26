<script setup>

</script>
<template>
  <div class="imag-list">
    <el-card class="card-left"shadow="hover">
      <!-- <template #header>Yummy hamburger</template> -->
      <img
        src="/src/assets/img/temp/imag4.jpg"
        style="width: 100%"
      />
    </el-card>
    <el-card class="card-left"shadow="hover">
      <!-- <template #header>Yummy hamburger</template> -->
      <img
        src="/src/assets/img/temp/imag5.jpg"
        style="width: 100%"
      />
    </el-card>
    <el-card class="card-left"shadow="hover">
      <!-- <template #header>Yummy hamburger</template> -->
      <img
        src="/src/assets/img/temp/imag6.jpg"
        style="width: 100%"
      />
    </el-card> 
    <el-card class="card-left" style="max-width: 25%; margin-right: 2rem;" shadow="hover">
      <!-- <template #header>Yummy hamburger</template> -->
      <img
        src="/src/assets/img/temp/imag7.jpg"
        style="width: 100%"
      />
    </el-card>          
  </div>
</template>


<style scoped>
:deep(.el-card__body){
  padding:0.2rem;
  background-color: #0f405485;
}
.card-left{
  margin: 2rem 0 2rem 2rem;
}
.imag-list{
  display: flex;
}
.item {
  margin-top: 2rem;
  display: flex;
  position: relative;
}

.details {
  flex: 1;
  margin-left: 1rem;
}

i {
  display: flex;
  place-items: center;
  place-content: center;
  width: 32px;
  height: 32px;
  color: var(--color-text);
}

h3 {
  font-size: 1.2rem;
  font-weight: 500;
  margin-bottom: 0.4rem;
  color: var(--color-heading);
}

@media (min-width: 1024px) {
  .item {
    margin-top: 0;
    padding: 0.4rem 0 1rem calc(var(--section-gap) / 2);
  }

  i {
    top: calc(50% - 25px);
    left: -26px;
    position: absolute;
    border: 1px solid var(--color-border);
    background: var(--color-background);
    border-radius: 8px;
    width: 50px;
    height: 50px;
  }

  .item:before {
    content: ' ';
    border-left: 1px solid var(--color-border);
    position: absolute;
    left: 0;
    bottom: calc(50% + 25px);
    height: calc(50% - 25px);
  }

  .item:after {
    content: ' ';
    border-left: 1px solid var(--color-border);
    position: absolute;
    left: 0;
    top: calc(50% + 25px);
    height: calc(50% - 25px);
  }

  .item:first-of-type:before {
    display: none;
  }

  .item:last-of-type:after {
    display: none;
  }
}
</style>
