# ParkEasy - Smart Parking Solutions

ParkEasy is a comprehensive web application that helps users find convenient, secure, and affordable parking spaces in nearby areas. Built with Flask, MongoDB, and Bootstrap, it provides a modern and user-friendly interface for parking reservations and management.

## Features

- **Smart Parking Search**: Find available parking spaces near your destination
- **Multiple Parking Options**: Hourly, daily, monthly, and event parking
- **Secure Locations**: All parking areas are verified and monitored
- **Easy Booking**: Quick and simple reservation process
- **Mobile-Friendly**: Responsive design that works on all devices
- **Real-time Availability**: Live updates on parking space availability
- **24/7 Support**: Round-the-clock customer service
- **Contact Management System**: Complete contact form with database storage, verification, and admin management
- **Admin Dashboard**: Manage contact submissions with verify/delete functionality

## Database Setup

The application uses MongoDB database to store contact form submissions with verification tracking.

### Prerequisites

- MongoDB Community Server (running locally or remote)
- Python 3.7+
- Flask and required dependencies

### Setup Instructions

1. Install and start MongoDB:

   - Download MongoDB Community Server from: https://www.mongodb.com/try/download/community
   - Start MongoDB service (usually runs on mongodb://localhost:27017/)

2. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Initialize the MongoDB database:

   ```bash
   python init_mongodb.py
   ```

4. **For migrating from MySQL**: Run the migration script to transfer existing data:

   ```bash
   python migrate_mysql_to_mongodb.py
   ```

5. Run the Flask application:
   ```bash
   python app.py
   ```

### Database Configuration

The database configuration is stored in `config.py`:

- Host: localhost
- Username: root (default XAMPP)
- Password: empty (default XAMPP)
- Database: parkeasy_db

### Contact Management Features

- **Form Submission**: Users can submit contact inquiries through the contact form
- **Admin Dashboard**: View all contact submissions at `/admin/contacts`
- **Verification System**: Mark contact submissions as verified for tracking
- **Delete Functionality**: Remove spam or irrelevant submissions
- **Detailed View**: View full contact details including complete messages
- **Status Tracking**: Visual indicators for verified vs pending submissions
- **Email Integration**: Direct email reply links for easy communication

## Pages

- **Home** (`/`): Landing page with overview of services and features
- **About** (`/about`): Information about ParkEasy mission and team
- **Services** (`/services`): Detailed description of parking services and pricing
- **Careers** (`/careers`): Job opportunities and application process
- **Contact** (`/contact`): Contact form connected to MySQL database
- **Admin Dashboard** (`/admin/contacts`): Manage all contact form submissions
- **Contact Details** (`/admin/contact_details/<id>`): View detailed contact information

## Admin Features

### Contact Management Dashboard

- **View All Submissions**: Complete list of contact form submissions
- **Verification System**: Mark submissions as verified or keep as pending
- **Delete Function**: Remove unwanted or spam submissions
- **Status Tracking**: Visual badges showing verification status
- **Detailed View**: Click to see full contact details and messages
- **Email Integration**: Direct mailto links for easy responses
- **Statistics**: Total, verified, and pending submission counts

### Admin Routes

- `POST /admin/verify_contact/<id>`: Mark a contact as verified
- `POST /admin/delete_contact/<id>`: Delete a contact submission
- `GET /admin/contact_details/<id>`: View detailed contact information

## Services Offered

1. **Hourly Parking** - Perfect for short visits and quick errands
2. **Daily Parking** - Ideal for work, events, or all-day activities
3. **Monthly Parking** - Long-term solutions for residents and commuters
4. **Valet Services** - Premium parking for special events
5. **Event Parking** - Specialized arrangements for concerts and sports
6. **Secure Parking** - Enhanced security with CCTV and monitoring
7. **EV Charging** - Electric vehicle charging stations
8. **Mobile App Booking** - Easy reservations through mobile app

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Styling**: Custom CSS with Bootstrap components
- **Icons**: Bootstrap Icons
- **Animations**: AOS (Animate On Scroll)
- **Image Gallery**: GLightbox
- **Responsive Design**: Bootstrap Grid System

## Installation and Setup

1. Clone the repository
2. Install Flask: `pip install flask`
3. Navigate to the project directory
4. Run the application: `python app.py`
5. Open your browser and go to `http://localhost:5000`

## File Structure

```
Flask_with_bootstarpmade_template/
│
├── app.py                 # Main Flask application
├── templates/             # HTML templates
│   ├── index.html        # Home page
│   ├── about.html        # About page
│   ├── services.html     # Services page
│   ├── careers.html      # Careers page
│   └── contact.html      # Contact page
│
├── static/               # Static files
│   ├── css/
│   │   └── main.css      # Main stylesheet
│   ├── js/
│   │   └── main.js       # Main JavaScript
│   ├── img/              # Images and photos
│   └── vendor/           # Third-party libraries
│       ├── bootstrap/
│       ├── aos/
│       ├── glightbox/
│       └── ...
│
└── README.md            # This file
```

## Features by Page

### Home Page

- Hero section with call-to-action
- Service overview
- Statistics counter
- Featured parking locations
- Customer testimonials

### About Page

- Company mission and vision
- Team information
- Key features and benefits
- Company statistics

### Services Page

- Detailed service descriptions
- Pricing plans
- Feature comparison
- Call-to-action sections

### Careers Page

- Job opportunities
- Company culture information
- Application process
- Employee benefits

### Contact Page

- Contact form with validation
- Company contact information
- Interactive map
- FAQ section

## Contact Information

- **Phone**: +91 555 PARK-EASY (7275-3279)
- **Email**: info@parkeasy.com
- **Address**: 123 Parking Street, KR Puram, Bangalore 560036

## License

This project uses the Bootstrap template from BootstrapMade under their standard license.

---

© 2025 ParkEasy. All Rights Reserved.
