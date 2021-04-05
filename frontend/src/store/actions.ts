import { api } from '@/api';
import {
  IAccessUpdate,
  IDatasetCreate,
  IDatasetUpdate,
  IQueryCreate,
  IQueryRequestsAccessUpdate,
  IQueryUpdate,
} from '@/interfaces';
import router from '@/router';
import { AppNotification, MainState, State } from '@/store/index';
import { getLocalToken, removeLocalToken, saveLocalToken } from '@/utils';
import { AxiosError } from 'axios';
import { getStoreAccessors } from 'typesafe-vuex';
import { ActionContext } from 'vuex';
import {
  commitAddNotification,
  commitPushDataset,
  commitPushQuery,
  commitRemoveNotification,
  commitSetAccesses,
  commitSetAccessGrant,
  commitSetDataset,
  commitSetDatasets,
  commitSetLoggedIn,
  commitSetLogInError,
  commitSetQueries,
  commitSetQuery,
  commitSetQueryRequest,
  commitSetQueryRequests,
  commitSetToken,
  commitSetUserProfile,
} from './mutations';

type MainContext = ActionContext<MainState, State>;

export const actions = {
  async actionGetQueryRequests(context: MainContext) {
    try {
      const response = await api.getQueryRequestsAccesses(
        context.rootState.main.token,
      );
      if (response) {
        commitSetQueryRequests(context, response.data);
      }
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  // async actionGetQueryRequestsByQuery(context: MainContext, queryId: number) {
  //     try {
  //         const response = await api.getQueryRequestsAccessesByQuery(context.rootState.main.token, queryId);
  //         if (response) {
  //             commitSetQueryRequests(context, response.data);
  //         }
  //     } catch (error) {
  //         await dispatchCheckApiError(context, error);
  //     }
  // },
  async actionUpdateQueryRequests(
    context: MainContext,
    payload: { id: number; query: IQueryRequestsAccessUpdate },
  ) {
    try {
      const loadingNotification = { content: 'saving', showProgress: true };
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.updateQueryRequestsAccess(
            context.rootState.main.token,
            payload.id,
            payload.query,
          ),
          await new Promise((resolve, reject) =>
            setTimeout(() => resolve(), 500),
          ),
        ])
      )[0];
      commitSetQueryRequest(context, response.data);
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        content: 'Query Request successfully updated',
        color: 'success',
      });
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionGetAccesses(context: MainContext) {
    try {
      const response = await api.getAccesses(context.rootState.main.token);
      if (response) {
        commitSetAccesses(context, response.data);
      }
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionUpdateAccessGrant(
    context: MainContext,
    payload: { id: number; query: IAccessUpdate },
  ) {
    try {
      const loadingNotification = { content: 'saving', showProgress: true };
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.updateAccessGrant(
            context.rootState.main.token,
            payload.id,
            payload.query,
          ),
          await new Promise((resolve, reject) =>
            setTimeout(() => resolve(), 500),
          ),
        ])
      )[0];
      commitSetAccessGrant(context, response.data);
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        content: 'Query successfully updated',
        color: 'success',
      });
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionGetQueries(context: MainContext) {
    try {
      const response = await api.getQueries(context.rootState.main.token);
      if (response) {
        commitSetQueries(context, response.data);
      }
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionUpdateQuery(
    context: MainContext,
    payload: { id: number; query: IQueryUpdate },
  ) {
    try {
      const loadingNotification = { content: 'saving', showProgress: true };
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.updateQuery(
            context.rootState.main.token,
            payload.id,
            payload.query,
          ),
          await new Promise((resolve, reject) =>
            setTimeout(() => resolve(), 500),
          ),
        ])
      )[0];
      commitSetQuery(context, response.data);
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        content: 'Query successfully updated',
        color: 'success',
      });
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionCreateQuery(
    context: MainContext,
    payload: { query: IQueryCreate; datasetId?: number },
  ) {
    try {
      const { query, datasetId } = payload;
      const loadingNotification = { content: 'saving', showProgress: true };
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.createQuery(context.rootState.main.token, query, datasetId),
          await new Promise((resolve, reject) =>
            setTimeout(() => resolve(), 500),
          ),
        ])
      )[0];
      commitPushQuery(context, response.data);
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        content: 'Query successfully created',
        color: 'success',
      });
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionGetDatasets(context: MainContext) {
    try {
      const response = await api.getDatasets(context.rootState.main.token);
      if (response) {
        commitSetDatasets(context, response.data);
      }
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionUpdateDataset(
    context: MainContext,
    payload: { id: number; dataset: IDatasetUpdate },
  ) {
    try {
      const loadingNotification = { content: 'saving', showProgress: true };
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.updateDataset(
            context.rootState.main.token,
            payload.id,
            payload.dataset,
          ),
          await new Promise((resolve, reject) =>
            setTimeout(() => resolve(), 500),
          ),
        ])
      )[0];
      commitSetDataset(context, response.data);
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        content: 'Dataset successfully updated',
        color: 'success',
      });
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionCreateDataset(context: MainContext, payload: IDatasetCreate) {
    try {
      const loadingNotification = { content: 'saving', showProgress: true };
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.createDataset(context.rootState.main.token, payload),
          await new Promise((resolve, reject) =>
            setTimeout(() => resolve(), 500),
          ),
        ])
      )[0];
      commitPushDataset(context, response.data);
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        content: 'Dataset successfully created',
        color: 'success',
      });
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionLogIn(
    context: MainContext,
    payload: { username: string; password: string },
  ) {
    try {
      const response = await api.logInGetToken(
        payload.username,
        payload.password,
      );
      const token = response.data.access_token;
      if (token) {
        saveLocalToken(token);
        commitSetToken(context, token);
        commitSetLoggedIn(context, true);
        commitSetLogInError(context, false);
        await dispatchGetUserProfile(context);
        await dispatchRouteLoggedIn(context);
        commitAddNotification(context, {
          content: 'Logged in',
          color: 'success',
        });
      } else {
        await dispatchLogOut(context);
      }
    } catch (err) {
      commitSetLogInError(context, true);
      await dispatchLogOut(context);
    }
  },
  async actionGetUserProfile(context: MainContext) {
    try {
      const response = await api.getMe(context.state.token);
      if (response.data) {
        commitSetUserProfile(context, response.data);
      }
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionUpdateUserProfile(context: MainContext, payload) {
    try {
      const loadingNotification = { content: 'saving', showProgress: true };
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.updateMe(context.state.token, payload),
          await new Promise((resolve, reject) =>
            setTimeout(() => resolve(), 500),
          ),
        ])
      )[0];
      commitSetUserProfile(context, response.data);
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        content: 'Profile successfully updated',
        color: 'success',
      });
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionCheckLoggedIn(context: MainContext) {
    if (!context.state.isLoggedIn) {
      let token = context.state.token;
      if (!token) {
        const localToken = getLocalToken();
        if (localToken) {
          commitSetToken(context, localToken);
          token = localToken;
        }
      }
      if (token) {
        try {
          const response = await api.getMe(token);
          commitSetLoggedIn(context, true);
          commitSetUserProfile(context, response.data);
        } catch (error) {
          await dispatchRemoveLogIn(context);
        }
      } else {
        await dispatchRemoveLogIn(context);
      }
    }
  },
  async actionRemoveLogIn(context: MainContext) {
    removeLocalToken();
    commitSetToken(context, '');
    commitSetLoggedIn(context, false);
  },
  async actionLogOut(context: MainContext) {
    await dispatchRemoveLogIn(context);
    await dispatchRouteLogOut(context);
  },
  async actionUserLogOut(context: MainContext) {
    await dispatchLogOut(context);
    commitAddNotification(context, { content: 'Logged out', color: 'success' });
  },
  actionRouteLogOut(context: MainContext) {
    if (router.currentRoute.path !== '/login') {
      router.push('/login');
    }
  },
  async actionCheckApiError(context: MainContext, payload: AxiosError) {
    if (payload.response!.status === 401) {
      await dispatchLogOut(context);
    }
  },
  actionRouteLoggedIn(context: MainContext) {
    if (
      router.currentRoute.path === '/login' ||
      router.currentRoute.path === '/'
    ) {
      router.push('/main');
    }
  },
  async removeNotification(
    context: MainContext,
    payload: { notification: AppNotification; timeout: number },
  ) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        commitRemoveNotification(context, payload.notification);
        resolve(true);
      }, payload.timeout);
    });
  },
  async passwordRecovery(context: MainContext, payload: { username: string }) {
    const loadingNotification = {
      content: 'Sending password recovery email',
      showProgress: true,
    };
    try {
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.passwordRecovery(payload.username),
          await new Promise((resolve, reject) =>
            setTimeout(() => resolve(), 500),
          ),
        ])
      )[0];
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        content: 'Password recovery email sent',
        color: 'success',
      });
      await dispatchLogOut(context);
    } catch (error) {
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        color: 'error',
        content: 'Incorrect username',
      });
    }
  },
  async resetPassword(
    context: MainContext,
    payload: { password: string; token: string },
  ) {
    const loadingNotification = {
      content: 'Resetting password',
      showProgress: true,
    };
    try {
      commitAddNotification(context, loadingNotification);
      const response = (
        await Promise.all([
          api.resetPassword(payload.password, payload.token),
          await new Promise((resolve, reject) =>
            setTimeout(() => resolve(), 500),
          ),
        ])
      )[0];
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        content: 'Password successfully reset',
        color: 'success',
      });
      await dispatchLogOut(context);
    } catch (error) {
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {
        color: 'error',
        content: 'Error resetting password',
      });
    }
  },
};

