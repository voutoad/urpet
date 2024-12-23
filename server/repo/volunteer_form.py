from datetime import date

from server.repo.repo import BaseRepo
from server.models import db
from server.models.volunteer_form import VolunteerForm


class VolunteerFormRepo(BaseRepo):
    def create(
        self,
        name: str,
        description: str,
        email: str,
        date_of_birth: date,
        img: str,
        login: str,
    ) -> VolunteerForm:
        volunteer = VolunteerForm()
        volunteer.name = name
        volunteer.description = description
        volunteer.email = email
        volunteer.date_of_birth = date_of_birth
        volunteer.img = img
        volunteer.login = login
        self.session.add(volunteer)
        self.session.commit()
        return volunteer

    def save(self, volunteer: VolunteerForm) -> VolunteerForm:
        self.session.add(volunteer)
        self.session.commit()
        return volunteer

    def get_by_id(self, vol_id: int) -> VolunteerForm | None:
        return self.session.query(VolunteerForm).filter_by(id=vol_id).first()

    def get_by_login(self, login: str) -> VolunteerForm | None:
        return self.session.query(VolunteerForm).filter_by(login=login).first()


VOLUNTEER = VolunteerFormRepo(db.session)