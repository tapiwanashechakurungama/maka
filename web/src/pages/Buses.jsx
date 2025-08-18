import React from "react";
import { Typography, Box } from "@mui/material";

export default function Buses() {
  return (
    <Box p={4}>
      <Typography variant="h5">Buses Management</Typography>
      <Typography variant="body2" mt={2}>
        Here you can add, edit, and view buses. (CRUD functionality coming soon)
      </Typography>
    </Box>
  );
}
