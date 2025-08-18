
---

# Smart Notice Board using Raspberry Pi and Firebase

A modern, IoT-based digital notice board system that replaces traditional paper announcements. It features a web-based admin panel for posting messages and images in real-time, which are then displayed on a screen powered by a Raspberry Pi.

## Problem Statement

Traditional notice boards are static, require manual updates, and are inefficient for disseminating urgent information. This project solves these issues by creating a dynamic, centrally-managed digital notice board that can be updated remotely from any device with a web browser, saving time and reducing paper waste.

## Features

-   **Remote Content Management**: Update notices from any device via a simple web interface.
-   **Multimedia Support**: Post text-based messages and upload accompanying images.
-   **Real-time Updates**: New notices are instantly fetched and displayed on the screen.
-   **Cloud Backend**: Leverages Google Firebase for a robust database and file storage solution.
-   **Auto-Refreshing Display**: The notice board screen automatically refreshes to show the latest content.

## How It Works

The system uses a web application to manage content. An administrator uses a web form to submit new text and images. This data is sent to a Python Flask server, which then stores the text in a Firestore database and the images in Firebase Cloud Storage. A Raspberry Pi, connected to a monitor, runs a web browser pointed at the display page. This page continuously fetches and displays the latest notices from Firebase.

## Technology Stack

| Category      | Technology                              |
| :------------ | :-------------------------------------- |
| **Hardware**  | Raspberry Pi 4, LCD Monitor             |
| **Backend**   | Python, Flask                           |
| **Frontend**  | HTML, CSS (Bootstrap), JavaScript       |
| **Database**  | Google Firestore                        |
| **Storage**   | Google Cloud Storage for Firebase       |

## Hardware & Software Requirements

### Hardware
-   Raspberry Pi 4 (or any model with Wi-Fi)
-   MicroSD Card (16GB+)
-   LCD Monitor with HDMI input
-   HDMI Cable & Power Supply

### Software
-   Raspberry Pi OS
-   Python 3.x
-   A modern web browser (like Chromium)

## Setup and Installation

### 1. Configure Firebase
1.  Create a new project in the [Firebase Console](https://console.firebase.google.com/).
2.  Enable **Firestore Database** (in Test mode for setup).
3.  Enable **Cloud Storage**.
4.  Go to `Project Settings` > `Service accounts` and click **"Generate new private key"**.
5.  Save the downloaded JSON file and rename it to **`serviceAccountKey.json`**. Place this file in the root directory of your project.

### 2. Set Up the Raspberry Pi
1.  Clone this repository onto your Raspberry Pi:
    ```bash
    git clone https://github.com/Mahalaxmi2812/smart-notice-board.git
    cd smart-notice-board
    ```
2.  Install the required Python packages:
    ```bash
    pip install Flask firebase-admin google-cloud-storage werkzeug
    ```

### 3. Configure and Run the Application
1.  Open `app.py` and update the `storageBucket` URL with your Firebase project's ID. You can find this in the Firebase Storage section.
    ```python
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'your-project-id.appspot.com' 
    })
    ```
2.  Run the Flask server from the terminal:
    ```bash
    python app.py
    ```
3.  Find your Raspberry Pi's IP address by running `hostname -I`.

## Usage

1.  **To Display Notices**:
    -   On the Raspberry Pi, open a web browser and navigate to `http://<YOUR_PI_IP_ADDRESS>:5000/notice`.
    -   Set the browser to full-screen (kiosk mode) for a clean display.

2.  **To Add or Delete Notices**:
    -   On any other device (laptop, phone) on the same network, open a browser and go to `http://<YOUR_PI_IP_ADDRESS>:5000`.
    -   Use the form to submit new messages and images.
    -   Click the `×` symbol next to a message to delete it. The display will update automatically.