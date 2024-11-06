import Link from 'next/link';
import { MessageSquare, ShieldAlert, Shield, LogOut } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { useAuth } from '@/hooks/useAuth';
import { Spinner } from './Spinner';

export default function Sidebar() {
  const { user, logout, isLoading } = useAuth();

  return (
    <div className="w-64 bg-gray-100 h-full p-4 flex flex-col">
      <h1 className="text-2xl font-bold mb-6">Dashboard</h1>
      {isLoading ? (
        <Spinner />
      ) : (
        <nav className="space-y-2 flex-grow">
          {user?.role === 'superadmin' && (
            <Link href="/super-admin" passHref>
              <Button variant="ghost" className="w-full justify-start">
                <ShieldAlert className="mr-2 h-4 w-4" />
                Superadmin
              </Button>
            </Link>
          )}
          {(user?.role === 'superadmin' || user?.role === 'admin') && (
            <Link href="/admin" passHref>
              <Button variant="ghost" className="w-full justify-start">
                <Shield className="mr-2 h-4 w-4" />
                Admin
              </Button>
            </Link>
          )}
          <Link href="/messaging" passHref>
            <Button variant="ghost" className="w-full justify-start">
              <MessageSquare className="mr-2 h-4 w-4" />
              Messaging
            </Button>
          </Link>
        </nav>
      )}
      <Button variant="ghost" className="w-full justify-start mt-auto" onClick={logout}>
        <LogOut className="mr-2 h-4 w-4" />
        Logout
      </Button>
    </div>
  );
}