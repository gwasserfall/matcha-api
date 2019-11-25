<template>
  <div class="search">
    <div class="md-layout md-gutter">
        <search-preferences></search-preferences>
        <div class="md-layout-item">
          <md-card>
            <md-card-header>
                <div class="md-title">Potential Matches</div>
              </md-card-header>
              <match-card></match-card>
          </md-card>
        </div>
      </div>
  </div>
</template>

<script>
import MatchCard from '@/components/MatchCard.vue'
import SearchPreferences from '@/components/SearchPreferences.vue'

export default {
  name: 'login',
  components: {
    MatchCard,
    SearchPreferences
  }
}
</script>

<style scoped>
  .md-checkbox {
    display: flex;
  }
</style>