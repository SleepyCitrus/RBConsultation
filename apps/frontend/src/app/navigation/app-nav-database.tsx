import {
  SidebarGroup,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/src/components/ui/sidebar";
import { IconPin, IconSparkles2 } from "@tabler/icons-react";
import Link from "next/link";

const databaseNav = [
  {
    title: "New Reveals",
    url: "/reveals",
    icon: IconSparkles2,
  },
  {
    title: "Staples",
    url: "/staples",
    icon: IconPin,
  },
  // {
  //   title: "Cards",
  //   url: "/cards",
  //   icon: IconCards,
  // },
  // {
  //   title: "Decks",
  //   url: "/decks",
  //   icon: IconCopy,
  // },
];

export default function AppNavDatabase() {
  return (
    <SidebarGroup>
      <SidebarGroupLabel>Database</SidebarGroupLabel>
      <SidebarMenu>
        {databaseNav.map((item) => (
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
