<template>
    <router-view></router-view>
</template>

<script lang="ts">
import {Component, Vue} from 'vue-property-decorator';
import {store} from '@/store';

// const routeGuarddatasets = async (to, from, next) => {
//     if (!readHasdatasetsAccess(store)) {
//         next('/main');
//     } else {
//         next();
//     }
// };

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

