'use client'

import { useForm, Controller, set } from 'react-hook-form'
import { Dispatch, SetStateAction, useEffect, useState } from 'react'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Loader2 } from "lucide-react"
import api from '@/lib/axios'
import { IUserRead } from '@/types/user'
import { ICompanyCreate, ICompanyRead } from '@/types/company'



interface CreateCompanyModalProps {
  isOpen: boolean
  onClose: () => void
  setCompaniesData: Dispatch<SetStateAction<ICompanyRead[]>>
}


export default function CreateCompanyModal({ isOpen, onClose, setCompaniesData }: CreateCompanyModalProps) {
  const { register, handleSubmit, formState: { errors }, reset, control } = useForm<ICompanyCreate>() 
  const [admins, setAdmins] = useState<IUserRead[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchAdmins = async () => {
      try {
        const response = await api.get<IUserRead[]>('/users/admins')
        setAdmins(response.data)
        setIsLoading(false)
      } catch (err) {
        setError('Failed to load admins. Please try again later.')
        setIsLoading(false)
      }
    }

    fetchAdmins()
  }, [])

  const onSubmit = async (data: ICompanyCreate) => {
    console.log(data)
    const company = await api.post("/companies", data)
    setCompaniesData((prev) => {
      return [...prev, company.data]
    })
    reset()
    onClose()
  }

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[600px]">
        <DialogHeader>
          <DialogTitle>Create New Company</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit(onSubmit)}>
          <div className="grid gap-4 py-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="name">Company Name</Label>
                <Input
                  id="name"
                  {...register("name", { required: "Company name is required" })}
                />
                {errors.name && <p className="text-red-500 text-sm">{errors.name.message}</p>}
              </div>
              <div className="space-y-2">
                <Label htmlFor="website">Website</Label>
                <Input
                  id="website"
                  {...register("website")}
                />
              </div>
            </div>
            <div className="space-y-2">
              <Label htmlFor="description">Description</Label>
              <Textarea
                id="description"
                {...register("description")}
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="contact_email">Contact Email</Label>
                <Input
                  id="contact_email"
                  type="email"
                  {...register("contact_email", { required: "Contact email is required" })}
                />
                {errors.contact_email && <p className="text-red-500 text-sm">{errors.contact_email.message}</p>}
              </div>
              <div className="space-y-2">
                <Label htmlFor="contact_phone">Contact Phone</Label>
                <Input
                  id="contact_phone"
                  {...register("contact_phone", { required: "Contact phone is required" })}
                />
                {errors.contact_phone && <p className="text-red-500 text-sm">{errors.contact_phone.message}</p>}
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="street">Street</Label>
                <Input
                  id="street"
                  {...register("street")}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="city">City</Label>
                <Input
                  id="city"
                  {...register("city")}
                />
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="state">State</Label>
                <Input
                  id="state"
                  {...register("state")}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="postal_code">Postal Code</Label>
                <Input
                  id="postal_code"
                  {...register("postal_code", { required: "Postal code is required" })}
                />
                {errors.postal_code && <p className="text-red-500 text-sm">{errors.postal_code.message}</p>}
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="country">Country</Label>
                <Input
                  id="country"
                  {...register("country")}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="admin_id">Admin</Label>
                <Controller
                  name="admin_id"
                  control={control}
                  rules={{ required: "Admin is required" }}
                  render={({ field }) => (
                    <Select onValueChange={field.onChange} value={field.value}>
                      <SelectTrigger>
                        <SelectValue placeholder="Select an admin" />
                      </SelectTrigger>
                      <SelectContent>
                        {isLoading ? (
                          <SelectItem value="loading" disabled>
                            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                            Loading admins...
                          </SelectItem>
                        ) : error ? (
                          <SelectItem value="error" disabled>
                            {error}
                          </SelectItem>
                        ) : (
                          admins.map((admin) => (
                            <SelectItem key={admin.id} value={admin.id}>
                              {admin.name}
                            </SelectItem>
                          ))
                        )}
                      </SelectContent>
                    </Select>
                  )}
                />
                {errors.admin_id && <p className="text-red-500 text-sm">{errors.admin_id.message}</p>}
              </div>
            </div>
          </div>
          <DialogFooter>
            <Button type="submit" disabled={isLoading}>Create Company</Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}