import { Drawer, List, ListItem, ListItemIcon, ListItemText } from "@mui/material";
import DashboardIcon from "@mui/icons-material/Dashboard";
import DirectionsBusIcon from "@mui/icons-material/DirectionsBus";
import TimelineIcon from "@mui/icons-material/Timeline";
import BarChartIcon from "@mui/icons-material/BarChart";
import { NavLink } from "react-router-dom";

export default function Sidebar() {
  const navItems = [
    { to: "/dashboard", icon: <DashboardIcon />, label: "Dashboard" },
    { to: "/buses", icon: <DirectionsBusIcon />, label: "Buses" },
    { to: "/routes", icon: <TimelineIcon />, label: "Routes" },
    { to: "/analytics", icon: <BarChartIcon />, label: "Analytics" },
  ];
  return (
    <Drawer variant="permanent" anchor="left">
      <List>
        {navItems.map(({ to, icon, label }) => (
          <ListItem
            key={to}
            component={NavLink}
            to={to}
            style={({ isActive }) => ({
              background: isActive ? "#e3f2fd" : undefined,
              borderLeft: isActive ? "4px solid #1976d2" : undefined,
            })}
          >
            <ListItemIcon>{icon}</ListItemIcon>
            <ListItemText primary={label} />
          </ListItem>
        ))}
      </List>
    </Drawer>
  );
}