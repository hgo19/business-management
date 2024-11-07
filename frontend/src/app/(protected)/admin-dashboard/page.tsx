'use client'

import { useEffect, useState } from 'react';
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Plus, Trash2 } from 'lucide-react';
import CreateUserModal from './_components/create-user';
import { IUserRead } from '@/types/user';
import api from '@/lib/axios';
import { useAuth } from '@/hooks/useAuth';

export default function Component() {
  const [isUserModalOpen, setIsUserModalOpen] = useState(false);
  const [usersData, setUsersData] = useState<IUserRead[]>([])

  const { user } = useAuth()

  console.log(user)
  
  useEffect(() => {
    const fetchData = async () => {
      if (user?.administered_company) {
        const users = await api.get(`/users/company/${user.administered_company.id}`)
        setUsersData(users.data)
      }
    }

    fetchData()
  }, [user])

  const handleDeleteUser = async (userId: string) => {
    try {
      await api.delete(`/users/${userId}`);
      setUsersData(prevData => prevData.filter(user => user.id !== userId));
    } catch (error) {
      console.error('Error deleting user:', error);
    }
  };

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Admin Administration</h1>
      
      <section>
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-semibold">Users</h2>
          <Button onClick={() => setIsUserModalOpen(true)}>
            <Plus className="mr-2 h-4 w-4" /> Add User
          </Button>
        </div>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Name</TableHead>
              <TableHead>Email</TableHead>
              <TableHead>Role</TableHead>
              <TableHead className="w-[100px]">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {usersData.map((user) => (
              <TableRow key={user.id}>
                <TableCell>{user.name}</TableCell>
                <TableCell>{user.email}</TableCell>
                <TableCell>{user.role}</TableCell>
                <TableCell>
                  <Button
                    variant="destructive"
                    size="sm"
                    onClick={() => handleDeleteUser(user.id)}
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </section>

      <CreateUserModal isOpen={isUserModalOpen} onClose={() => setIsUserModalOpen(false)} setUsersData={setUsersData} companyId={user?.administered_company?.id!} />
    </div>
  );
}