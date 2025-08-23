import React, { useEffect, useState } from "react";
import { getBuses, addBus, updateBus, deleteBus, publishBus } from "../api/buses";
import { Button, Box } from "@mui/material";
import BusTable from "../components/BusTable";
import BusForm from "../components/BusForm";

export default function Buses() {
  const [buses, setBuses] = useState([]);
  const [open, setOpen] = useState(false);
  const [editing, setEditing] = useState(null);
  const [form, setForm] = useState({ plate_number: "", capacity: "" });

  // In Buses.jsx
  const fetchBuses = () => getBuses().then(res => {
    const list = Array.isArray(res.data?.results) ? res.data.results : (res.data || []);
    const normalized = list.map(b => ({
      ...b,
      plate_number: b.plate_number ?? b.license_plate ?? b.plateNumber ?? b.licensePlate ?? b.license ?? b.plate ?? '',
    }));
    setBuses(normalized);
  });

  useEffect(() => { fetchBuses(); }, []);

  const handleOpen = (bus = null) => {
    setEditing(bus);
    setForm(bus ? { plate_number: bus.plate_number, capacity: bus.capacity } : { plate_number: "", capacity: "" });
    setOpen(true);
  };

  const handleClose = () => { setOpen(false); setEditing(null); };

  const handleSubmit = async () => {
    if (editing) {
      await updateBus(editing.id, form);
    } else {
      await addBus(form);
    }
    fetchBuses();
    handleClose();
  };

  const handleDelete = async (id) => {
    await deleteBus(id);
    fetchBuses();
  };

  const handlePublish = async (bus) => {
    await publishBus(bus.id, !bus.published);
    fetchBuses();
  };

  return (
    <Box p={{ xs: 2, md: 3 }} sx={{ minHeight: "calc(100vh - 64px)", width: "100%", maxWidth: "100%", overflowX: "hidden" }}>
      <Button variant="contained" onClick={() => handleOpen()} sx={{ mb: 2 }}>Add Bus</Button>
      <BusTable buses={Array.isArray(buses) ? buses : []} onEdit={handleOpen} onDelete={handleDelete} onPublish={handlePublish} />
      <BusForm open={open} onClose={handleClose} onSubmit={handleSubmit} form={form} setForm={setForm} editing={editing} />
    </Box>
  );
}