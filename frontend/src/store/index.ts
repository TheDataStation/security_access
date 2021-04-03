import Vue from 'vue';
import Vuex, {StoreOptions} from 'vuex';
import {mutations} from './mutations';
import {getters} from './getters';
import {actions} from './actions';
import {IBothAccess, IDataset, IQuery, IUser} from '@/interfaces';

const defaultState: MainState = {
    isLoggedIn: null,
    token: '',
    logInError: false,
    userProfile: null,
    dashboardMiniDrawer: false,
    dashboardShowDrawer: true,
    notifications: [],
    datasets: [],
    queries: [],
    accesses: {},
};

export const mainModule = {
    state: defaultState,
    mutations,
    actions,
    getters,
};


export interface AppNotification {
    content: string;
    color?: string;
    showProgress?: boolean;
}

export interface MainState {
    token: string;
    isLoggedIn: boolean | null;
    logInError: boolean;
    userProfile: IUser | null;
    dashboardMiniDrawer: boolean;
    dashboardShowDrawer: boolean;
    notifications: AppNotification[];
    datasets: IDataset[];
    queries: IQuery[];
    accesses: IBothAccess;
}

export interface State {
    main: MainState;
}


Vue.use(Vuex);

const storeOptions: StoreOptions<State> = {
    modules: {
        main: mainModule,
    },
};

export const store = new Vuex.Store<State>(storeOptions);

export default store;
