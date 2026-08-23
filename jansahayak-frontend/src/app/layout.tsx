import type { Metadata } from "next";
import { Geist } from "next/font/google";
import "./globals.css";
import { ToastMsgProvider } from "@/contexts/ToastMsgContext";
import ToastNotification from "@/components/global/ToastMsg";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "JanSayaHak",
  description: "AI Prompt Interface",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en" className={`${geistSans.variable} h-full antialiased`}>
      <ToastMsgProvider>
        <body className="min-h-screen min-w-screen flex flex-col scrollbar-thumb-ui-tertiary/20 scrollbar-thin">
          <ToastNotification />
          {children}
        </body>
      </ToastMsgProvider>
    </html>
  );
}
