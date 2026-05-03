# 🚀 **Project Chronos: Interstellar Booking Synchronization**
### **IBM Bob Dev Day Hackathon 2026 Submission**

**Project Chronos** is a high-performance extension of the **Galaxium Travels** ecosystem. By leveraging **IBM Bob** as an AI-powered development partner, we transformed a standard booking template into a physics-aware, relativistic-syncing platform in record time to meet the hackathon goal of turning **"idea into impact faster."**

---

## **🤖 Idea to Impact: The IBM Bob Factor**

We used **IBM Bob** to accelerate the development lifecycle and move from a "broken handshake" to a "synchronized reality" faster than traditional manual development:

*  **Accelerated Onboarding**: Used **Bob** to quickly map the existing architecture of the Python, Java, and React microservices.  

*  **Rapid Bug Resolution**: **Bob** identified and fixed a critical "None" type handshake error between the Java Inventory Service and the Python Backend that would have stalled deployment.

*  **Automated Artifacts**: Generated complex relativistic logic and documentation, reducing the routine manual work that slows down a team.

*  **Proof of Collaboration**: Full interaction logs and generated logic sessions are available in the **/bob_sessions folder**.

---

## **🌌 The Challenge: Relativistic Clock Drift**

In interstellar travel, time is not constant. Due to time dilation, traveler ship-time drifts away from Earth-time (UTC).

*  **The Problem**: Standard reservation holds expire prematurely or fail to synchronize when users move at relativistic speeds.

*  **The Solution**: Project Chronos anchors all transactions to a Universal Reference Frame.

---

### **The Physics Engine**

We integrated a backend logic layer that utilizes the **Lorentz Factor** ($\gamma$) to ensure booking holds remain valid across different inertial frames:

                 $$ \gamma = \frac{1}{\sqrt{1 - \frac{v^2}{c^2}}} $$

---

## **🏗️ System Architecture**

The project maintains a robust, three-tier microservice structure, hardened with a physics-aware sync layer:

*   **`booking_system_backend/`**: FastAPI (Python) service featuring the new **Physics Sync Engine**.
*   **`booking_system_frontend/`**: React (TypeScript) UI displaying **real-time UTC countdowns**.
*   **`inventory_hold_service/`**: Spring Boot (Java) service managing **relativity-safe reservation logic**.
*   **`bob_sessions/`**: **REQUIRED** interaction reports showing our development journey with **IBM Bob**.
*   **`docker-compose.yml`**: Full-stack orchestration for one-command deployment.

---

## **🌟 Key Innovation Features**

*   **Physics-Aware API**: A hardened handshake between services that prevents **"None/Undefined"** ID errors during relativistic data transfers.
*   **Modern Space-Themed UI**: A beautiful, responsive interface featuring an animated starfield and live seat availability.
*   **Dynamic Class Tracking**: Independent availability for **Economy**, **Business**, and **Galaxium Class** seats.
*   **Universal Reference Sync**: Live updates for seat counts and booking status using a unified, drift-free **UTC clock**.

---

## **🚀 Quick Start Guide**

### **Prerequisites**
*   **Python 3.8+**
*   **Node.js 18+** (with npm)
*   **Java 17+** (for the Inventory Service)

---

### **One-Command Launch (Recommended)**

**For Windows Users:**
```bash
start.bat
```
**For macOS/Linux Users:**
```bash
./start.sh
```
This command automatically installs all dependencies and launches the backend on Port 8001 and the frontend on Port 5173

---

## **💺 Seat Classes & Pricing Model**

| **Class** | **Multiplier** | **Features** | **Seat Allocation** |
| :--- | :--- | :--- | :--- |
| **Economy** | **1.0x** | Standard seating and amenities | **60%** of total seats |
| **Business** | **2.5x** | Priority boarding, extra legroom | **30%** of total seats |
| **Galaxium** | **5.0x** | Private pods, Lounge, Concierge | **10%** of total seats |

---

## **🧪 Testing & Validation**

To verify the service layer and seat class validation logic, run the following:

```bash
cd booking_system_backend
pytest tests/test_services.py
```
---

## **📄 License**

This project is an extension of the Galaxium Travels ecosystem and is licensed under the **Apache License 2.0**. See the [LICENSE] file for full details.


**Built with ❤️ and IBM Bob for the space travelers of tomorrow.** 🚀✨







