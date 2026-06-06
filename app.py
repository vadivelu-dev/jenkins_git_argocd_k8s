from flask import Flask, render_template, url_for, request, flash, redirect, jsonify, make_response
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import config
import csv
from io import StringIO

app = Flask(__name__)
app.secret_key = 'parking_app_secret_key'

# MongoDB Configuration
client = MongoClient(config.MONGODB_URI)
db = client[config.MONGODB_DB]
contacts_collection = db.contacts

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/find-parking")
def find_parking():
    location = request.args.get('location', '')
    
    if location:
        google_maps_url = f"https://www.google.com/maps/search/parking+near+{location.replace(' ', '+')}"
    else:
        google_maps_url = "https://www.google.com/maps/search/parking+near+me"
    
    return redirect(google_maps_url)

@app.route("/careers")
def careers():
    return render_template("careers.html")

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        print("Form submitted!")  # Debug print
        try:
            # Get form data
            name = request.form.get('name')
            email = request.form.get('email')
            parking_type = request.form.get('parking_type')
            message = request.form.get('message')
            
            print(f"Form data: name={name}, email={email}, parking_type={parking_type}, message={message[:50] if message else None}...")  # Debug print
            
            # Validate form data
            if not all([name, email, parking_type, message]):
                print("Validation failed - missing fields")  # Debug print
                flash('Please fill in all required fields.', 'error')
                return render_template("contact.html")
            
            # Insert data into MongoDB database
            contact_doc = {
                'name': name,
                'email': email,
                'parking_type': parking_type,
                'message': message,
                'verified': False,
                'created_at': datetime.now()
            }
            
            result = contacts_collection.insert_one(contact_doc)
            
            print("Data inserted successfully!")  # Debug print
            flash('✅ Data submitted successfully! Your message has been saved to our database. We will get back to you soon.', 'success')
            return redirect(url_for('contact'))
            
        except Exception as e:
            print(f"Error occurred: {e}")  # Debug print
            flash('An error occurred while submitting your message. Please try again.', 'error')
            print(f"Database error: {e}")  # Log error for debugging
            
    return render_template("contact.html")

@app.route("/admin/contacts")
def admin_contacts():
    """Admin route to view all contact submissions"""
    try:
        contacts = list(contacts_collection.find().sort("created_at", -1))
        return render_template("admin_contacts.html", contacts=contacts)
    except Exception as e:
        flash(f"Database error: {e}", 'error')
        return render_template("admin_contacts.html", contacts=[])

@app.route("/admin/export_contacts_csv")
def export_contacts_csv():
    """Export contact submissions to CSV file"""
    try:
        contacts = list(contacts_collection.find().sort("created_at", -1))
        
        # Create CSV content with proper encoding
        output = StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_ALL)
        
        # Write header row
        writer.writerow(['ID', 'Name', 'Email', 'Parking Type', 'Message', 'Verified', 'Submitted Date', 'Submitted Time'])
        
        # Write data rows
        for contact in contacts:
            # Format the date and time separately for better CSV compatibility
            if contact.get('created_at'):
                date_part = contact['created_at'].strftime('%Y-%m-%d')
                time_part = contact['created_at'].strftime('%H:%M:%S')
            else:
                date_part = ''
                time_part = ''
            
            # Handle verified attribute
            verified_status = 'Yes' if contact.get('verified', False) else 'No'
            
            # Clean message text to prevent CSV issues
            message_text = str(contact.get('message', '')).replace('\n', ' ').replace('\r', ' ')
            
            writer.writerow([
                str(contact['_id']),
                str(contact.get('name', '')),
                str(contact.get('email', '')),
                str(contact.get('parking_type', '')),
                message_text,
                verified_status,
                date_part,
                time_part
            ])
        
        # Create response with UTF-8 BOM for Excel compatibility
        csv_content = '\ufeff' + output.getvalue()  # Add BOM for Excel
        response = make_response(csv_content)
        response.headers['Content-Type'] = 'text/csv; charset=utf-8'
        response.headers['Content-Disposition'] = f'attachment; filename=parkeasy_contacts_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        
        return response
        
    except Exception as e:
        flash(f'Error exporting contacts: {e}', 'error')
        return redirect(url_for('admin_contacts'))

