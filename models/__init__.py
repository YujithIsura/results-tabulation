from datetime import datetime
from config import db, ma
from sqlalchemy.orm import relationship


class Person(db.Model):
    __tablename__ = 'person'
    person_id = db.Column(db.Integer, primary_key=True)
    lname = db.Column(db.String(32), index=True)
    fname = db.Column(db.String(32))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Election(db.Model):
    __tablename__ = 'election'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)


class Office(db.Model):
    __tablename__ = 'office'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    electionId = db.Column(db.Integer, db.ForeignKey("election.id"))

    election = relationship("Election", foreign_keys=[electionId])


class Electorate(db.Model):
    __tablename__ = 'electorate'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    electionId = db.Column(db.Integer, db.ForeignKey("election.id"))


class Party(db.Model):
    __tablename__ = 'party'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(100), index=True)


class TallySheet(db.Model):
    __tablename__ = 'tallySheet'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(10), index=True)
    electionId = db.Column(db.Integer, db.ForeignKey("election.id"))
    officeId = db.Column(db.Integer, db.ForeignKey("office.id"))
    latestVersionId = db.Column(db.Integer, db.ForeignKey("tallySheet_version.id"))

    election = relationship("Election", foreign_keys=[electionId], lazy='joined')
    office = relationship("Office", foreign_keys=[officeId], lazy='joined')
    latestVersion = relationship("TallySheetVersion", foreign_keys=[latestVersionId])


class TallySheetVersion(db.Model):
    __tablename__ = 'tallySheet_version'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.id"))

    createdBy = db.Column(db.Integer)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TallySheet_PRE_41(db.Model):
    __tablename__ = 'tallySheet_PRE-41'
    tallySheetVersionId = db.Column(db.Integer, db.ForeignKey("tallySheet_version.id"), primary_key=True)
    tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet_version.tallySheetId"))
    electoralDistrictId = db.Column(db.Integer, db.ForeignKey("office.id"))
    pollingDivisionId = db.Column(db.Integer, db.ForeignKey("office.id"))
    countingCentreId = db.Column(db.Integer, db.ForeignKey("office.id"))


class TallySheet_PRE_41__party(db.Model):
    __tablename__ = 'tallySheet_PRE-41__party'
    tallySheetVersionId = db.Column(db.Integer, db.ForeignKey("tallySheet_version.id"), primary_key=True)
    partyId = db.Column(db.Integer, db.ForeignKey("party.id"), primary_key=True)
    voteCount = db.Column(db.Integer)


# class TallySheet_PRE_34_CO(db.Model):
#     __tablename__ = 'tallySheet_PRE-34-CO'
#     tallySheetVersionId = db.Column(db.Integer, db.ForeignKey("tallySheet_version.id"), primary_key=True)
#     tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet_version.tallySheetId"))
#     electoralDistrictId = db.Column(db.Integer, db.ForeignKey("office.id"))
#     pollingDivisionId = db.Column(db.Integer, db.ForeignKey("office.id"))
#     countingCentreId = db.Column(db.Integer, db.ForeignKey("office.id"))
#
#
# class TallySheet_PRE_34_CO__candidate(db.Model):
#     __tablename__ = 'tallySheet_PRE-34-CO__candidate'
#     tallySheetVersionId = db.Column(db.Integer, db.ForeignKey("tallySheet_version.id"), primary_key=True)
#     candidateId = db.Column(db.Integer, db.ForeignKey("candidate.id"), primary_key=True)
#     candidateId = db.Column(db.Integer, db.ForeignKey("candidate.id"), primary_key=True)
#     voteCount = db.Column(db.Integer)


ModelSchema = ma.ModelSchema
