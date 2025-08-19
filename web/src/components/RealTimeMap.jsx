import React, { useEffect, useState } from "react";
import { CircularProgress, Typography } from "@mui/material";
import { GoogleMap, Marker, useJsApiLoader } from "@react-google-maps/api";
import axios from "axios";

const containerStyle = { width: "100%", height: "400px" };
const center = { lat: -19.455, lng: 29.817 }; // Example: Gweru, Zimbabwe

export default function RealTimeMap() {
  const { isLoaded } = useJsApiLoader({
    googleMapsApiKey: "AIzaSyCAAgY8nqGTOR1dkzPdlIsXYn6bf4DDmJE",
  });
  const [busLocations, setBusLocations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let interval;
    const fetchLocations = () => {
      axios
        .get("http://parole.pythonanywhere.com/api/bus-locations/")
        .then((res) => {
          setBusLocations(res.data);
          setLoading(false);
        })
        .catch(() => {
          setError("Failed to load bus locations");
          setLoading(false);
        });
    };
    fetchLocations();
    interval = setInterval(fetchLocations, 5000);
    return () => clearInterval(interval);
  }, []);

  if (!isLoaded) return <CircularProgress />;
  if (loading) return <CircularProgress />;
  if (error) return <Typography color="error">{error}</Typography>;

  return (
    <GoogleMap mapContainerStyle={containerStyle} center={center} zoom={13}>
      {busLocations.map((bus) => (
        <Marker
          key={bus.id}
          position={{ lat: bus.latitude, lng: bus.longitude }}
          label={bus.plate_number}
        />
      ))}
    </GoogleMap>
  );
}
