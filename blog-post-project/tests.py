from main import app, db, User

def delete_all_users():
    with app.app_context():
        try:
            num_rows_deleted = db.session.query(User).delete()
            db.session.commit()
            print(f"Deleted {num_rows_deleted} users.")
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting users: {e}")


# def recreate_user_table():
#     with app.app_context():
#         try:
#             # Drop the User table if it exists
#             User.__table__.drop(db.engine, checkfirst=True)
#             print("User table dropped.")
#             # Create the User table
#             User.__table__.create(db.engine)
#             print("User table created.")
#             db.session.commit() # Commit changes if any (though create/drop are often DDL and auto-commit)
#         except Exception as e:
#             db.session.rollback()
#             print(f"Error recreating User table: {e}")

# if __name__ == '__main__':
    # recreate_user_table()
if __name__ == '__main__':
    delete_all_users()
