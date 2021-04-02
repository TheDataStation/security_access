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

export interface IBodyCreateFileApiV1FilesPost {
  /** @format binary */
  file: File;
}

export interface IBodyCreateUserOpenApiV1UsersOpenPost {
  password: string;

  /** @format email */
  email: string;
  full_name?: string;
}

export interface IBodyLoginAccessTokenApiV1LoginAccessTokenPost {
  /** @pattern password */
  grant_type?: string;
  username: string;
  password: string;
  scope?: string;
  client_id?: string;
  client_secret?: string;
}

export interface IBodyResetPasswordApiV1ResetPasswordPost {
  token: string;
  new_password: string;
}

export interface IBodyUpdateUserMeApiV1UsersMePut {
  password?: string;
  full_name?: string;

  /** @format email */
  email?: string;
}

export interface IDataset {
  id: number;

  /** @format date-time */
  created_at: string;
  title: string;
  description?: string;
  file_ids: number[];
}

export interface IDatasetCreate {
  title: string;
  description?: string;
  fileIds: number[];
}

export interface IDatasetUpdate {
  title?: string;
  description?: string;
}

export interface IFile {
  id: number;

  /** @format date-time */
  created_at: string;
  name: string;
}

export interface IHTTPValidationError {
  detail?: IValidationError[];
}

export interface IMessage {
  msg: string;
}

export interface IQuery {
  id: number;

  /** @format date-time */
  created_at: string;

  /** @format binary */
  input_data?: File;
  status?: IQueryStatus;
  status_reason?: string;

  /** An enumeration. */
  type?: IQueryType;
  description?: string;

  /** @format json-string */
  payload?: string;
}

export interface IQueryCreate {
  /** An enumeration. */
  type: IQueryType;
  description?: string;

  /** @format json-string */
  payload?: string;
}

/**
 * An enumeration.
 */
export enum IQueryStatus {
  IPending = "pending",
  IStarted = "started",
  ISucceeded = "succeeded",
  IFailed = "failed",
}

/**
 * An enumeration.
 */
export enum IQueryType {
  IDod = "dod",
  IBlindml = "blindml",
  ICatalog = "catalog",
  IOther = "other",
}

export interface IQueryUpdate {
  id: number;

  /** @format date-time */
  created_at: string;

  /** @format binary */
  input_data?: File;
  status?: IQueryStatus;
  status_reason?: string;

  /** An enumeration. */
  type?: IQueryType;
  description?: string;

  /** @format json-string */
  payload?: string;
}

export interface IToken {
  access_token: string;
  token_type: string;
}

export interface IUser {
  id: number;

  /** @format date-time */
  created_at: string;

  /** @format email */
  email?: string;
  is_active?: boolean;
  is_superuser?: boolean;
  full_name?: string;
}

export interface IUserCreate {
  /** @format email */
  email: string;
  is_active?: boolean;
  is_superuser?: boolean;
  full_name?: string;
  password: string;
}

export interface IUserUpdate {
  /** @format email */
  email?: string;
  is_active?: boolean;
  is_superuser?: boolean;
  full_name?: string;
  password?: string;
}

export interface IValidationError {
  loc: string[];
  msg: string;
  type: string;
}
