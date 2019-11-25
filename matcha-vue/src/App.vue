<template>
  <div id="app" class="page-container">

  <md-app md-waterfall md-mode="overlap">
      <md-app-toolbar class="md-accent md-large">
        <div class="md-toolbar-row">
          <md-button class="md-icon-button" @click="menuVisible = !menuVisible">
            <md-icon>menu</md-icon>
          </md-button>

          <span class="md-title">
            <img src="@/assets/logo_white.png" alt="logo" class="logo-main">
          </span>
        </div>
      </md-app-toolbar>

      <md-app-drawer :md-active.sync="menuVisible">

        <md-list>
          <md-list-item to="/" exact>Home <code>/</code></md-list-item>
          <md-list-item to="/search" exact>Search <code>/search</code></md-list-item>

        </md-list>
      </md-app-drawer>

      <md-app-content>
        <router-view></router-view>
      </md-app-content>
    </md-app>


  </div>
</template>

<style>

.logo-main {
  height: 100px !important;
}

.md-app-content {
  margin-bottom: 70px !important;
}

</style>

<script>
export default {
  data () {
    return {
      menuVisible: false
    }
  }
}
</script>