import DefaultLayout from "@/components/Layouts/DefaultLayout";
import React from "react";

interface DashboardLayoutProps {
  children: React.ReactNode;
}

const DashboardLayout = ({ children }: DashboardLayoutProps) => {
  return (
    <div className="flex">
      <DefaultLayout>
        <main className="w-screen">{children}</main>
      </DefaultLayout>
    </div>
  );
};

export default DashboardLayout;
