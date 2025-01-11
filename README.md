## 🗺️ Georgian Cities Explorer

## About the Program:
This program features locations across cities in Georgia, designed to help users explore and discover new places. If someone is in a particular city and doesn’t know what to visit, they can use this site to learn about available locations. Essentially, it is a platform for those interested in traveling and exploring cities more deeply.


## 🚀 Features  

### **User APP**  
- **User Registration**:  
  Users can register on the site. After successful registration, they receive a verification link via email to activate their account.  
- **Profile Management**:  
  Authenticated users can:  
  - Update their profile picture, name, password, or email.  
  - Users can reset their password in case of forgetting. 
  - Delete their account.  
  - Reverify their email when updated.  

### **Main APP**  
- **Browse Locations**:  
  - Explore locations across Georgia.  
  - Filter by city or category.  
  - Search for specific locations.  
  - Enjoy pagination with 5 locations per page.  
- **Authenticated User Actions**:  
  - Rate locations (1–5 stars) and update/remove ratings.  
  - Comment on locations to share impressions or give advice.  
  - Like, reply to, edit, or delete comments.  
- **Popular Locations**:  
  - View the most visited locations of the day, based on unique authenticated/anonymous user visits.  
- **Traveler Map AI**: (This is only for users who have active subscription)
  - Plan your day by entering a city name and selecting a preferred language (English or Georgian).  
  - Traveler Map AI: Users who are unsure where to go or how to plan their day can use this feature. By entering a city name and selecting a language &#40;English or Georgian&#41;, they receive a suggested itinerary. The AI only includes locations already added to the program, and if multiple locations belong to the same category, only one is included in the response.

### **Favorites App**
- Add locations to your personal favorite list.
- Remove locations from the favorite list at any time.
- This is possible for both Anonymous and Authorized users.


### **RemindMe APP**  
- **Set Reminders**:  
  - Plan visits by setting a reminder with date and time.  
  - Receive email reminders one hour before the visit, including weather forecasts.
  - Validate the operational hours of the location to ensure it is open during the selected time.
  - If the location is closed, users receive a message to select a valid time.
- **Manage Reminders**:
 - Update or delete reminders.
- Deleted reminders ensure no further emails are sent.
### Votes App:
- When the site administrator wants to update the program by adding new locations, they can involve users in the process.
- The administrator adds proposed locations, and users can vote for or against them.
- If a location receives a predetermined number of votes, it is automatically added to the program, and users can view its details.

### Subscription App:
- User can purchase one of subscription to have access to special feature of program (Generating Traveler Map).


## 🛠️ Tech Stack  
- **Framework**: Django REST Framework   
- **Database**: PostgreSQL
- **Task Queue**: Celery with Redis

## 📄 API Documentation
This project includes an interactive API documentation powered by Swagger. You can explore all the endpoints, test requests, and view responses directly from your browser

### Access Swagger Documentation

- URL: http://localhost:8000/swagger/
- **The documentation provides**:
 - Endpoint Details: Request methods, parameters, and responses.
 - Try It Out: Test API requests in real time.