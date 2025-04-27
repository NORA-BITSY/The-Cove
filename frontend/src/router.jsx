import React from "react";
import { createBrowserRouter } from "react-router-dom";
import Home from "./pages/Home";
import ReviewsPage from "./pages/ReviewsPage";
import BadgesPage from "./pages/BadgesPage";
// ...existing route imports...

const router = createBrowserRouter([
  { path: "/", element: <Home /> },
  { path: "/reviews", element: <ReviewsPage /> },
  { path: "/badges", element: <BadgesPage /> },
  // ...existing routes...
]);

export default router;
