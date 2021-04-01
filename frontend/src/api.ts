/* eslint-disable */
/* tslint:disable */
/*
 * ---------------------------------------------------------------
 * ## THIS FILE WAS GENERATED VIA SWAGGER-TYPESCRIPT-API        ##
 * ##                                                           ##
 * ## AUTHOR: acacode                                           ##
 * ## SOURCE: https://github.com/acacode/swagger-typescript-api ##
 * ---------------------------------------------------------------
 */

export interface BodyCreateUserOpenApiV1UsersOpenPost {
  password: string;

  /** @format email */
  email: string;
  full_name?: string;
}

export interface BodyLoginAccessTokenApiV1LoginAccessTokenPost {
  /** @pattern password */
  grant_type?: string;
  username: string;
  password: string;
  scope?: string;
  client_id?: string;
  client_secret?: string;
}

export interface BodyResetPasswordApiV1ResetPasswordPost {
  token: string;
  new_password: string;
}

export interface BodyUpdateUserMeApiV1UsersMePut {
  password?: string;
  full_name?: string;

  /** @format email */
  email?: string;
}

export interface Dataset {
  id: number;

  /** @format date-time */
  created_at: string;
  title?: string;
  description?: string;
  url_ids: number[];
}

export interface DatasetCreate {
  title: string;
  description?: string;
  data: string[];
}

export interface DatasetUpdate {
  title?: string;
  description?: string;
}

export interface HTTPValidationError {
  detail?: ValidationError[];
}

export interface Message {
  msg: string;
}

export interface Token {
  access_token: string;
  token_type: string;
}

export interface User {
  id: number;

  /** @format date-time */
  created_at: string;

  /** @format email */
  email?: string;
  is_active?: boolean;
  is_superuser?: boolean;
  full_name?: string;
}

export interface UserCreate {
  /** @format email */
  email: string;
  is_active?: boolean;
  is_superuser?: boolean;
  full_name?: string;
  password: string;
}

export interface UserUpdate {
  /** @format email */
  email?: string;
  is_active?: boolean;
  is_superuser?: boolean;
  full_name?: string;
  password?: string;
}

export interface ValidationError {
  loc: string[];
  msg: string;
  type: string;
}

export type QueryParamsType = Record<string | number, any>;
export type ResponseFormat = keyof Omit<Body, "body" | "bodyUsed">;

export interface FullRequestParams extends Omit<RequestInit, "body"> {
  /** set parameter to `true` for call `securityWorker` for this request */
  secure?: boolean;
  /** request path */
  path: string;
  /** content type of request body */
  type?: ContentType;
  /** query params */
  query?: QueryParamsType;
  /** format of response (i.e. response.json() -> format: "json") */
  format?: ResponseFormat;
  /** request body */
  body?: unknown;
  /** base url */
  baseUrl?: string;
  /** request cancellation token */
  cancelToken?: CancelToken;
}

export type RequestParams = Omit<FullRequestParams, "body" | "method" | "query" | "path">;

export interface ApiConfig<SecurityDataType = unknown> {
  baseUrl?: string;
  baseApiParams?: Omit<RequestParams, "baseUrl" | "cancelToken" | "signal">;
  securityWorker?: (securityData: SecurityDataType | null) => Promise<RequestParams | void> | RequestParams | void;
}

export interface HttpResponse<D extends unknown, E extends unknown = unknown> extends Response {
  data: D;
  error: E;
}

type CancelToken = Symbol | string | number;

export enum ContentType {
  Json = "application/json",
  FormData = "multipart/form-data",
  UrlEncoded = "application/x-www-form-urlencoded",
}

export class HttpClient<SecurityDataType = unknown> {
  public baseUrl: string = "";
  private securityData: SecurityDataType | null = null;
  private securityWorker?: ApiConfig<SecurityDataType>["securityWorker"];
  private abortControllers = new Map<CancelToken, AbortController>();

  private baseApiParams: RequestParams = {
    credentials: "same-origin",
    headers: {},
    redirect: "follow",
    referrerPolicy: "no-referrer",
  };

  constructor(apiConfig: ApiConfig<SecurityDataType> = {}) {
    Object.assign(this, apiConfig);
  }

  public setSecurityData = (data: SecurityDataType | null) => {
    this.securityData = data;
  };

  private addQueryParam(query: QueryParamsType, key: string) {
    const value = query[key];

    return (
      encodeURIComponent(key) +
      "=" +
      encodeURIComponent(Array.isArray(value) ? value.join(",") : typeof value === "number" ? value : `${value}`)
    );
  }

  protected toQueryString(rawQuery?: QueryParamsType): string {
    const query = rawQuery || {};
    const keys = Object.keys(query).filter((key) => "undefined" !== typeof query[key]);
    return keys
      .map((key) =>
        typeof query[key] === "object" && !Array.isArray(query[key])
          ? this.toQueryString(query[key] as QueryParamsType)
          : this.addQueryParam(query, key),
      )
      .join("&");
  }

