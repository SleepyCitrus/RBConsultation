import { Sidebar, SidebarContent, SidebarFooter } from "@/src/components/ui/sidebar";
import AppNavDatabase from "./app-nav-database";
import AppNavEvents from "./app-nav-events";
import AppSidebarHeader from "./app-sidebar-header";

export default function AppSidebar() {
  return (
    <Sidebar collapsible="icon" variant="inset">
      <AppSidebarHeader />
      <SidebarContent>
        <AppNavDatabase />
        <AppNavEvents />
      </SidebarContent>
      <SidebarFooter />
    </Sidebar>
  );
}
