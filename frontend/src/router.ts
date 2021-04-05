import Vue from 'vue';
import Router from 'vue-router';

import RouterComponent from './components/RouterComponent.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      component: () =>
        import(/* webpackChunkName: "start" */ './views/main/Start.vue'),
      children: [
        {
          path: 'login',
          // route level code-splitting
          // this generates a separate chunk (about.[hash].js) for this route
          // which is lazy-loaded when the route is visited.
          component: () =>
            import(/* webpackChunkName: "login" */ './views/Login.vue'),
        },
        {
          path: 'recover-password',
          component: () =>
            import(
              /* webpackChunkName: "recover-password" */ './views/PasswordRecovery.vue'
            ),
        },
        {
          path: 'reset-password',
          component: () =>
            import(
              /* webpackChunkName: "reset-password" */ './views/ResetPassword.vue'
            ),
        },
        {
          path: 'main',
          component: () =>
            import(/* webpackChunkName: "main" */ './views/main/Main.vue'),
          redirect: 'main/dashboard',
          children: [
            {
              path: 'dashboard',
              component: () =>
                import(
                  /* webpackChunkName: "main-dashboard" */ './views/main/Dashboard.vue'
                ),
            },
            {
              path: 'profile',
              component: RouterComponent,
              redirect: 'profile/view',
              children: [
                {
                  path: 'view',
                  component: () =>
                    import(
                      /* webpackChunkName: "main-profile" */ './views/main/profile/UserProfile.vue'
                    ),
                },
                {
                  path: 'edit',
                  component: () =>
                    import(
                      /* webpackChunkName: "main-profile-edit" */ './views/main/profile/UserProfileEdit.vue'
                    ),
                },
                {
                  path: 'password',
                  component: () =>
                    import(
                      /* webpackChunkName: "main-profile-password" */ './views/main/profile/UserProfileEditPassword.vue'
                    ),
                },
              ],
            },
            // {
            //     path: 'admin',
            //     component: () => import(/* webpackChunkName: "main-admin" */ './views/main/admin/Admin.vue'),
            //     redirect: 'admin/users/all',
            //     children: [
            //         {
            //             path: 'users',
            //             redirect: 'users/all',
            //         },
            //         {
            //             path: 'users/all',
            //             component: () => import(
            //                 /* webpackChunkName: "main-admin-users" */ './views/main/admin/AdminUsers.vue'),
            //         },
            //         {
            //             path: 'users/edit/:id',
            //             name: 'main-admin-users-edit',
            //             component: () => import(
            //                 /* webpackChunkName: "main-admin-users-edit" */ './views/main/admin/EditUser.vue'),
            //         },
            //         {
            //             path: 'users/create',
            //             name: 'main-admin-users-create',
            //             component: () => import(
            //                 /* webpackChunkName: "main-admin-users-create" */ './views/main/admin/CreateUser.vue'),
            //         },
            //     ],
            // },
            {
              path: 'datasets',
              component: () =>
                import(
                  /* webpackChunkName: "main-datasets" */ './views/main/datasets/Datasets.vue'
                ),
              redirect: 'datasets/datasets/all',
              children: [
                {
                  path: 'datasets/all',
                  component: () =>
                    import(
                      /* webpackChunkName: "main-datasets-users" */ './views/main/datasets/ViewDatasets.vue'
                    ),
                },
                // {
                //     path: 'datasets/edit/:id',
                //     name: 'main-datasets-edit',
                //     component: () => import(
                //         /* webpackChunkName: "main-datasets-edit" */ './views/main/datasets/EditDataset.vue'),
                // },
                {
                  path: 'datasets/create',
                  name: 'main-datasets-create',
                  component: () =>
                    import(
                      /* webpackChunkName: "main-datasets-create" */ './views/main/datasets/CreateDataset.vue'
                    ),
                },
              ],
            },
            {
              path: 'queries',
              component: () =>
                import(
                  /* webpackChunkName: "main-queries" */ './views/main/queries/Queries.vue'
                ),
              redirect: 'queries/queries/all',
              children: [
                {
                  path: 'queries/all',
                  component: () =>
                    import(
                      /* webpackChunkName: "main-queries-users" */ './views/main/queries/ViewQueries.vue'
                    ),
                },
                {
                  path: 'requests/edit/:id',
                  name: 'main-queries-requests-edit',
                  component: () =>
                    import(
                      /* webpackChunkName: "main-queries-requests-edit" */ './views/main/queries/EditQueryRequestsAccess.vue'
                    ),
                },
                {
                  path: 'queries/create',
                  name: 'main-queries-create',
                  component: () =>
                    import(
                      /* webpackChunkName: "main-queries-create" */ './views/main/queries/CreateQuery.vue'
                    ),
                },
                {
                  path: 'queries/:id',
                  name: 'main-queries-view',
                  component: () =>
                    import(
                      /* webpackChunkName: "main-queries-view" */ './views/main/queries/ViewQuery.vue'
                    ),
                },
              ],
            },
            {
              path: 'accesses',
              component: () =>
                import(
                  /* webpackChunkName: "main-accesses" */ './views/main/accesses/Accesses.vue'
                ),
              redirect: 'accesses/accesses/all',
              children: [
                {
                  path: 'accesses/all',
                  component: () =>
                    import(
                      /* webpackChunkName: "main-accesses-users" */ './views/main/accesses/ViewAccesses.vue'
                    ),
                },
                {
                  path: 'accesses/edit/:id',
                  name: 'main-accesses-edit',
                  component: () =>
                    import(
                      /* webpackChunkName: "main-accesses-edit" */ './views/main/accesses/EditAccessGrant.vue'
                    ),
                },
                {
                  path: 'accesses/:id',
                  name: 'main-accesses-view',
                  component: () =>
                    import(
                      /* webpackChunkName: "main-accesses-view" */ './views/main/accesses/ViewAccessReceipt.vue'
                    ),
                },
              ],
            },
          ],
        },
      ],
    },
    {
      path: '/*',
      redirect: '/',
    },
  ],
});
