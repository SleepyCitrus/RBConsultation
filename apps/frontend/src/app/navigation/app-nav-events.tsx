import {
  SidebarGroup,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/src/components/ui/sidebar";
import { IconCalendarEvent } from "@tabler/icons-react";
import Link from "next/link";

const eventsNav = [
  {
    title: "Event Finder",
    url: "/events",
    icon: IconCalendarEvent,
  },
];

export default function AppNavEvents() {
  return (
    <SidebarGroup>
      <SidebarGroupLabel>Events</SidebarGroupLabel>
      <SidebarMenu>
        {eventsNav.map((item) => (
          <SidebarMenuItem key={item.title}>
            <SidebarMenuButton render={<Link href={item.url} />}>
              <item.icon />
              <span>{item.title}</span>
            </SidebarMenuButton>
          </SidebarMenuItem>
        ))}
      </SidebarMenu>
    </SidebarGroup>
  );
}
