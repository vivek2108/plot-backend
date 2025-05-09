from app.config.database import Base, SessionLocal, engine
from app.crud.users import get_password_hash
from app.models.users import Designations, Roles, Users


def init() -> None:
    """
    Initializes the database:
    - Creates all tables
    - Inserts static roles and designations
    - Creates an initial admin user (if not present)
    """
    print("Creating tables if they do not exist...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Insert static roles
        roles = ["admin", "manager", "employee"]
        for role_name in roles:
            if not db.query(Roles).filter_by(name=role_name).first():
                db.add(Roles(name=role_name))
        print("Inserted default roles.")

        # Insert static designations
        designations = [
            "Chairman",
            "Executive Director",
            "Managing Director",
            "Director",
            "Senior Associate",
            "Associate",
        ]
        for title in designations:
            if not db.query(Designations).filter_by(title=title).first():
                db.add(Designations(title=title))
        print("Inserted default designations.")

        db.commit()

        # Create initial admin user
        if not db.query(Users).filter_by(username="admin").first():
            admin_role = db.query(Roles).filter_by(name="admin").first()
            designation = db.query(Designations).filter_by(title="Chairman").first()

            admin_user = Users(
                username="admin",
                full_name="Admin User",
                email="admin@example.com",
                hashed_password=get_password_hash("admin123"),  # Use env-var in prod
                role_id=admin_role.id,
                designation_id=designation.id,
                created_by="system",
                updated_by="system",
            )
            db.add(admin_user)
            db.commit()
            print("Inserted initial admin user.")
        else:
            print("Admin user already exists.")
    finally:
        db.close()
        print("DB initialization complete.")


if __name__ == "__main__":
    init()
