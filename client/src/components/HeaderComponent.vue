<template>
  <div id="header">
    <nav class="bg-gray-700 border-b border-gray-200  z-30 w-full">
      <div class="">
        <div class="flex items-center justify-between">
          <div class="flex items-center justify-start text-gray-200 text-xl">
            <div class=" font-bold flex items-center pr-2">
              <i class="fi-xnsuxl-tools-solid mx-2"></i>
              <span class=" whitespace-nowrap">NLPAnalyser</span>
            </div>
            <b-link to="/runs" class="header-link" router-tag="span">Runs</b-link>
            <b-link to="/sandbox" class=" header-link" router-tag="span">Sandbox</b-link>
          </div>
        </div>
      </div>
    </nav>
  </div>
</template>

<script>
export default {
  name: 'HeaderComponent',
};
</script>

<style>
#header {
  color: white;
  background-color: white;
}


</style>
