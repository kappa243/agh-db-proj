# FlaskPlayer
The project for Databases Course at AGH UST.
Created by Szymon Idec & Karol Śliwa.

### About
Our application is used to play music. To access the application, you need to register and then log in to the created account. The user can play songs on the main page, as well as create his own public or private playlists. They can also search for tracks, artists and public playlists of other users, which they can follow to access them quickly. A user who has administrator rights has access to the admin panel, from which he can edit and delete other users.

### Technology used in the project:
- **PostgreSQL** - core database used by application
- **Flask** (with Jinja2) - backend framework with web template engine
- **Flask-SQLAlchemy** - Flask's extension that adds support for SQLAlchemy (ORM)
- **Flask-Migrate** - extension that handles SQLAlchemy database migrations