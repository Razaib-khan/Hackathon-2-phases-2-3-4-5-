import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { ThemeProvider } from '../utils/theme';
import { AuthProvider } from '../contexts/AuthContext';
import ChatWidget from '@/components/ChatWidget';
import { ToastProvider } from '@/context/ToastContext';
import { ChatProvider } from '@/context/ChatContext';

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "AIDO TODO App",
  description: "Modern task management system",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <AuthProvider>
          <ThemeProvider>
            <ChatProvider>
              <ToastProvider>
                {children}
                <ChatWidget />
              </ToastProvider>
            </ChatProvider>
          </ThemeProvider>
        </AuthProvider>
      </body>
    </html>
  );
}
