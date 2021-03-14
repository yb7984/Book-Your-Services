from unittest import TestCase
from app import app
from utils import *
from models import *
from secrets import token_urlsafe

# Use test database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bookyourservices_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class ScheduleModelTest(TestCase):
    """Test class for Data Model"""

    def setUp(self):
        """Clean up any exists schedule and insert a test schedule"""
        User.query.delete()
        Schedule.query.delete()

        user = User.register(username="test", email="test@test.com",
                             first_name="fn", last_name="ln", password='test')
        db.session.add(user)
        db.session.commit()

        self.user = user

        schedule = Schedule(username=self.user.username, date_exp="0", schedules=json.dumps(
            [{"start": "07:00", "end": "08:00"}]
        ))
        db.session.add(schedule)
        db.session.commit()

        self.schedule = schedule

    def tearDown(self):
        """Clean up any faulted transaction."""
        db.session.rollback()

        Schedule.query.filter(Schedule.date_exp == self.schedule.date_exp,
                              Schedule.username == self.user.username).delete()
        db.session.commit()

        User.query.filter(User.username == self.user.username).delete()
        db.session.commit()

    def test_schedule_name(self):
        """Testing the schedule_name property"""
        item = self.schedule

        self.assertEqual(
            item.schedule_name, "SUNDAY")

        item = Schedule(username=self.user.username,
                        date_exp='2021-06-07', schedules='')

        self.assertEqual(
            item.schedule_name, 'Mon, 07. Jun 2021')

    def test_schedule_list(self):
        """Testing the schedule_list property"""
        list = self.schedule.schedule_list

        self.assertEqual(len(list), 1)
        self.assertEqual(list[0]["start"], "07:00")
        self.assertEqual(list[0]["end"], "08:00")

    def test_available_times(self):
        """Testing the available_times method"""
        list = self.schedule.available_times(
            datetime.date(year=2021, month=3, day=10))

        self.assertEqual(len(list), 0)

        list = self.schedule.available_times(
            datetime.date(year=2021, month=3, day=14))

        self.assertEqual(len(list), 1)
        self.assertEqual(list, [("07:00-08:00", "07:00 to 08:00")])

    def test_check_available(self):
        """Testing the available_times method"""
        available = Schedule.check_available(self.user.username,
                                        datetime.date(year=2021, month=3, day=10),
                                        {"start": "07:00", "end": "08:00"})

        self.assertEqual(available , True)

    def test_repr(self):
        """Testing the __repr method"""
        item = self.schedule

        self.assertEqual(
            item.__repr__(), f"<Schedule date_exp={item.date_exp} username={item.username}>")

    def test_serialize(self):
        """Testing the serialize method"""

        item = self.schedule

        self.assertEqual(item.serialize(), {
            "username": item.username,
            "date_exp": item.date_exp,
            "schedules": item.schedules,
            "schedule_name": item.schedule_name,
            "is_active": item.is_active
        })
