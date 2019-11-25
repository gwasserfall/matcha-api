<template>
			
	<div class="md-layout-item md-size-20">
		<md-card>
			<md-card-header>
			<div class="md-title">Your Preferences</div>
			</md-card-header>
		<md-list>

		<md-subheader>Search Radius</md-subheader>
		<md-list-item>
			<input type="range" style="width: 100%;">
			40km
		</md-list-item>

		<md-divider></md-divider>
		<md-subheader>Gender Preference</md-subheader>
		<md-list-item><md-checkbox value="male">Male</md-checkbox></md-list-item>
		<md-list-item><md-checkbox value="male">Female</md-checkbox></md-list-item>
		<md-list-item><md-checkbox value="male">Other</md-checkbox></md-list-item>

		<md-list-item>
			<md-checkbox value="" />
			<span class="md-list-item-text">Male</span>
		</md-list-item>

		<md-list-item>
			<md-checkbox value="" />
			<span class="md-list-item-text">Female</span>
		</md-list-item>

		</md-list>
		</md-card>
	</div>
</template>

<script>
export default {
  name: 'search-preferences'
}
</script>

<style>

</style>