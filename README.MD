# The Cove

The Cove is a comprehensive web application built for the boating community. It combines a FastAPI backend and a React frontend (using Vite) to deliver real-time functionalities, social interactions, and reservation management—all orchestrated via Docker Compose and served securely behind Nginx.

---

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Functions & Elements](#functions--elements)
- [Installation & Deployment](#installation--deployment)
- [Setup & Configuration](#setup--configuration)
- [User Guide](#user-guide)
- [Contributing](#contributing)

---

## Description

The Cove is designed to serve boaters by providing tools to:
- Reserve spots on marinas or sandbars in real time.
- Engage through live streaming and global message feeds.
- Stay informed with real-time alerts and notifications.
- Participate in events, view calendars, and review local businesses.
- Enjoy an intuitive and interactive web experience even when offline.

---

## Features

- **User Authentication:** Facebook OAuth integration ensures secure access and community verification.
- **Spot Reservations:** A dynamic interactive map allows users to claim and reserve spots.
- **Live Streaming:** Powered by WebRTC and OvenMediaEngine enabling real-time broadcasting.
- **Event Management:** Create and view events using an integrated calendar system.
- **Alerts & Notifications:** Instantly report hazards and receive weather updates.
- **Global Message Feed:** Chat functionality open to all users with write access for logged-in users.
- **Push Notifications & Offline Mode:** Service worker support for offline capabilities and notifications.
- **Additional Modules:** Include local reviews and gamification (badges) to further enhance user engagement.

---

## Functions & Elements

- **Backend:**  
  - REST API endpoints for authentication, spot management, live streaming, events, alerts, messages, reviews, and badges.
  - Real-time communication powered by Socket.IO.
  - Database seeding and migrations with Alembic.

- **Frontend:**  
  - Single Page Application (SPA) built with React and Vite.
  - Components such as LiveStream, MapSpotPicker, GlobalMessageFeed, OnboardingModal, and more.
  - Context-based authentication to manage user sessions.
  - Offline service worker for improved reliability.

- **Infrastructure:**  
  - Docker Compose orchestrates multiple services (frontend, backend, PostgreSQL, Redis, Nginx, media server).
  - Nginx for secure SSL termination.
  - CI/CD integration through GitHub Actions.

---

## Installation & Deployment

### Local Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/<your-username>/thecove.git && cd thecove
   ```

2. **Copy Environment Variables:**
   ```bash
   cp .env.example .env
   ```
   Update the `.env` file with valid credentials and configuration values.

3. **Build and Run Containers:**
   ```bash
   docker compose up -d --build
   ```
   This command builds the containers, applies database migrations, seeds initial data, and starts the application.

4. **Access the Application:**
   Open a browser and navigate to [https://thecove.boatable.app](https://thecove.boatable.app).

### Deployment

- **CI/CD Pipeline:**  
  The GitHub Actions workflow in `.github/workflows/ci.yml` automatically builds, tests, and deploys when changes are pushed to the main branch.
- **Production:**  
  Ensure that SSL certificates are in place (via Let's Encrypt) and DNS records point to the server. Customize the Docker Compose and Nginx configuration as necessary for your hosting environment.

---

## Setup & Configuration

- **Database:**  
  Uses PostgreSQL with connection details provided in the `.env` file.
- **Authentication:**  
  Facebook OAuth credentials must be set in the environment variables.
- **Frontend Config:**  
  VITE_API_URL, VITE_FB_APP_ID, and VITE_MEDIA_WS need to be updated for your specific deployment domain.
- **Service Workers:**  
  The service worker in `/frontend/public/service-worker.js` provides offline mode and push notifications (stubbed for further integration).

---

## User Guide

1. **Onboarding:**  
   New users are greeted with an onboarding modal that explains the features and guides them through setting up their profile and reserving spots.

2. **Spot Reservations:**  
   Navigate to the interactive map, click on an available spot, and claim it with an optional note.

3. **Live Streaming:**  
   - **Start a Stream:** Logged-in users can initiate a broadcast.
   - **Watch a Stream:** View active streams and join the chat.
   
4. **Global Message Feed:**  
   Engage in a community chat that is visible on the home page. Only logged-in users are permitted to send messages.

5. **Events & Reviews:**  
   Check the events calendar for upcoming events or review local businesses (e.g., marinas, fuel docks).

6. **Alerts:**  
   Users can submit real-time alerts to notify others about hazards or weather updates.

---

## Contributing

Contributions are welcome. Please open an issue or pull request on GitHub with your changes. For detailed developer instructions, refer to the project documentation in the repository.

---

Enjoy building, sharing, and navigating the world of boating with The Cove!
