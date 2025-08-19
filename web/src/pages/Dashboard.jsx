import React from "react";
import { Typography, Box, Grid, Card } from "@mui/material";
//import AnalyticsDashboard from "../components/AnalyticsDashboard";
//import RealTimeMap from "../components/RealTimeMap";

export default function Dashboard() {
  return (
    <Box p={4}>
      <Typography variant="h4" gutterBottom>
        Admin Dashboard
      </Typography>
      <Typography variant="body1" mt={2} mb={4}>
        Welcome to the admin dashboard. Use the navigation to manage buses,
        routes, and view analytics.
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Analytics Overview
            </Typography>
            {/* <AnalyticsDashboard /> */}
          </Card>
        </Grid>
        <Grid item xs={12} md={6}>
          <Card sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Real-Time Bus Locations
            </Typography>
            {/* <RealTimeMap /> */}
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}
