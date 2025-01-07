# Social Media API

This project is a RESTful API built using Django and Django REST Framework (DRF). It simulates the functionality of a social media platform where users can create posts, follow other users, view their feed, and perform other related tasks. The API supports CRUD operations for users and posts, user authentication, and a follow system, all while ensuring a clean and efficient backend design.

## Features

- **User Management**: Users can register, log in, and manage their profiles.
- **Post Management**: Users can create, read, update, and delete posts.
- **Follow System**: Users can follow and unfollow other users.
- **Feed of Posts**: Users can view a feed of posts from the users they follow.
- **Authentication**: Users must authenticate to interact with the system.
- **Pagination**: Post feed is paginated for efficient data loading.
  
Optional Features (Stretch Goals):

- Likes and Comments on posts
- Notifications for followers, likes, and comments
- Direct messaging between users
- Post sharing and reposting
- Hashtags and mentions
- Trending posts based on likes or reposts
- Profile Customization
- Media uploads (images, videos)

## Technologies Used

- **Backend**: Django, Django REST Framework (DRF)
- **Database**: SQLite (can be changed to PostgreSQL or MySQL for production)
- **Authentication**: Django's built-in authentication system, optionally JWT for token-based authentication
- **Deployment**: Heroku (or PythonAnywhere for deployment)
  
## Requirements

- Python 3.8+
- Django 3.x or above
- Django REST Framework
- PostgreSQL or SQLite (for development)
- Git (for version control)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Israa-Hassanein/social_media_api.git
cd social-media-api


