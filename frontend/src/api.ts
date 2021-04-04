import axios from 'axios';
import {apiUrl} from '@/env';
import {
    IAccessUpdate,
    IBothAccess,
    IDataset,
    IDatasetCreate,
    IDatasetUpdate,
    IQuery,
    IQueryCreate,
    IQueryRequestsAccess,
    IQueryRequestsAccessUpdate,
    IQueryUpdate,
    IUser,
    IUserCreate,
    IUserUpdate,
} from '@/interfaces';


export const api = {
    uploadUrl: `${apiUrl}/api/v1/files/`,
    authHeaders(token: string) {
        return {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        };
    },
    async logInGetToken(username: string, password: string) {
        const params = new URLSearchParams();
        params.append('username', username);
        params.append('password', password);

        return axios.post(`${apiUrl}/api/v1/login/access-token`, params);
    },
    async getMe(token: string) {
        return axios.get<IUser>(`${apiUrl}/api/v1/users/me`, this.authHeaders(token));
    },
    async updateMe(token: string, data: IUserUpdate) {
        return axios.put<IUser>(`${apiUrl}/api/v1/users/me`, data, this.authHeaders(token));
    },
    // async getQueryRequestsAccessesByQuery(token: string, queryId: number) {
    //     return axios.get<IQueryRequestsAccess[]>(`${apiUrl}/api/v1/queries/${queryId}/requests_access/`, this.authHeaders(token));
    // },
    async getQueryRequestsAccesses(token: string) {
        return axios.get<IQueryRequestsAccess[]>(`${apiUrl}/api/v1/queries/requests_access/`, this.authHeaders(token));
    },
    async updateQueryRequestsAccess(token: string, queryRequestsAccessId: number, data: IQueryRequestsAccessUpdate) {
        return axios.put(`${apiUrl}/api/v1/queries/requests_access/${queryRequestsAccessId}`, data, this.authHeaders(token));
    },
    async getDatasets(token: string) {
        return axios.get<IDataset[]>(`${apiUrl}/api/v1/datasets/`, this.authHeaders(token));
    },
    async updateDataset(token: string, datasetId: number, data: IDatasetUpdate) {
        return axios.put(`${apiUrl}/api/v1/datasets/${datasetId}`, data, this.authHeaders(token));
    },
    async createDataset(token: string, data: IDatasetCreate) {
        return axios.post(`${apiUrl}/api/v1/datasets/`, data, this.authHeaders(token));
    },
    async getAccesses(token: string) {
        return axios.get<IBothAccess>(`${apiUrl}/api/v1/accesses/`, this.authHeaders(token));
    },
    async getQueries(token: string) {
        return axios.get<IQuery[]>(`${apiUrl}/api/v1/queries/`, this.authHeaders(token));
    },
    async updateQuery(token: string, queryId: number, data: IQueryUpdate) {
        return axios.put(`${apiUrl}/api/v1/queries/${queryId}`, data, this.authHeaders(token));
    },
    async updateAccessGrant(token: string, accessId: number, data: IAccessUpdate) {
        return axios.put(`${apiUrl}/api/v1/accesses/${accessId}`, data, this.authHeaders(token));
    },
    async createQuery(token: string, data: IQueryCreate, datasetId?: number) {
        return axios.post(`${apiUrl}/api/v1/queries/`, {
            query_in: data,
            dataset_id: {dataset_id: datasetId},
        }, this.authHeaders(token));
    },


    async getUsers(token: string) {
        return axios.get<IUser[]>(`${apiUrl}/api/v1/users/`, this.authHeaders(token));
    },
    async updateUser(token: string, userId: number, data: IUserUpdate) {
        return axios.put(`${apiUrl}/api/v1/users/${userId}`, data, this.authHeaders(token));
    },
    async createUser(token: string, data: IUserCreate) {
        return axios.post(`${apiUrl}/api/v1/users/`, data, this.authHeaders(token));
    },
    async passwordRecovery(email: string) {
        return axios.post(`${apiUrl}/api/v1/password-recovery/${email}`);
    },
    async resetPassword(password: string, token: string) {
        return axios.post(`${apiUrl}/api/v1/reset-password/`, {
            new_password: password,
            token,
        });
    },
};