const { dispatch } = getStoreAccessors<MainState | any, State>('');

export const dispatchCheckApiError = dispatch(actions.actionCheckApiError);
export const dispatchCheckLoggedIn = dispatch(actions.actionCheckLoggedIn);
export const dispatchGetUserProfile = dispatch(actions.actionGetUserProfile);
export const dispatchLogIn = dispatch(actions.actionLogIn);
export const dispatchLogOut = dispatch(actions.actionLogOut);
export const dispatchUserLogOut = dispatch(actions.actionUserLogOut);
export const dispatchRemoveLogIn = dispatch(actions.actionRemoveLogIn);
export const dispatchRouteLoggedIn = dispatch(actions.actionRouteLoggedIn);
export const dispatchRouteLogOut = dispatch(actions.actionRouteLogOut);
export const dispatchUpdateUserProfile = dispatch(
  actions.actionUpdateUserProfile,
);
export const dispatchRemoveNotification = dispatch(actions.removeNotification);
export const dispatchPasswordRecovery = dispatch(actions.passwordRecovery);
export const dispatchResetPassword = dispatch(actions.resetPassword);
export const dispatchGetDatasets = dispatch(actions.actionGetDatasets);
export const dispatchGetQueryRequests = dispatch(
  actions.actionGetQueryRequests,
);
export const dispatchUpdateQueryRequests = dispatch(
  actions.actionUpdateQueryRequests,
);
export const dispatchCreateDataset = dispatch(actions.actionCreateDataset);
export const dispatchUpdateDataset = dispatch(actions.actionUpdateDataset);
export const dispatchCreateQuery = dispatch(actions.actionCreateQuery);
export const dispatchGetQueries = dispatch(actions.actionGetQueries);
export const dispatchGetAccesses = dispatch(actions.actionGetAccesses);
export const dispatchUpdateAccessGrant = dispatch(
  actions.actionUpdateAccessGrant,
);
