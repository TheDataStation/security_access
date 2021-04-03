<template>
    <v-container fluid>
        <v-card class="ma-3 pa-3">
            <v-card-title primary-title>
                <div class="headline primary--text">Dashboard</div>
            </v-card-title>
            <v-card-text>
                <div class="headline font-weight-light ma-5">Welcome {{ greetedUser }}</div>
            </v-card-text>
            <v-card-actions>
                <v-btn to="/main/profile/view">
                    <v-icon left>
                        web
                    </v-icon>
                    View Profile
                </v-btn>
                <v-btn to="/main/datasets/">
                    <v-icon left>
                        description
                    </v-icon>
                    View Datasets
                </v-btn>
                <v-btn to="/main/queries/">
                    <v-icon left>
                        query_stats
                    </v-icon>
                    View Queries
                </v-btn>
                <v-btn to="/main/accesses/">
                    <v-icon left>
                        admin_panel_settings
                    </v-icon>
                    View Accesses
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-container>
</template>

<script lang="ts">
import {Component, Vue} from 'vue-property-decorator';
import {readUserProfile} from '@/store/getters';

@Component
export default class Dashboard extends Vue {
    get greetedUser() {
        const userProfile = readUserProfile(this.$store);
        if (userProfile) {
            if (userProfile.full_name) {
                return userProfile.full_name;
            } else {
                return userProfile.email;
            }
        }
    }
}
</script>
