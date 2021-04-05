import {
  IAccess,
  IDataset,
  IQuery,
  IQueryRequestsAccess,
  IUser,
} from '@/interfaces';
import Vue from 'vue';
import Vuex, { StoreOptions } from 'vuex';
import { actions } from './actions';
import { getters } from './getters';
import { mutations } from './mutations';

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
  queryRequests: IQueryRequestsAccess[];
  accessGrants: IAccess[];
  accessReceipts: IAccess[];
}

export interface State {
  main: MainState;
}

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
  accessGrants: [],
  accessReceipts: [],
  queryRequests: [],
};

export const mainModule = {
  state: defaultState,
  mutations,
  actions,
  getters,
};

Vue.use(Vuex);

const storeOptions: StoreOptions<State> = {
  modules: {
    main: mainModule,
  },
};

export const store = new Vuex.Store<State>(storeOptions);

export default store;
