<template>
  <div id="app" class="my-theme">
<!--    <HeaderComponent></HeaderComponent>-->
    <div class="flex">
      <NavComponent class="">
      </NavComponent>
      <router-view class="w-full h-screen overflow-auto"/>
    </div>
  </div>
</template>

<style>
@import 'styles.css';

/* fontawesome */
@import 'assets/css/all.css';

@font-face {
  font-family: 'Fantasque';
  src: url("fonts/fantasque/fantasquesansmono-regular.otf") format('truetype')
}

@font-face {
  font-family: 'Inter';
  src: url("fonts/inter/Inter-Regular.ttf") format('truetype')
}

@font-face {
  font-family: 'Inter';
  src: url("fonts/inter/Inter-Bold.ttf") format('truetype');
  font-weight: bold;
}

* {
  font-family: 'Inter', 'Fantasque', serif;
  font-size: 18px;
  /*-webkit-user-select: none; !* Safari *!*/
  /*-moz-user-select: none; !* Firefox *!*/
  /*-ms-user-select: none; !* IE10+/Edge *!*/
  /*user-select: none; !* Standard *!*/
}

#app {
  margin: 0;

}
</style>
<script>
// import HeaderComponent from './components/HeaderComponent.vue';
import NavComponent from "./components/NavComponent";

export default {
  components: {
    // HeaderComponent,
    NavComponent
  },
  mounted() {
    let recaptchaScript = document.createElement('script')
    recaptchaScript.setAttribute('src', 'https://friconix.com/cdn/friconix.js')
    document.head.appendChild(recaptchaScript)
  },
};
</script>
