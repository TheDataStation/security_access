import {AppNotification, MainState} from '@/store';
import {getStoreAccessors} from 'typesafe-vuex';
import {State} from '@/store';
import {IAccess, IBothAccess, IDataset, IQuery, IUser} from '@/interfaces';


export const mutations = {
    setAccesses(state: MainState, payload: IBothAccess) {
        state.accesses = payload;
    },
    pushDataset(state: MainState, payload: IDataset) {
        state.datasets.push(payload);
    },
    setDatasets(state: MainState, payload: IDataset[]) {
        state.datasets = payload;
    },
    setDataset(state: MainState, payload: IDataset) {
        const idx = state.queries.findIndex((q) => q.id === payload.id);
        state.datasets[idx] = payload;
    },
    setQueries(state: MainState, payload: IQuery[]) {
        state.queries = payload;
    },
    pushQuery(state: MainState, payload: IQuery) {
        state.queries.push(payload);
    },
    setQuery(state: MainState, payload: IQuery) {
        const idx = state.queries.findIndex((q) => q.id === payload.id);
        state.queries[idx] = payload;
    },
    setToken(state: MainState, payload: string) {
        state.token = payload;
    },
    setLoggedIn(state: MainState, payload: boolean) {
        state.isLoggedIn = payload;
    },
    setLogInError(state: MainState, payload: boolean) {
        state.logInError = payload;
    },
    setUserProfile(state: MainState, payload: IUser) {
        state.userProfile = payload;
    },
    setDashboardMiniDrawer(state: MainState, payload: boolean) {
        state.dashboardMiniDrawer = payload;
    },
    setDashboardShowDrawer(state: MainState, payload: boolean) {
        state.dashboardShowDrawer = payload;
    },
    addNotification(state: MainState, payload: AppNotification) {
        state.notifications.push(payload);
    },
    removeNotification(state: MainState, payload: AppNotification) {
        state.notifications = state.notifications.filter((notification) => notification !== payload);
    },
};

const {commit} = getStoreAccessors<MainState | any, State>('');

export const commitSetDashboardMiniDrawer = commit(mutations.setDashboardMiniDrawer);
export const commitSetDashboardShowDrawer = commit(mutations.setDashboardShowDrawer);
export const commitSetLoggedIn = commit(mutations.setLoggedIn);
export const commitSetLogInError = commit(mutations.setLogInError);
export const commitSetToken = commit(mutations.setToken);
export const commitSetUserProfile = commit(mutations.setUserProfile);
export const commitAddNotification = commit(mutations.addNotification);
export const commitRemoveNotification = commit(mutations.removeNotification);
export const commitSetDatasets = commit(mutations.setDatasets);
export const commitSetQueries = commit(mutations.setQueries);
export const commitSetAccesses = commit(mutations.setAccesses);
export const commitSetDataset = commit(mutations.setDataset);
export const commitSetQuery = commit(mutations.setQuery);
export const commitPushDataset = commit(mutations.pushDataset);
export const commitPushQuery = commit(mutations.pushQuery);

