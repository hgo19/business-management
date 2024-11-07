import { ICompanyRead } from "./company"

export interface IUserRead {
  id: string
  name: string
  email: string
  role: string
  company_id?: string
  company?: ICompanyRead
  administered_company?: ICompanyRead
}

export interface IUserCreate {
  name: string;
  email: string;
  role: string;
  password: string;
}


export type IUserUpdate = Partial<IUserCreate>