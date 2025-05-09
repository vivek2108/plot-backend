from app.config.database import Base, SessionLocal, engine
from app.crud.users import get_password_hash
from app.models.users import Designations, Roles, Users


def init():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Static Roles
        roles = ["admin", "manager", "employee"]
        for role_name in roles:
            if not db.query(Roles).filter_by(name=role_name).first():
                db.add(Roles(name=role_name))

        # Static Designations
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

        db.commit()

        # Create initial admin user with role and designation
        if not db.query(Users).filter_by(username="admin").first():
            admin_role = db.query(Roles).filter_by(name="admin").first()
            designation = db.query(Designations).filter_by(title="Chairman").first()

            admin = Users(
                username="admin",
                full_name="admin user",
                email="admin@example.com",
                hashed_password=get_password_hash(
                    "admin123"
                ),  # Use hash in real project
                role_id=admin_role.id,
                designation_id=designation.id,
                created_by="admin",
                updated_by="admin",
            )
            db.add(admin)
            db.commit()
            print("Inserted initial admin user.")

    finally:
        db.close()


if __name__ == "__main__":
    init()
