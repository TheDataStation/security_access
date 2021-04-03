import {MainState, State} from '@/store';
import {getStoreAccessors} from 'typesafe-vuex';

export const getters = {
    hasAdminAccess: (state: MainState) => {
        return (
            state.userProfile &&
            state.userProfile.is_superuser && state.userProfile.is_active);
    },
    loginError: (state: MainState) => state.logInError,
    dashboardShowDrawer: (state: MainState) => state.dashboardShowDrawer,
    dashboardMiniDrawer: (state: MainState) => state.dashboardMiniDrawer,
    userProfile: (state: MainState) => state.userProfile,
    token: (state: MainState) => state.token,
    isLoggedIn: (state: MainState) => state.isLoggedIn,
    firstNotification: (state: MainState) => state.notifications.length > 0 && state.notifications[0],
    datasets: (state: MainState) => state.datasets,
    queries: (state: MainState) => state.queries,
    accessGrants: (state: MainState) => state.accesses.access_grants ? state.accesses.access_grants : [],
    accessReceipts: (state: MainState) => state.accesses.access_receipts ? state.accesses.access_receipts : [],
    oneDataset: (state: MainState) => (datasetId: number) => {
        const filteredDatasets = state.datasets.filter((dataset) => dataset.id === datasetId);
        if (filteredDatasets.length > 0) {
            return {...filteredDatasets[0]};
        }
    },
    lastDataset: (state: MainState) => state.datasets[state.datasets.length - 1],
};

const {read} = getStoreAccessors<MainState, State>('');

export const readDashboardMiniDrawer = read(getters.dashboardMiniDrawer);
export const readDashboardShowDrawer = read(getters.dashboardShowDrawer);
export const readHasAdminAccess = read(getters.hasAdminAccess);
export const readIsLoggedIn = read(getters.isLoggedIn);
export const readLoginError = read(getters.loginError);
export const readToken = read(getters.token);
export const readDatasets = read(getters.datasets);
export const readQueries = read(getters.queries);
export const readAccessGrants = read(getters.accessGrants);
export const readAccessReceipts = read(getters.accessReceipts);
export const readUserProfile = read(getters.userProfile);
export const readFirstNotification = read(getters.firstNotification);
export const readOneDataset = read(getters.oneDataset);
export const readLastDataset = read(getters.lastDataset);
