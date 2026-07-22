import { SidebarHeader, SidebarMenu, SidebarMenuButton } from "@/src/components/ui/sidebar";
import { BookMarked } from "lucide-react";
import Link from "next/link";

export default function AppSidebarHeader() {
  return (
    <SidebarHeader>
      <SidebarMenu>
        <SidebarMenuButton
          render={<Link href="/" />}
          size="lg"
          className="text-sidebar-accent-foreground"
        >
          <div className="flex size-8 items-center justify-center rounded-lg bg-sidebar-primary text-sidebar-primary-foreground">
            <BookMarked className="!size-5" />
          </div>
          <div className="grid flex-1 text-left text-base leading-tight group-data-[state=collapsed]:hidden">
            <span className="truncate font-medium">RiftTheory</span>
          </div>
        </SidebarMenuButton>
      </SidebarMenu>
    </SidebarHeader>
  );
}
