export interface IUserRead {
  id: string
  name: string
  email: string
  role: string
}

export interface IUserCreate {
  name: string;
  email: string;
  role: string;
  password: string;
}