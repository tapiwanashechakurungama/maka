import React from "react";
import { Typography, Box } from "@mui/material";

export default function RoutesPage() {
  return (
    <Box p={4}>
      <Typography variant="h5">Routes Management</Typography>
      <Typography variant="body2" mt={2}>
        Here you can add, edit, and view routes. (CRUD functionality coming
        soon)
      </Typography>
    </Box>
  );
}
