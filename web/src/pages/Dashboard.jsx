import React from "react";
import { Typography, Box } from "@mui/material";

export default function Dashboard() {
  return (
    <Box p={4}>
      <Typography variant="h4">Admin Dashboard</Typography>
      <Typography variant="body1" mt={2}>
        Welcome to the admin dashboard. Use the navigation to manage buses,
        routes, and view analytics.
      </Typography>
    </Box>
  );
}
