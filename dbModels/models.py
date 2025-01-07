from dbModels import db, app
from flask_login import UserMixin

etud_ses = db.Table(
    "seances_etudiant",
    db.Column('id_etu', db.Integer, db.ForeignKey('student.id_etu')),
    db.Column('id_ses', db.Integer, db.ForeignKey('seance.id_ses')),
    mysql_engine='InnoDB',
)

etud_abs = db.Table(
    "absence_etudiant",
    db.Column('id_etu', db.Integer, db.ForeignKey('student.id_etu')),
    db.Column('id_ses', db.Integer, db.ForeignKey('seance.id_ses')),
    db.Column('justifie', db.String(20), nullable=True),
    mysql_engine='InnoDB',
)

class User(db.Model, UserMixin):
    __table_args__ = {'mysql_engine': 'InnoDB'}
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"User('{self.id}', '{self.email}')"

class Professor(db.Model):
    __table_args__ = {'mysql_engine': 'InnoDB'}
    id_ens = db.Column(db.Integer, primary_key=True)
    nom_ens = db.Column(db.String(60), nullable=False)
    prenom_ens = db.Column(db.String(60), nullable=False)
    tel_ens = db.Column(db.String(20), unique=True, nullable=True)
    adr_ens = db.Column(db.String(20), unique=True, nullable=True)
    brth_ens = db.Column(db.DateTime, unique=True, nullable=True)
    elements = db.relationship('Element', backref='professor')
    id_dept = db.Column(db.Integer, db.ForeignKey('department.id_dep'))

    def __repr__(self):
        return f"Professor('{self.id_ens}', '{self.nom_ens}', '{self.prenom_ens}')"

class Student(db.Model):
    __table_args__ = {'mysql_engine': 'InnoDB'}
    id_etu = db.Column(db.Integer, primary_key=True)
    nom_etu = db.Column(db.String(60), nullable=False)
    prenom_etu = db.Column(db.String(60), nullable=False)
    tel_etu = db.Column(db.String(20), unique=True, nullable=True)
    adr_etu = db.Column(db.String(20), unique=True, nullable=True)
    brth_etu = db.Column(db.DateTime, unique=True, nullable=True)
    id_sem = db.Column(db.Integer, db.ForeignKey('semestre.id_sem'))
    insrit = db.relationship('Seance', secondary=etud_ses, backref='etudiant_ses')
    absenter = db.relationship('Seance', secondary=etud_abs, backref='etudiant_abs')


    def __repr__(self):
        return f"Student('{self.id_etu}', '{self.nom_etu}', '{self.prenom_etu}')"

class Admin(db.Model):
    __table_args__ = {'mysql_engine': 'InnoDB'}
    id_adm = db.Column(db.Integer, primary_key=True)
    nom_adm = db.Column(db.String(60), nullable=False)
    prenom_adm = db.Column(db.String(60), nullable=False)
    tel_adm = db.Column(db.String(20), unique=True, nullable=True)

    def __repr__(self):
        return f"Admin('{self.id_adm}', '{self.nom_adm}', '{self.prenom_adm}')"

class Element(db.Model):
    __table_args__ = {'mysql_engine': 'InnoDB'}
    id_elem = db.Column(db.Integer, primary_key=True)
    nom_elem = db.Column(db.String(60), nullable=False)
    id_ens = db.Column(db.Integer, db.ForeignKey('professor.id_ens'))
    seances = db.relationship('Seance', backref='element')
    id_mod = db.Column(db.Integer, db.ForeignKey('module.id_mod'))

    def __repr__(self):
        return f"Element('{self.id_elem}', '{self.nom_elem}')"

class Module(db.Model):
    __table_args__ = {'mysql_engine': 'InnoDB'}
    id_mod = db.Column(db.Integer, primary_key=True)
    nom_mod = db.Column(db.String(60), nullable=False)
    id_sem = db.Column(db.Integer, db.ForeignKey('semestre.id_sem'))
    elements = db.relationship('Element', backref='module')

    def __repr__(self):
        return f"Module('{self.id_mod}', '{self.nom_mod}')"

class Filiere(db.Model):
    __table_args__ = {'mysql_engine': 'InnoDB'}
    id_fil = db.Column(db.Integer, primary_key=True)
    nom_fil = db.Column(db.String(60), nullable=False)
    id_dept = db.Column(db.Integer, db.ForeignKey('department.id_dep'))
    semestres = db.relationship('Semestre', backref='filiere')

    def __repr__(self):
        return f"Filiere('{self.id_fil}', '{self.nom_fil}')"

class Department(db.Model):
    __table_args__ = {'mysql_engine': 'InnoDB'}
    id_dep = db.Column(db.Integer, primary_key=True)
    nom_dep = db.Column(db.String(60), nullable=False)
    professors = db.relationship('Professor', backref='department')
    filieres = db.relationship('Filiere', backref='department')

    def __repr__(self):
        return f"Department('{self.id_dep}', '{self.nom_dep}')"

class Semestre(db.Model):
    __table_args__ = {'mysql_engine': 'InnoDB'}
    id_sem = db.Column(db.Integer, primary_key=True)
    nom_sem = db.Column(db.String(60), nullable=False)
    id_fil = db.Column(db.Integer, db.ForeignKey('filiere.id_fil'))
    modules = db.relationship('Module', backref='semestre')
    etudiants = db.relationship('Student', backref='semestre')


    def __repr__(self):
        return f"Department('{self.id_sem}', '{self.nom_sem}')"

class Seance(db.Model):
    __table_args__ = {'mysql_engine': 'InnoDB'}
    id_ses = db.Column(db.Integer, primary_key=True)
    date_ses = db.Column(db.DateTime, nullable=False)
    debut_sess = db.Column(db.Time, nullable=False)
    fin_sess = db.Column(db.Time, nullable=False)
    id_elem = db.Column(db.Integer, db.ForeignKey('element.id_elem'))

    def __repr__(self):
        return f"Seance('{self.id_ses}', '{self.date_ses}', '{self.debut_sess}', '{self.fin_sess}')"
