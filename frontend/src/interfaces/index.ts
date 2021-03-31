interface Base {
    id: number;
}

export interface IUserProfile extends Base {
    email: string;
    is_active: boolean;
    is_superuser: boolean;
    full_name: string;
}

export interface IUserProfileUpdate {
    email?: string;
    full_name?: string;
    password?: string;
    is_active?: boolean;
    is_superuser?: boolean;
}

export interface IUserProfileCreate {
    email: string;
    full_name?: string;
    password?: string;
    is_active?: boolean;
    is_superuser?: boolean;
}

interface DatasetBase {
    title?: string;
    description?: string;
    url_ids?: number[];
}

export interface IDatasetCreate extends DatasetBase {
    title: string;
    url_ids: number[];
}

export interface IDatasetUpdate extends DatasetBase {

}

export interface IDataset extends DatasetBase, Base {
    title: string;
    description?: string;
    urls: number[];
}


