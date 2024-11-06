export interface IUserRead {
  id: string
  name: string
  email: string
  role: string
  company_id?: string
}

export interface IUserCreate {
  name: string;
  email: string;
  role: string;
  password: string;
}


export type IUserUpdate = Partial<IUserCreate>