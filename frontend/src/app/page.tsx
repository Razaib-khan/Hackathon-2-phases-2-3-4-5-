'use client';

import Link from "next/link";
import { useAuth } from '@/src/contexts/AuthContext';

export default function Home() {
  const { user } = useAuth();

  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
      <main className="flex min-h-screen w-full max-w-3xl flex-col items-center justify-between py-32 px-16 bg-white dark:bg-black sm:items-start">
        <div className="flex flex-col items-center gap-6 text-center sm:items-start sm:text-left">
          <h1 className="max-w-xs text-3xl font-semibold leading-10 tracking-tight text-black dark:text-zinc-50">
            Welcome to AIDO TODO App
          </h1>
          <p className="max-w-md text-lg leading-8 text-zinc-600 dark:text-zinc-400">
            Manage your tasks efficiently with our modern task management system.
          </p>
          <div className="flex flex-col gap-4 text-base font-medium sm:flex-row">
            {user ? (
              <>
                <Link
                  href="/tasks"
                  className="flex h-12 w-full items-center justify-center gap-2 rounded-full bg-foreground px-5 text-background transition-colors hover:bg-[#383838] dark:hover:bg-[#ccc] md:w-[158px]"
                >
                  Go to Tasks
                </Link>
                <Link
                  href="/account"
                  className="flex h-12 w-full items-center justify-center gap-2 rounded-full bg-indigo-600 text-white px-5 transition-colors hover:bg-indigo-700 md:w-[158px]"
                >
                  Account Settings
                </Link>
              </>
            ) : (
              <>
                <Link
                  href="/auth/signup"
                  className="flex h-12 w-full items-center justify-center gap-2 rounded-full bg-foreground px-5 text-background transition-colors hover:bg-[#383838] dark:hover:bg-[#ccc] md:w-[158px]"
                >
                  Sign Up
                </Link>
                <Link
                  href="/auth/signin"
                  className="flex h-12 w-full items-center justify-center gap-2 rounded-full bg-indigo-600 text-white px-5 transition-colors hover:bg-indigo-700 md:w-[158px]"
                >
                  Sign In
                </Link>
              </>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