  protected addQueryParams(rawQuery?: QueryParamsType): string {
    const queryString = this.toQueryString(rawQuery);
    return queryString ? `?${queryString}` : "";
  }

  private contentFormatters: Record<ContentType, (input: any) => any> = {
    [ContentType.Json]: (input: any) =>
      input !== null && (typeof input === "object" || typeof input === "string") ? JSON.stringify(input) : input,
    [ContentType.FormData]: (input: any) =>
      Object.keys(input || {}).reduce((data, key) => {
        data.append(key, input[key]);
        return data;
      }, new FormData()),
    [ContentType.UrlEncoded]: (input: any) => this.toQueryString(input),
  };

  private mergeRequestParams(params1: RequestParams, params2?: RequestParams): RequestParams {
    return {
      ...this.baseApiParams,
      ...params1,
      ...(params2 || {}),
      headers: {
        ...(this.baseApiParams.headers || {}),
        ...(params1.headers || {}),
        ...((params2 && params2.headers) || {}),
      },
    };
  }

  private createAbortSignal = (cancelToken: CancelToken): AbortSignal | undefined => {
    if (this.abortControllers.has(cancelToken)) {
      const abortController = this.abortControllers.get(cancelToken);
      if (abortController) {
        return abortController.signal;
      }
      return void 0;
    }

    const abortController = new AbortController();
    this.abortControllers.set(cancelToken, abortController);
    return abortController.signal;
  };

  public abortRequest = (cancelToken: CancelToken) => {
    const abortController = this.abortControllers.get(cancelToken);

    if (abortController) {
      abortController.abort();
      this.abortControllers.delete(cancelToken);
    }
  };

  public request = async <T = any, E = any>({
    body,
    secure,
    path,
    type,
    query,
    format = "json",
    baseUrl,
    cancelToken,
    ...params
  }: FullRequestParams): Promise<HttpResponse<T, E>> => {
    const secureParams =
      ((typeof secure === "boolean" ? secure : this.baseApiParams.secure) &&
        this.securityWorker &&
        (await this.securityWorker(this.securityData))) ||
      {};
    const requestParams = this.mergeRequestParams(params, secureParams);
    const queryString = query && this.toQueryString(query);
    const payloadFormatter = this.contentFormatters[type || ContentType.Json];

    return fetch(`${baseUrl || this.baseUrl || ""}${path}${queryString ? `?${queryString}` : ""}`, {
      ...requestParams,
      headers: {
        ...(type && type !== ContentType.FormData ? { "Content-Type": type } : {}),
        ...(requestParams.headers || {}),
      },
      signal: cancelToken ? this.createAbortSignal(cancelToken) : void 0,
      body: typeof body === "undefined" || body === null ? null : payloadFormatter(body),
    }).then(async (response) => {
      const r = response as HttpResponse<T, E>;
      r.data = (null as unknown) as T;
      r.error = (null as unknown) as E;

      const data = await response[format]()
        .then((data) => {
          if (r.ok) {
            r.data = data;
          } else {
            r.error = data;
          }
          return r;
        })
        .catch((e) => {
          r.error = e;
          return r;
        });

      if (cancelToken) {
        this.abortControllers.delete(cancelToken);
      }

      if (!response.ok) throw data;
      return data;
    });
  };
}

/**
 * @title datastation
 * @version 0.1.0
 */
