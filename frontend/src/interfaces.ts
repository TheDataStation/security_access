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

export interface IAccess {
  id: number;

  /** @format date-time */
  created_at: string;
  expiry?: string | string | number;
  reveal_sharer?: boolean;

  /** An enumeration. */
  decision?: IAccessDecision;
  decision_reason?: string;
}

/**
 * An enumeration.
 */
export enum IAccessDecision {
  IYes = "yes",
  INo = "no",
  IMaybe = "maybe",
  IPending = "pending",
}

export interface IAccessUpdate {
  expiry?: string | string | number;
  reveal_sharer?: boolean;

  /** An enumeration. */
  decision?: IAccessDecision;
  decision_reason?: string;
}

export interface IBodyCreateFileApiV1FilesPost {
  /** @format binary */
  file: File;
}

export interface IBodyCreateQueryApiV1QueriesPost {
  query_in: IQueryCreate;
  dataset_id: IDatasetID;
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

export interface IBothAccess {
  access_grants?: IAccess[];
  access_receipts?: IAccess[];
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
  file_ids: number[];
}

export interface IDatasetID {
  dataset_id?: number;
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
  sharer_id: number;
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
  querier_id: number;
}

export interface IQueryCreate {
  /** An enumeration. */
  type: IQueryType;
  description?: string;

  /** @format json-string */
  payload?: string;
}

export interface IQueryRequestsAccess {
  id: number;

  /** @format date-time */
  created_at: string;
  expiry?: string | string | number;
  reveal_input_data?: boolean;
  reveal_querier?: boolean;
  query_id: number;
  access_id: number;
}

export interface IQueryRequestsAccessUpdate {
  expiry?: string | string | number;
  reveal_input_data?: boolean;
  reveal_querier?: boolean;
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
  is_operator?: boolean;
  full_name?: string;
}

export interface IUserCreate {
  /** @format email */
  email: string;
  is_active?: boolean;
  is_operator?: boolean;
  full_name?: string;
  password: string;
}

export interface IUserUpdate {
  /** @format email */
  email?: string;
  is_active?: boolean;
  is_operator?: boolean;
  full_name?: string;
  password?: string;
}

export interface IValidationError {
  loc: string[];
  msg: string;
  type: string;
}
