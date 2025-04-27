import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import { useEffect, useState } from "react";

export default function EventCalendar() {
  const [events, setEvents] = useState([]);
  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_URL}/events`)
      .then(r => r.json())
      .then(setEvents);
  }, []);
  return (
    <FullCalendar
      plugins={[dayGridPlugin]}
      initialView="dayGridMonth"
      events={events.map(e => ({
        id: e.id,
        title: e.title,
        start: e.start_time,
        end: e.end_time
      }))}
    />
  );
}
