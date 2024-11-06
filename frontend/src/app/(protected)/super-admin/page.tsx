'use client'

import { useEffect, useState } from 'react';
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Plus } from 'lucide-react';
import CreateCompanyModal from './_components/create-company';
import CreateAdminModal from './_components/create-admin';
import api from "@/lib/axios"
import { IUserRead } from '@/types/user';
import { ICompanyRead } from '@/types/company';


export default function SuperadminPage() {
  const [isCompanyModalOpen, setIsCompanyModalOpen] = useState(false);
  const [isSuperadminModalOpen, setIsSuperadminModalOpen] = useState(false);
  const [usersData, setUsersData] = useState<IUserRead[]>([])
  const [companiesData, setCompaniesData] = useState<ICompanyRead[]>([])

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
        console.log(error)
      }
    }
  
    fetchData()
  }, [])
  

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Superadmin Administration</h1>
      
      <section className="mb-8">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-semibold">Companies</h2>
          <Button onClick={() => setIsCompanyModalOpen(true)}>
            <Plus className="mr-2 h-4 w-4" /> Add Company
          </Button>
        </div>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Company Name</TableHead>
              <TableHead>Contact Email</TableHead>
              <TableHead>Contact Phone</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {companiesData.map((company) => (
              <TableRow key={company.id}>
                <TableCell>{company.name}</TableCell>
                <TableCell>{company.contact_email}</TableCell>
                <TableCell>{company.contact_phone}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </section>

      <section className="mb-8">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-semibold">Users</h2>
          <Button onClick={() => setIsSuperadminModalOpen(true)}>
            <Plus className="mr-2 h-4 w-4" /> Add Superadmin/Admin
          </Button>
        </div>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Name</TableHead>
              <TableHead>Email</TableHead>
              <TableHead>Role</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {usersData.map((user) => (
              <TableRow key={user.id}>
                <TableCell>{user.name}</TableCell>
                <TableCell>{user.email}</TableCell>
                <TableCell>{user.role}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </section>

      <CreateCompanyModal isOpen={isCompanyModalOpen} onClose={() => setIsCompanyModalOpen(false)} setCompaniesData={setCompaniesData} />
      <CreateAdminModal isOpen={isSuperadminModalOpen} onClose={() => setIsSuperadminModalOpen(false)} setUsersData={setUsersData} />
    </div>
  );
}