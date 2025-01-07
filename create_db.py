from app_pack import db, app
from app_pack.models import User, Professor, Student, Admin, Element, Module, Filiere, Department, Semestre, Seance, etud_abs, etud_ses

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
