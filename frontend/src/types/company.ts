export interface ICompanyCreate {
  name: string
  description?: string
  website?: string
  contact_email: string
  contact_phone: string
  street?: string
  city?: string
  state?: string
  postal_code: string
  country?: string
  admin_id: string
}


export interface ICompanyRead extends ICompanyCreate {
  id: string
  created_at: string
  updated_at: string
}