import React from 'react'
import { IUserRead } from '@/types/user'

interface UserPanelProps {
  users: IUserRead[]
  companyName: string
}

export const UserPanel: React.FC<UserPanelProps> = ({ users, companyName }) => {
  return (
    <div className="w-64 bg-white shadow-md p-4">
      <h2 className="text-xl font-semibold mb-4">{companyName} Users</h2>
      <ul>
        {users.map(user => (
          <li key={user.id} className="mb-2">
            <span className="font-medium">{user.name}</span> {user.administered_company ? "(Admin)" : ""}
          </li>
        ))}
      </ul>
    </div>
  )
}
