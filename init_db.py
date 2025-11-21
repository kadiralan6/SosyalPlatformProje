from app import app, db
from models import User

def init_database():
    """Initialize database with tables"""
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Check if admin user exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            # Create admin user
            admin = User(
                username='admin',
                email='admin@sabis.com',
                first_name='Admin',
                last_name='User',
                gender='other',
                birth_place='istanbul',
                school='bogazici',
                hobbies='reading,sports',
                about='Platform yöneticisi'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created (username: admin, password: admin123)")
        else:
            print("ℹ️  Admin user already exists")

if __name__ == '__main__':
    init_database()
