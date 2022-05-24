<template>
  <div>
    <div id="Main" class="xl:rounded-r  flex  h-screen bg-gray-800 flex-col divide-y divide-y-2">
      <div class="justify-start p-3 pr-4 items-center space-x-3 mx-auto border-gray-500 ">
        <div class=" font-bold text-white flex items-center text-2xl">
          <i class="fa fa-search mr-2" style="color:white"></i>
          <span class=" whitespace-nowrap text-xl">Analyser</span>
        </div>
      </div>

      <div class="flex flex-col justify-start w-full border-gray-600  pb-5">
        <b-link to="/runs" class="header-link" router-tag="span">
          <i class="fa fa-vial mr-2" style="color:white"></i>
          Runs
        </b-link>
        <b-link to="/sandbox" class="header-link" router-tag="span">
          <i class="fa fa-bug mr-2" style="color:white"></i>
          Sandbox
        </b-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HeaderComponent',
};
</script>

<style scoped>
#header {
  color: white;
  background-color: white;
}


.header-link {
  @apply cursor-pointer text-white w-auto py-2 my-0;
}

.header-link:hover {
  @apply font-black;
  @apply bg-gray-800;
}

</style>
