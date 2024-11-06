import { useForm } from 'react-hook-form';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import api from "@/lib/axios";
import { Dispatch, SetStateAction } from 'react';
import { IUserCreate, IUserRead } from '@/types/user';


interface CreateAdminModalProps {
  isOpen: boolean;
  onClose: () => void;
  setUsersData: Dispatch<SetStateAction<IUserRead[]>>
}

export default function CreateAdminModal({ isOpen, onClose, setUsersData }: CreateAdminModalProps) {
  const { register, handleSubmit, formState: { errors }, reset, setValue } = useForm<IUserCreate>();

  const onSubmit = async (data: IUserCreate) => {
    const user = await api.post<IUserRead>("/users/super-admin", data)
    setUsersData((prev) => {
      return [...prev, user.data]
    })
    reset();
    onClose();
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Create New User</DialogTitle>
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
              <Select onValueChange={(value) => setValue('role', value)} >
                <SelectTrigger className="col-span-3">
                  <SelectValue placeholder="Select a role" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="admin" defaultChecked>Admin</SelectItem>
                  <SelectItem value="superadmin" defaultChecked>Super admin</SelectItem>
                </SelectContent>
              </Select>
            </div>
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
          </div>
          <DialogFooter>
            <Button type="submit">Create User</Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}