@app.route("/admin/reports")
def admin_reports():
    """Admin reports with analytics and charts"""
    try:
        # Get all contacts for analysis
        contacts = list(contacts_collection.find().sort("created_at", -1))
        
        # Generate statistics
        total_contacts = len(contacts)
        verified_contacts = len([c for c in contacts if c.get('verified', False)])
        pending_contacts = total_contacts - verified_contacts
        
        # Parking type distribution
        parking_types = {}
        for contact in contacts:
            ptype = contact.get('parking_type', 'Unknown')
            parking_types[ptype] = parking_types.get(ptype, 0) + 1
        
        # Monthly submission trends (last 6 months)
        from collections import defaultdict
        monthly_data = defaultdict(int)
        for contact in contacts:
            if contact.get('created_at'):
                month_key = contact['created_at'].strftime('%Y-%m')
                monthly_data[month_key] += 1
        
        # Sort monthly data
        sorted_months = sorted(monthly_data.items())
        
        # Daily submissions (last 7 days)
        daily_data = defaultdict(int)
        for contact in contacts:
            if contact.get('created_at'):
                # Only include last 7 days
                days_diff = (datetime.now() - contact['created_at']).days
                if days_diff <= 7:
                    day_key = contact['created_at'].strftime('%Y-%m-%d')
                    daily_data[day_key] += 1
        
        sorted_days = sorted(daily_data.items())
        
        return render_template("admin_reports.html", 
                             contacts=contacts,
                             total_contacts=total_contacts,
                             verified_contacts=verified_contacts,
                             pending_contacts=pending_contacts,
                             parking_types=parking_types,
                             monthly_data=sorted_months,
                             daily_data=sorted_days)
        
    except Exception as e:
        flash(f'Error generating reports: {e}', 'error')
        return redirect(url_for('admin_contacts'))


@app.route("/admin/verify_contact/<contact_id>", methods=['POST'])
def verify_contact(contact_id):
    """Mark a contact submission as verified"""
    try:
        print(f"Attempting to verify contact with ID: {contact_id}")  # Debug log
        
        # Validate ObjectId format
        if not ObjectId.is_valid(contact_id):
            flash('Invalid contact ID format.', 'error')
            return redirect(url_for('admin_contacts'))
        
        result = contacts_collection.update_one(
            {'_id': ObjectId(contact_id)},
            {'$set': {'verified': True}}
        )
        
        if result.modified_count > 0:
            print(f"Successfully verified contact: {contact_id}")  # Debug log
            flash('✅ Contact submission verified successfully!', 'success')
        else:
            print(f"Contact not found or already verified: {contact_id}")  # Debug log
            flash('Contact not found or already verified.', 'warning')
        
        return redirect(url_for('admin_contacts'))
            
    except Exception as e:
        print(f"Error verifying contact {contact_id}: {e}")  # Debug log
        flash(f'Error verifying contact: {e}', 'error')
        return redirect(url_for('admin_contacts'))

@app.route("/admin/delete_contact/<contact_id>", methods=['POST'])
def delete_contact(contact_id):
    """Delete a contact submission"""
    try:
        print(f"Attempting to delete contact with ID: {contact_id}")  # Debug log
        
        # Validate ObjectId format
        if not ObjectId.is_valid(contact_id):
            flash('Invalid contact ID format.', 'error')
            return redirect(url_for('admin_contacts'))
        
        result = contacts_collection.delete_one({'_id': ObjectId(contact_id)})
        
        if result.deleted_count > 0:
            print(f"Successfully deleted contact: {contact_id}")  # Debug log
            flash('🗑️ Contact submission deleted successfully!', 'success')
        else:
            print(f"Contact not found for deletion: {contact_id}")  # Debug log
            flash('Contact not found.', 'warning')
        
        return redirect(url_for('admin_contacts'))
            
    except Exception as e:
        print(f"Error deleting contact {contact_id}: {e}")  # Debug log
        flash(f'Error deleting contact: {e}', 'error')
        return redirect(url_for('admin_contacts'))

@app.route("/admin/contact_details/<contact_id>")
def contact_details(contact_id):
    """View detailed information about a specific contact submission"""
    try:
        print(f"Attempting to view contact details for ID: {contact_id}")  # Debug log
        
        # Validate ObjectId format
        if not ObjectId.is_valid(contact_id):
            flash('Invalid contact ID format.', 'error')
            return redirect(url_for('admin_contacts'))
        
        contact = contacts_collection.find_one({'_id': ObjectId(contact_id)})
        
        if contact:
            print(f"Found contact details for: {contact_id}")  # Debug log
            return render_template("contact_details.html", contact=contact)
        else:
            print(f"Contact not found: {contact_id}")  # Debug log
            flash('Contact submission not found.', 'error')
            return redirect(url_for('admin_contacts'))
    except Exception as e:
        print(f"Error retrieving contact details {contact_id}: {e}")  # Debug log
        flash(f'Database error: {e}', 'error')
        return redirect(url_for('admin_contacts'))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)