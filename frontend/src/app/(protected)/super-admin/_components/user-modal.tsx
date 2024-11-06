'use client'

import { useForm, Controller } from 'react-hook-form';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import api from "@/lib/axios";
import { Dispatch, SetStateAction, useEffect } from 'react';
import { IUserCreate, IUserRead, IUserUpdate } from '@/types/user';

interface UserModalProps {
  isOpen: boolean;
  onClose: () => void;
  setUsersData: Dispatch<SetStateAction<IUserRead[]>>;
  editingUser: IUserRead | null;
}

export default function UserModal({ isOpen, onClose, setUsersData, editingUser }: UserModalProps) {
  const { register, handleSubmit, formState: { errors }, reset, setValue, control } = useForm<IUserCreate & IUserUpdate>();

  useEffect(() => {
    if (editingUser) {
      setValue('name', editingUser.name);
      setValue('email', editingUser.email);
      setValue('role', editingUser.role);
    } else {
      reset();
    }
  }, [editingUser, setValue, reset]);

  const onSubmit = async (data: IUserCreate & IUserUpdate) => {
    try {
      let user: IUserRead;
      if (editingUser) {
        const { password, ...updateData } = data;
        user = (await api.put<IUserRead>(`/users/${editingUser.id}`, updateData)).data;
        setUsersData(prev => prev.map(u => u.id === user.id ? user : u));
      } else {
        user = (await api.post<IUserRead>("/users/super-admin", data)).data;
        setUsersData(prev => [...prev, user]);
      }
      reset();
      onClose();
    } catch (error) {
      console.error('Error saving user:', error);
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>{editingUser ? 'Edit User' : 'Create New User'}</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit(onSubmit)}>
          <div className="grid gap-4 py-4">
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="name" className="text-right">
                Name
              </Label>
              <Input
                id="name"
                className="col-span-3"
                {...register("name", { required: "Name is required" })}
              />
              {errors.name && <p className="text-red-500 text-sm col-span-3 col-start-2">{errors.name.message}</p>}
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="email" className="text-right">
                Email
              </Label>
              <Input
                id="email"
                type="email"
                className="col-span-3"
                {...register("email", { required: "Email is required" })}
              />
              {errors.email && <p className="text-red-500 text-sm col-span-3 col-start-2">{errors.email.message}</p>}
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="role" className="text-right">
                Role
              </Label>
              <Controller
                name="role"
                control={control}
                rules={{ required: "Role is required" }}
                render={({ field }) => (
                  <Select onValueChange={field.onChange} value={field.value}>
                    <SelectTrigger className="col-span-3">
                      <SelectValue placeholder="Select a role" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="admin">Admin</SelectItem>
                      <SelectItem value="superadmin">Super admin</SelectItem>
                    </SelectContent>
                  </Select>
                )}
              />
              {errors.role && <p className="text-red-500 text-sm col-span-3 col-start-2">{errors.role.message}</p>}
            </div>
            {!editingUser && (
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="password" className="text-right">
                  Password
                </Label>
                <Input
                  id="password"
                  type="password"
                  className="col-span-3"
                  {...register("password", { required: "Password is required" })}
                />
                {errors.password && <p className="text-red-500 text-sm col-span-3 col-start-2">{errors.password.message}</p>}
              </div>
            )}
          </div>
          <DialogFooter>
            <Button type="submit">{editingUser ? 'Update User' : 'Create User'}</Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}