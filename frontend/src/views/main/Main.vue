<template>
    <div>
        <v-navigation-drawer v-model="showDrawer" :mini-variant="miniDrawer" app fixed persistent>
            <v-layout column fill-height>
                <v-list>
                    <v-subheader>Main menu</v-subheader>
                    <v-list-tile to="/main/dashboard">
                        <v-list-tile-action>
                            <v-icon>web</v-icon>
                        </v-list-tile-action>
                        <v-list-tile-content>
                            <v-list-tile-title>Dashboard</v-list-tile-title>
                        </v-list-tile-content>
                    </v-list-tile>
                    <v-list-tile to="/main/datasets">
                        <v-list-tile-action>
                            <v-icon>description</v-icon>
                        </v-list-tile-action>
                        <v-list-tile-content>
                            <v-list-tile-title>Datasets</v-list-tile-title>
                        </v-list-tile-content>
                    </v-list-tile>
                    <v-list-tile to="/main/queries">
                        <v-list-tile-action>
                            <v-icon>query_stats</v-icon>
                        </v-list-tile-action>
                        <v-list-tile-content>
                            <v-list-tile-title>Queries</v-list-tile-title>
                        </v-list-tile-content>
                    </v-list-tile>
                    <v-list-tile to="/main/accesses">
                        <v-list-tile-action>
                            <v-icon>admin_panel_settings</v-icon>
                        </v-list-tile-action>
                        <v-list-tile-content>
                            <v-list-tile-title>Accesses</v-list-tile-title>
                        </v-list-tile-content>
                    </v-list-tile>
                    <v-list-tile to="/main/profile/view">
                        <v-list-tile-action>
                            <v-icon>person</v-icon>
                        </v-list-tile-action>
                        <v-list-tile-content>
                            <v-list-tile-title>Profile</v-list-tile-title>
                        </v-list-tile-content>
                    </v-list-tile>
<!--                    <v-list-tile to="/main/profile/edit">-->
<!--                        <v-list-tile-action>-->
<!--                            <v-icon>edit</v-icon>-->
<!--                        </v-list-tile-action>-->
<!--                        <v-list-tile-content>-->
<!--                            <v-list-tile-title>Edit Profile</v-list-tile-title>-->
<!--                        </v-list-tile-content>-->
<!--                    </v-list-tile>-->
<!--                    <v-list-tile to="/main/profile/password">-->
<!--                        <v-list-tile-action>-->
<!--                            <v-icon>vpn_key</v-icon>-->
<!--                        </v-list-tile-action>-->
<!--                        <v-list-tile-content>-->
<!--                            <v-list-tile-title>Change Password</v-list-tile-title>-->
<!--                        </v-list-tile-content>-->
<!--                    </v-list-tile>-->
                </v-list>
                <v-divider></v-divider>
                <!--                <v-list v-show="hasAdminAccess" subheader>-->
                <!--                    <v-subheader>Admin</v-subheader>-->
                <!--                    <v-list-tile to="/main/admin/users/all">-->
                <!--                        <v-list-tile-action>-->
                <!--                            <v-icon>group</v-icon>-->
                <!--                        </v-list-tile-action>-->
                <!--                        <v-list-tile-content>-->
                <!--                            <v-list-tile-title>Manage Users</v-list-tile-title>-->
                <!--                        </v-list-tile-content>-->
                <!--                    </v-list-tile>-->
                <!--                    <v-list-tile to="/main/admin/users/create">-->
                <!--                        <v-list-tile-action>-->
                <!--                            <v-icon>person_add</v-icon>-->
                <!--                        </v-list-tile-action>-->
                <!--                        <v-list-tile-content>-->
                <!--                            <v-list-tile-title>Create User</v-list-tile-title>-->
                <!--                        </v-list-tile-content>-->
                <!--                    </v-list-tile>-->
                <!--                </v-list>-->
                <v-spacer></v-spacer>
                <v-list>
                    <v-list-tile @click="logout">
                        <v-list-tile-action>
                            <v-icon>close</v-icon>
                        </v-list-tile-action>
                        <v-list-tile-content>
                            <v-list-tile-title>Logout</v-list-tile-title>
                        </v-list-tile-content>
                    </v-list-tile>
                    <v-divider></v-divider>
                    <v-list-tile @click="switchMiniDrawer">
                        <v-list-tile-action>
                            <v-icon v-html="miniDrawer ? 'chevron_right' : 'chevron_left'"></v-icon>
                        </v-list-tile-action>
                        <v-list-tile-content>
                            <v-list-tile-title>Collapse</v-list-tile-title>
                        </v-list-tile-content>
                    </v-list-tile>
                </v-list>
            </v-layout>
        </v-navigation-drawer>
        <v-toolbar app color="primary" dark>
            <v-toolbar-side-icon @click.stop="switchShowDrawer"></v-toolbar-side-icon>
            <v-toolbar-title v-text="appName"></v-toolbar-title>
            <v-spacer></v-spacer>
            <v-menu bottom left offset-y>
                <v-btn slot="activator" icon>
                    <v-icon>more_vert</v-icon>
                </v-btn>
                <v-list>
                    <v-list-tile to="/main/profile">
                        <v-list-tile-content>
                            <v-list-tile-title>Profile</v-list-tile-title>
                        </v-list-tile-content>
                        <v-list-tile-action>
                            <v-icon>person</v-icon>
                        </v-list-tile-action>
                    </v-list-tile>
                    <v-list-tile @click="logout">
                        <v-list-tile-content>
                            <v-list-tile-title>Logout</v-list-tile-title>
                        </v-list-tile-content>
                        <v-list-tile-action>
                            <v-icon>close</v-icon>
                        </v-list-tile-action>
                    </v-list-tile>
                </v-list>
            </v-menu>
        </v-toolbar>
        <v-content>
            <router-view></router-view>
        </v-content>
        <v-footer app class="pa-3" fixed>
            <v-spacer></v-spacer>
            <span>&copy; {{ appName }}</span>
        </v-footer>
    </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import { appName } from '@/env';
import { dispatchUserLogOut } from '@/store/actions';
import {
  readDashboardMiniDrawer,
  readDashboardShowDrawer,
} from '@/store/getters';
import {
  commitSetDashboardMiniDrawer,
  commitSetDashboardShowDrawer,
} from '@/store/mutations';

const routeGuardMain = async (to, from, next) => {
  // if (to.path === '/main') {
  //     next('/main/dashboard');
  // } else {
  //     next();
  // }
  next();
};

@Component
export default class Main extends Vue {
  public appName = appName;

  get miniDrawer() {
    return readDashboardMiniDrawer(this.$store);
  }

  get showDrawer() {
    return readDashboardShowDrawer(this.$store);
  }

  set showDrawer(value) {
    commitSetDashboardShowDrawer(this.$store, value);
  }

  public beforeRouteEnter(to, from, next) {
    routeGuardMain(to, from, next);
  }

  public beforeRouteUpdate(to, from, next) {
    routeGuardMain(to, from, next);
  }

  public switchShowDrawer() {
    commitSetDashboardShowDrawer(
      this.$store,
      !readDashboardShowDrawer(this.$store),
    );
  }

  public switchMiniDrawer() {
    commitSetDashboardMiniDrawer(
      this.$store,
      !readDashboardMiniDrawer(this.$store),
    );
  }

  public async logout() {
    await dispatchUserLogOut(this.$store);
  }
}
</script>
