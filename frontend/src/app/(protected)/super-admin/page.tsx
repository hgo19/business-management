'use client'

import { useEffect, useState } from 'react';
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Plus, Trash2, Edit } from 'lucide-react';
import CompanyModal from './_components/company-modal';
import UserModal from './_components/user-modal';
import api from "@/lib/axios"
import { IUserRead } from '@/types/user';
import { ICompanyRead } from '@/types/company';
import { useAuth } from '@/hooks/useAuth';

export default function Component() {
  const [isCompanyModalOpen, setIsCompanyModalOpen] = useState(false);
  const [isUserModalOpen, setIsUserModalOpen] = useState(false);
  const [usersData, setUsersData] = useState<IUserRead[]>([])
  const [companiesData, setCompaniesData] = useState<ICompanyRead[]>([])
  const [editingUser, setEditingUser] = useState<IUserRead | null>(null);
  const [editingCompany, setEditingCompany] = useState<ICompanyRead | null>(null);
  const [admins, setAdmins] = useState<IUserRead[]>([])
  const { user } = useAuth()


  useEffect(() => {
    const fetchData = async () => {
      try {
        const [usersResponse, companiesResponse] = await Promise.all([
          api.get("/users"),
          api.get("/companies"),
        ])
        setUsersData(usersResponse.data)
        setCompaniesData(companiesResponse.data)
      } catch (error) {
        console.error(error)
      }
    }
  
    fetchData()
  }, [])


  useEffect(() => {
    const getAdmins = () => {
      if (usersData && usersData.length) {
        const admins = usersData.filter(userData => userData.role === "admin")
        setAdmins(admins)
      }
    }

    getAdmins()
  }, [usersData])

  const handleDeleteCompany = async (companyId: string) => {
    try {
      await api.delete(`/companies/${companyId}`);
      setCompaniesData(prevData => prevData.filter(company => company.id !== companyId));
    } catch (error) {
      console.error('Error deleting company:', error);
    }
  };

  const handleDeleteUser = async (userId: string) => {
    try {
      await api.delete(`/users/${userId}`);
      setUsersData(prevData => prevData.filter(user => user.id !== userId));
    } catch (error) {
      console.error('Error deleting user:', error);
    }
  };

  const handleEditUser = (user: IUserRead) => {
    setEditingUser(user);
    setIsUserModalOpen(true);
  };

  const handleEditCompany = (company: ICompanyRead) => {
    setEditingCompany(company);
    setIsCompanyModalOpen(true);
  };

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Superadmin Administration</h1>
      
      <section className="mb-8">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-semibold">Companies</h2>
          <Button onClick={() => {setEditingCompany(null); setIsCompanyModalOpen(true);}}>
            <Plus className="mr-2 h-4 w-4" /> Add Company
          </Button>
        </div>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Company Name</TableHead>
              <TableHead>Contact Email</TableHead>
              <TableHead>Contact Phone</TableHead>
              <TableHead className="w-[150px]">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {companiesData.map((company) => (
              <TableRow key={company.id}>
                <TableCell>{company.name}</TableCell>
                <TableCell>{company.contact_email}</TableCell>
                <TableCell>{company.contact_phone}</TableCell>
                <TableCell>
                  <div className="flex space-x-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleEditCompany(company)}
                    >
                      <Edit className="h-4 w-4" />
                    </Button>
                    <Button
                      variant="destructive"
                      size="sm"
                      onClick={() => handleDeleteCompany(company.id)}
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </section>

      <section className="mb-8">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-semibold">Users</h2>
          <Button onClick={() => {setEditingUser(null); setIsUserModalOpen(true);}}>
            <Plus className="mr-2 h-4 w-4" /> Add Superadmin/Admin
          </Button>
        </div>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Name</TableHead>
              <TableHead>Email</TableHead>
              <TableHead>Role</TableHead>
              <TableHead className="w-[150px]">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {usersData.map((userData) => (
              <TableRow key={userData.id}>
                <TableCell>{userData.name}</TableCell>
                <TableCell>{userData.email}</TableCell>
                <TableCell>{userData.role}</TableCell>
                <TableCell>
                  <div className="flex space-x-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleEditUser(userData)}
                    >
                      <Edit className="h-4 w-4" />
                    </Button>
                    <Button
                      variant="destructive"
                      size="sm"
                      onClick={() => handleDeleteUser(userData.id)}
                      disabled={userData.id === user?.id}
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </section>

      <CompanyModal 
        isOpen={isCompanyModalOpen} 
        onClose={() => {setIsCompanyModalOpen(false); setEditingCompany(null);}} 
        setCompaniesData={setCompaniesData} 
        editingCompany={editingCompany}
        admins={admins}
      />
      <UserModal 
        isOpen={isUserModalOpen} 
        onClose={() => {setIsUserModalOpen(false); setEditingUser(null);}} 
        setUsersData={setUsersData} 
        editingUser={editingUser}
      />
    </div>
  );
}