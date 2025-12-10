# Social Network Web App

A Threads-like social platform where users can create posts, follow other users, and interact through likes. 
This project was developed as part of the CS50 Web Programming course using Django, JavaScript, and Bootstrap.

---

**Video Overview:** https://youtu.be/UceT2uk_4-k

---

## Features

### Create & Interact
- Users can create text-based posts.
- Like and unlike posts with instant, asynchronous updates.
- Edit your own posts in place without reloading the page.

### User Profiles
- View any user’s profile page.
- Shows follower/following counts and all posts by that user.
- Follow or unfollow other users (authenticated users only).

### Feeds
- **All Posts:** Displays every post in reverse chronological order.
- **Following Feed:** Shows posts from users you follow.

### Pagination
- Posts are displayed 10 per page.
- Includes Next/Previous navigation to browse older or newer posts.

---

## Technologies Used
- **Python**
- **Django**
- **SQLite**
- **JavaScript**
- **HTML5**
- **CSS3**
- **Bootstrap**
- **RESTful APIs (fetch for asynchronous updates)**

---

## Installation

1. **Clone the repository**
     git clone https://github.com/saraccmululo/social-network-app.git
     cd social-network-app
2. **Install dependencies**
     pip install -r requirements.txt
3. **Run database migrations**
     python manage.py migrate
4. **Start the development server**
     python manage.py runserver
5. Open your browser at:
     http://127.0.0.1:8000/

---