export class Api<SecurityDataType extends unknown> extends HttpClient<SecurityDataType> {
  api = {
    /**
     * @description OAuth2 compatible token login, get an access token for future requests
     *
     * @tags login
     * @name LoginAccessTokenApiV1LoginAccessTokenPost
     * @summary Login Access Token
     * @request POST:/api/v1/login/access-token
     */
    loginAccessTokenApiV1LoginAccessTokenPost: (
      data: BodyLoginAccessTokenApiV1LoginAccessTokenPost,
      params: RequestParams = {},
    ) =>
      this.request<Token, HTTPValidationError>({
        path: `/api/v1/login/access-token`,
        method: "POST",
        body: data,
        type: ContentType.UrlEncoded,
        format: "json",
        ...params,
      }),

    /**
     * @description Test access token
     *
     * @tags login
     * @name TestTokenApiV1LoginTestTokenPost
     * @summary Test Token
     * @request POST:/api/v1/login/test-token
     * @secure
     */
    testTokenApiV1LoginTestTokenPost: (params: RequestParams = {}) =>
      this.request<User, any>({
        path: `/api/v1/login/test-token`,
        method: "POST",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description Reset password
     *
     * @tags login
     * @name ResetPasswordApiV1ResetPasswordPost
     * @summary Reset Password
     * @request POST:/api/v1/reset-password/
     */
    resetPasswordApiV1ResetPasswordPost: (data: BodyResetPasswordApiV1ResetPasswordPost, params: RequestParams = {}) =>
      this.request<Message, HTTPValidationError>({
        path: `/api/v1/reset-password/`,
        method: "POST",
        body: data,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * @description Retrieve users.
     *
     * @tags users
     * @name ReadUsersApiV1UsersGet
     * @summary Read Users
     * @request GET:/api/v1/users/
     * @secure
     */
    readUsersApiV1UsersGet: (query?: { skip?: number; limit?: number }, params: RequestParams = {}) =>
      this.request<User[], HTTPValidationError>({
        path: `/api/v1/users/`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description Create new user.
     *
     * @tags users
     * @name CreateUserApiV1UsersPost
     * @summary Create User
     * @request POST:/api/v1/users/
     * @secure
     */
    createUserApiV1UsersPost: (data: UserCreate, params: RequestParams = {}) =>
      this.request<User, HTTPValidationError>({
        path: `/api/v1/users/`,
        method: "POST",
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * @description Get current user.
     *
     * @tags users
     * @name ReadUserMeApiV1UsersMeGet
     * @summary Read User Me
     * @request GET:/api/v1/users/me
     * @secure
     */
    readUserMeApiV1UsersMeGet: (params: RequestParams = {}) =>
      this.request<User, any>({
        path: `/api/v1/users/me`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description Update own user.
     *
     * @tags users
     * @name UpdateUserMeApiV1UsersMePut
     * @summary Update User Me
     * @request PUT:/api/v1/users/me
     * @secure
     */
    updateUserMeApiV1UsersMePut: (data: BodyUpdateUserMeApiV1UsersMePut, params: RequestParams = {}) =>
      this.request<User, HTTPValidationError>({
        path: `/api/v1/users/me`,
        method: "PUT",
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * @description Create new user without the need to be logged in.
     *
     * @tags users
     * @name CreateUserOpenApiV1UsersOpenPost
     * @summary Create User Open
     * @request POST:/api/v1/users/open
     */
    createUserOpenApiV1UsersOpenPost: (data: BodyCreateUserOpenApiV1UsersOpenPost, params: RequestParams = {}) =>
      this.request<User, HTTPValidationError>({
        path: `/api/v1/users/open`,
        method: "POST",
        body: data,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * @description Get a specific user by id.
     *
     * @tags users
     * @name ReadUserByIdApiV1UsersUserIdGet
     * @summary Read User By Id
     * @request GET:/api/v1/users/{user_id}
     * @secure
     */
    readUserByIdApiV1UsersUserIdGet: (userId: number, params: RequestParams = {}) =>
      this.request<User, HTTPValidationError>({
        path: `/api/v1/users/${userId}`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description Update a user.
     *
     * @tags users
     * @name UpdateUserApiV1UsersUserIdPut
     * @summary Update User
     * @request PUT:/api/v1/users/{user_id}
     * @secure
     */
    updateUserApiV1UsersUserIdPut: (userId: number, data: UserUpdate, params: RequestParams = {}) =>
      this.request<User, HTTPValidationError>({
        path: `/api/v1/users/${userId}`,
        method: "PUT",
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * @description Retrieve datasets.
     *
     * @tags datasets
     * @name ReadDatasetsApiV1DatasetsGet
     * @summary Read Datasets
     * @request GET:/api/v1/datasets/
     * @secure
     */
    readDatasetsApiV1DatasetsGet: (query?: { skip?: number; limit?: number }, params: RequestParams = {}) =>
      this.request<Dataset[], HTTPValidationError>({
        path: `/api/v1/datasets/`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description Create new dataset.
     *
     * @tags datasets
     * @name CreateDatasetApiV1DatasetsPost
     * @summary Create Dataset
     * @request POST:/api/v1/datasets/
     * @secure
     */
    createDatasetApiV1DatasetsPost: (data: DatasetCreate, params: RequestParams = {}) =>
      this.request<Dataset, HTTPValidationError>({
        path: `/api/v1/datasets/`,
        method: "POST",
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * @description Get dataset by ID.
     *
     * @tags datasets
     * @name ReadDatasetApiV1DatasetsIdGet
     * @summary Read Dataset
     * @request GET:/api/v1/datasets/{id}
     * @secure
     */
    readDatasetApiV1DatasetsIdGet: (id: number, params: RequestParams = {}) =>
      this.request<Dataset, HTTPValidationError>({
        path: `/api/v1/datasets/${id}`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description Update an dataset.
     *
     * @tags datasets
     * @name UpdateDatasetApiV1DatasetsIdPut
     * @summary Update Dataset
     * @request PUT:/api/v1/datasets/{id}
     * @secure
     */
    updateDatasetApiV1DatasetsIdPut: (id: number, data: DatasetUpdate, params: RequestParams = {}) =>
      this.request<Dataset, HTTPValidationError>({
        path: `/api/v1/datasets/${id}`,
        method: "PUT",
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * @description Delete an dataset.
     *
     * @tags datasets
     * @name DeleteDatasetApiV1DatasetsIdDelete
     * @summary Delete Dataset
     * @request DELETE:/api/v1/datasets/{id}
     * @secure
     */
    deleteDatasetApiV1DatasetsIdDelete: (id: number, params: RequestParams = {}) =>
      this.request<Dataset, HTTPValidationError>({
        path: `/api/v1/datasets/${id}`,
        method: "DELETE",
        secure: true,
        format: "json",
        ...params,
      }),
  };
}
