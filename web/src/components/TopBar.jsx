import React from "react";
import { AppBar, Toolbar, Typography, Avatar, Box, Button, InputBase, alpha, IconButton } from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import { useNavigate } from "react-router-dom";

export default function TopBar({ onMenuClick = () => {} }) {
  const navigate = useNavigate();
  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };
  return (
    <AppBar
      position="sticky"
      color="default"
      elevation={0}
      sx={{
        borderBottom: "1px solid",
        borderColor: (t) => alpha(t.palette.text.primary, 0.06),
        backgroundColor: (t) => alpha("#ffffff", 0.8),
        backdropFilter: "saturate(180%) blur(8px)",
      }}
    >
      <Toolbar sx={{ minHeight: 64 }}>
        <Box sx={{ display: { xs: "flex", md: "none" }, mr: 1 }}>
          <IconButton edge="start" color="inherit" aria-label="menu" onClick={onMenuClick}>
            <MenuIcon />
          </IconButton>
        </Box>
        <Typography variant="h6" sx={{ fontWeight: 700, flexGrow: 1 }}>
          MSU Bus Admin Panel
        </Typography>
        <Box sx={{ display: { xs: "none", md: "flex" }, alignItems: "center", gap: 2, mr: 2 }}>
          <Box
            sx={{
              px: 2,
              py: 0.5,
              borderRadius: 2,
              bgcolor: (t) => alpha(t.palette.primary.main, 0.06),
              minWidth: 260,
            }}
          >
            <InputBase placeholder="Search..." fullWidth />
          </Box>
        </Box>
        <Box display="flex" alignItems="center" gap={2}>
          <Avatar sx={{ bgcolor: "primary.main", width: 32, height: 32 }}>A</Avatar>
          <Button color="error" variant="outlined" onClick={handleLogout}>
            Logout
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
}
