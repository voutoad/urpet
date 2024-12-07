from datetime import date

from repo import BaseRepo
from server.models.database import db
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

    def get_by_id(self, vol_id: int) -> VolunteerForm | None:
        return self.session.query(VolunteerForm).filter_by(id=vol_id).first()


VOLUNTEER = VolunteerFormRepo(db.session)