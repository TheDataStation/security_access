import {MainState, State} from '@/store';
import {getStoreAccessors} from 'typesafe-vuex';

export const getters = {
    hasAdminAccess: (state: MainState) => {
        return (
            state.userProfile &&
            state.userProfile.is_operator && state.userProfile.is_active);
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
    queryRequests: (state: MainState) => state.queryRequests,
    oneQueryRequest: (state: MainState) => (queryRequestId: number) => {
        const filteredQueryRequests = state.queryRequests.filter((queryRequest) => queryRequest.id === queryRequestId);
        if (filteredQueryRequests.length > 0) {
            return {...filteredQueryRequests[0]};
        }
    },
    oneQuery: (state: MainState) => (queryId: number) => {
        const filteredQuerys = state.queries.filter((query) => query.id === queryId);
        if (filteredQuerys.length > 0) {
            return {...filteredQuerys[0]};
        }
    },
    accessGrants: (state: MainState) => state.accessGrants ? state.accessGrants : [],
    oneAccessGrant: (state: MainState) => (accessGrantId: number) => {
        const filteredAccessGrants = state.accessGrants.filter((accessGrant) => accessGrant.id === accessGrantId);
        if (filteredAccessGrants.length > 0) {
            return {...filteredAccessGrants[0]};
        }
    },
    accessReceipts: (state: MainState) => state.accessReceipts ? state.accessReceipts : [],
    oneAccessReceipt: (state: MainState) => (accessReceiptId: number) => {
        const filteredAccessReceipts = state.accessReceipts.filter((accessReceipt) => accessReceipt.id === accessReceiptId);
        if (filteredAccessReceipts.length > 0) {
            return {...filteredAccessReceipts[0]};
        }
    },
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
export const readQueryRequests = read(getters.queryRequests);
export const readAccessGrants = read(getters.accessGrants);
export const readAccessReceipts = read(getters.accessReceipts);
export const readUserProfile = read(getters.userProfile);
export const readFirstNotification = read(getters.firstNotification);
export const readOneDataset = read(getters.oneDataset);
export const readOneQuery = read(getters.oneQuery);
export const readOneQueryRequest = read(getters.oneQueryRequest);
export const readOneAccessGrant = read(getters.oneAccessGrant);
export const readOneAccessReceipt = read(getters.oneAccessReceipt);
export const readLastDataset = read(getters.lastDataset);
