"use client";
import DefaultLayout from "@/components/Layouts/DefaultLayout";
import React from "react";

interface DashboardLayoutProps {
  children: React.ReactNode;
}

const DashboardLayout = ({ children }: DashboardLayoutProps) => {
  return <DefaultLayout>{children}</DefaultLayout>;
};

export default DashboardLayout;
