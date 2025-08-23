import React from "react";
import {
  Drawer,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Typography,
  Box,
} from "@mui/material";
import { useTheme } from "@mui/material/styles";
import useMediaQuery from "@mui/material/useMediaQuery";
import DashboardIcon from "@mui/icons-material/Dashboard";
import DirectionsBusIcon from "@mui/icons-material/DirectionsBus";
import TimelineIcon from "@mui/icons-material/Timeline";
import PlaceIcon from "@mui/icons-material/Place";
import BarChartIcon from "@mui/icons-material/BarChart";
import EventNoteIcon from "@mui/icons-material/EventNote";
import ReceiptLongIcon from "@mui/icons-material/ReceiptLong";
import { NavLink } from "react-router-dom";

const drawerWidth = 240;

export default function Sidebar({ mobileOpen = false, onClose = () => {} }) {
  const theme = useTheme();
  const isDesktop = useMediaQuery(theme.breakpoints.up("md"));
  const navItems = [
    { to: "/dashboard", icon: <DashboardIcon />, label: "Dashboard" },
    { to: "/buses", icon: <DirectionsBusIcon />, label: "Buses" },
    { to: "/routes", icon: <TimelineIcon />, label: "Routes" },
    { to: "/stations", icon: <PlaceIcon />, label: "Stations" },
    { to: "/schedules", icon: <EventNoteIcon />, label: "Schedules" },
    { to: "/bookings", icon: <ReceiptLongIcon />, label: "Bookings" },
    { to: "/analytics", icon: <BarChartIcon />, label: "Analytics" },
  ];

  const content = (
    <>
      <Toolbar sx={{ minHeight: 64 }}>
        <Typography variant="h6" sx={{ fontWeight: 800, color: "primary.main" }}>
          MSU Admin
        </Typography>
      </Toolbar>
      <Box sx={{ px: 1 }}>
        <List>
          {navItems.map(({ to, icon, label }) => (
            <ListItemButton
              key={to}
              component={NavLink}
              to={to}
              onClick={!isDesktop ? onClose : undefined}
              sx={{
                borderRadius: 2,
                mb: 0.5,
                color: "text.secondary",
                "&.active": {
                  bgcolor: "primary.main",
                  color: "#fff",
                  "& .MuiListItemIcon-root": { color: "#fff" },
                },
              }}
            >
              <ListItemIcon sx={{ minWidth: 40, color: "primary.main" }}>
                {icon}
              </ListItemIcon>
              <ListItemText primary={label} />
            </ListItemButton>
          ))}
        </List>
      </Box>
    </>
  );

  return (
    <>
      {/* Temporary drawer on mobile */}
      {!isDesktop && (
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={onClose}
          ModalProps={{ keepMounted: true }}
          PaperProps={{
            sx: {
              width: drawerWidth,
              borderRight: 0,
              boxShadow: "0 10px 30px rgba(2, 8, 23, 0.06)",
              background: "linear-gradient(180deg, #ffffff 0%, #fbfdff 100%)",
            },
          }}
        >
          {content}
        </Drawer>
      )}
      {/* Permanent drawer on desktop */}
      {isDesktop && (
        <Drawer
          variant="permanent"
          anchor="left"
          PaperProps={{
            sx: {
              width: drawerWidth,
              borderRight: 0,
              boxShadow: "0 10px 30px rgba(2, 8, 23, 0.06)",
              background: "linear-gradient(180deg, #ffffff 0%, #fbfdff 100%)",
            },
          }}
        >
          {content}
        </Drawer>
      )}
    </>
  );
}