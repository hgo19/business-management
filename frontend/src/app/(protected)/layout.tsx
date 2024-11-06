"use client";

import { useEffect } from 'react';
import Sidebar from '@/components/Siderbar';
import { useAuth } from '@/hooks/useAuth';
import { useRouter } from 'next/navigation';
import { Spinner } from '@/components/Spinner';

export default function ProtectedLayout({ children }: { children: React.ReactNode }) {
  const { user, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !user) {
      router.push('/login');
    }
  }, [isLoading, user, router]);

  if (isLoading) {
    return (
      <div className='flex items-center justify-center min-h-screen bg-gray-100'>
        <Spinner className="h-8 w-8" />
      </div>
    );
  }

  return (
    <div className="flex h-screen">
      <Sidebar />
      <main className="flex-1 overflow-y-auto p-8">{children}</main>
    </div>
  );
}
