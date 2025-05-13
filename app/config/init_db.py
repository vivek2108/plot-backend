import csv
import os

from app.config.database import Base, SessionLocal, engine
from app.crud.users import get_password_hash
from app.models.users import Designations, Roles, Users
from app.models.areas import Areas
from app.models.images import Images
from app.models.plots import Plots


def read_csv(filepath: str) -> list[dict]:
    """Reads a CSV file and returns a list of dictionaries."""
    if not os.path.exists(filepath):
        print(f"CSV not found: {filepath}")
        return []
    with open(filepath, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


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
    base_path = "app/config/data"
    try:
        # Insert static roles from roles.csv
        roles_data = read_csv(f"{base_path}/roles.csv")
        for row in roles_data:
            role_name = row["name"].strip()
            if role_name and not db.query(Roles).filter_by(name=role_name).first():
                db.add(Roles(name=role_name))
        print("Inserted roles from CSV.")

        # Insert static designations from designations.csv
        designations_data = read_csv(f"{base_path}/designations.csv")
        for row in designations_data:
            title = row["title"].strip()
            if title and not db.query(Designations).filter_by(title=title).first():
                db.add(Designations(title=title))
        print("Inserted designations from CSV.")

        # Insert static areas from areas.csv
        areas_data = read_csv(f"{base_path}/areas.csv")
        for row in areas_data:
            name = row.get("name", "").strip()
            city = row.get("city", "").strip()
            state = row.get("state", "").strip()
            if name and not db.query(Areas).filter_by(name=name).first():
                db.add(Areas(name=name, city=city, state=state))
        print("Inserted areas from CSV.")

        db.commit()

        # Create initial admin user
        if not db.query(Users).filter_by(username="admin").first():
            admin_role = db.query(Roles).filter_by(name="admin").first()
            designation = db.query(Designations).filter_by(title="Chairman").first()
            if not admin_role or not designation:
                print("Cannot create admin user: Required role/designation missing.")
            else:
                admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
                admin_user = Users(
                    username="admin",
                    full_name="Admin User",
                    email="admin@example.com",
                    hashed_password=get_password_hash(admin_password),
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
