<template>
    <router-view></router-view>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

@Component
export default class Datasets extends Vue {
  public beforeRouteEnter(to, from, next) {
    next();
  }

  public beforeRouteUpdate(to, from, next) {
    next();
  }
}
</script>

