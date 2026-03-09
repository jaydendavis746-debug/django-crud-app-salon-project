<img width="1917" height="943" alt="image" src="https://github.com/user-attachments/assets/e3ad6c44-cd6c-47aa-be3f-e3d33a7a4be3" />


---
The deployed app is available at [FirstLook](https://firstlook-salon-3904214644a9.herokuapp.com/)  
The project planning board can be viewed on [Trello](https://trello.com/b/gtSoMGov/django-project).


# **FirstLook — Luxury Salon Booking Platform**

FirstLook is a full‑stack salon management platform built with Django, designed to deliver a premium, editorial‑grade beauty experience. It blends a luxury brand identity with a robust booking engine, stylist dashboards, availability management, and a cohesive glass‑UI design system. The platform supports both clients and stylists, offering a seamless end‑to‑end workflow from discovery to appointment completion.

---

### ✨ Features

#### **Client Experience**
- Editorial‑inspired homepage with glowing hero titles and animated gradients  
- Service browsing with premium card layouts  
- Real‑time stylist availability  
- Smooth booking flow with date/time pickers  
- Booking detail pages styled with frosted‑glass panels  
- Account creation, login, and profile management  

#### **Stylist Dashboard**
- Personalised dashboard for each stylist  
- Create, update, and delete availability slots  
- Automatic locking of booked availability  
- Manage bookings and reschedule appointments  
- CRUD management for services, availability, and bookings  
- Unified design system across all dashboard pages  

#### **Brand & UI System**
- FL monogram and luxury wordmark  
- Frosted‑glass surfaces with blur and soft shadows  
- Animated underline interactions  
- Button micro‑interactions (lift, glow, shadow transitions)  
- Responsive layouts across all devices  
- Editorial typography and spacing  

#### **Technical**
- Django backend with relational models  
- Django ORM for services, stylists, bookings, and availability  
- Custom template system with reusable components  
- Global CSS design system for consistent styling  

---

### 🧱 Tech Stack

- **Backend:** Django, Python  
- **Database:** PostgreSQL (local or cloud)  
- **Frontend:** HTML, Django Templates, CSS  
- **Version Control:** Git + GitHub  


### 🗂️ Project Structure

```
firstlook/
│
├── salon/               # Core project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── main_app/                   # Main app: services, stylists, bookings
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── templates/salon/
│
├── static/                  # Global CSS, images, brand assets
│   └── base.css
│
├── templates/               # Shared templates
│   └── base.html
│
└── manage.py
```

---

### 🎨 Brand Identity

FirstLook’s visual identity draws inspiration from high‑fashion beauty brands. The UI uses:

-  wordmark  
- Frosted glass surfaces  
- Soft glows and gradients  
- Editorial typography  
- Intentional micro‑interactions  
- Clean, modern spacing  

This creates a premium, memorable experience that elevates the salon’s digital presence.

---

### 🔮 Future editions

- Client booking history  
- Email confirmations  
- Stripe integration for deposits  
- Multi‑stylist service selection  
- Admin analytics dashboard  
- Dark mode  

---



---

If you want, I can also generate a **shorter GitHub‑friendly version**, a **portfolio‑optimized version**, or a **branding showcase section** that highlights your FL monogram and design system.
