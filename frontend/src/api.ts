import axios from 'axios';
import {apiUrl} from '@/env';
import {
    IDataset,
    IDatasetCreate,
    IDatasetUpdate,
    IUserProfile,
    IUserProfileCreate,
    IUserProfileUpdate
} from './interfaces';


export const api = {
    uploadUrl: `${apiUrl}/api/v1/datasets/file/`,
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
        return axios.get<IUserProfile>(`${apiUrl}/api/v1/users/me`, this.authHeaders(token));
    },
    async updateMe(token: string, data: IUserProfileUpdate) {
        return axios.put<IUserProfile>(`${apiUrl}/api/v1/users/me`, data, this.authHeaders(token));
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
    async getUsers(token: string) {
        return axios.get<IUserProfile[]>(`${apiUrl}/api/v1/users/`, this.authHeaders(token));
    },
    async updateUser(token: string, userId: number, data: IUserProfileUpdate) {
        return axios.put(`${apiUrl}/api/v1/users/${userId}`, data, this.authHeaders(token));
    },
    async createUser(token: string, data: IUserProfileCreate) {
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
