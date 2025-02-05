# 🏯 Georgian Cities Explorer  

## About the Program  
This program features locations across cities in Georgia, helping users explore and discover new places. If someone is in a particular city and doesn’t know what to visit, they can use this site to learn about available locations. Essentially, it is a platform for those interested in traveling and exploring cities more deeply.  

---

## 🚀 Features  

### 👤📱 User APP  
- **User Registration:** Users receive an email verification link to activate their account.  
- **Profile Management:** Update profile details, reset passwords, and delete accounts.  

### 🏞️ Main APP  
- **Browse Locations:** Search, filter, and paginate locations.  
- **Authenticated User Actions:** Rate locations, comment, like/reply to comments.  
- **Popular Locations:** View most visited locations based on daily unique visits.  
- **Traveler Map AI (Subscription Required):** AI-generated itinerary for travel planning.  

### ⭐❤️ Favorites App  
- **Save and manage favorite locations.**  

### ⏰📧 RemindMe APP  
- **Set reminders for location visits** with weather forecasts and operational hours validation.  

### 🗳️👍 Votes App  
- **Users vote for new locations to be added.**  

### 💳📅 Subscription App  
- **Paid subscriptions unlock the AI-powered Traveler Map feature.**  

---

## 🛠️ Tech Stack  
- **Framework:** Django REST Framework  
- **Database:** PostgreSQL  
- **Task Queue:** Celery with Redis  

---

## 📝 API Documentation  
Swagger documentation is available:  
📌 **URL:** `http://localhost:8000/swagger/`  

Features:  
- **Endpoint Details:** Request methods, parameters, responses.  
- **Try It Out:** Test API requests directly.  

---

## 🚀 How to Run the Project with Docker  

### 1️⃣ Clone the Repository  
```sh
git clone https://github.com/gioms101/georgian_city_explorer.git
cd georgian_city_explorer
```

### 2️⃣ Create a `.env` File  
Create a `.env` file in the project root with the following environment variables:  
```env
SECRET_KEY=
DEBUG=
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
EMAIL_HOST=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_PORT=
AI_API_KEY=
WEATHER_API_KEY=
PAYPAL_CLIENT_ID=
PAYPAL_CLIENT_SECRET=
```

### 3️⃣ Build and Start Containers  
Run the following command to build and start the Docker containers:  
```sh
docker compose up --build -d
```
This will start the following services:  
👉 **PostgreSQL** (database)  
👉 **Redis** (task queue backend)  
👉 **Django Web App**  
👉 **Celery & Celery Beat**  

### 4️⃣ Create a Superuser  
To access the **Django Admin Panel**, create a superuser:  
```sh
docker exec -it <container_id_or_name> python manage.py createsuperuser
```
Follow the prompts to set up a **username, email, and password**.

### 5️ Access the Application  
- 🌍 **Website:** `http://localhost:8000/`  
- 🛠️ **Admin Panel:** `http://localhost:8000/admin/`  

---

## 📌 Useful Docker Commands  

### 🔍 Check Running Containers  
```sh
docker ps
```

### 🛠️ Stop Containers  
```sh
docker compose down
```

### 🗑️ Remove Unused Images  
```sh
docker rmi -f $(docker images -q)
```

---

