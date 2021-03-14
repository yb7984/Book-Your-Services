"""Modules file for handling request related to schedule"""

from models import Schedule, Appointment, db
from flask import request, jsonify
from forms import ScheduleForm
import datetime
import json


class ScheduleHandler:
    """Handler for schedule"""

    @staticmethod
    def list(username, schedule_type="weekly", only_active=False, only_after=True):
        """Return schedule list"""
        filters = []
        filters.append(Schedule.username == username)
        if schedule_type == "weekly":
            filters.append(Schedule.date_exp.in_(
                ['0', '1', '2', '3', '4', '5', '6']))
        else:
            filters.append(Schedule.date_exp.notin_(
                ['0', '1', '2', '3', '4', '5', '6']))

            if only_after == True:
                filters.append(Schedule.date_exp >=
                               datetime.date.today().isoformat())

        if only_active == True:
            filters.append(Schedule.is_active == True)

        return Schedule.query.filter(
            *tuple(filters)).order_by(Schedule.date_exp)

    @staticmethod
    def get_available_times(username, date, appointment_id=0):
        """Return the list of available times for a provider"""

        schedule = ScheduleHandler.get(username, date.isoformat())
        if schedule is None or schedule.is_active == False:
            # no specific date, check for the weekly schedule
            weekday = date.isoweekday()
            if weekday == 7:
                weekday = 0
            schedule = ScheduleHandler.get(username, str(weekday))

        if schedule is None or schedule.is_active == False or len(schedule.schedules) == 0:
            # no defined schedule
            return []

        times = json.loads(schedule.schedules)

        return [time for time in times if Appointment.check_available(
            username,
            start=datetime.datetime.combine(date , datetime.time.fromisoformat(time["start"])),
            end=datetime.datetime.combine(date , datetime.time.fromisoformat(time["end"])),
            appointment_id=appointment_id)]

    @staticmethod
    def get(username, date_exp):
        """Return Schedule"""
        return Schedule.query.filter(Schedule.username == username, Schedule.date_exp == date_exp).first()

    @staticmethod
    def update(username):
        """update schedules"""
        form = ScheduleForm(obj=request.json, prefix="schedule")

        print(request.json)
        print(request.form)
        if form.validate():
            date_exp_weekly = form.date_exp_weekly.data
            date_exp_dates = form.date_exp_dates.data

            date_exp_dates_list = date_exp_dates.split(
                ",") if len(date_exp_dates) > 0 else []

            print(date_exp_weekly)
            print(date_exp_dates_list)

            for date in date_exp_dates_list:
                # remove dates before today
                if date < datetime.date.today().isoformat():
                    date_exp_dates_list.remove(date)

            if len(date_exp_weekly) == 0 and len(date_exp_dates_list) == 0:
                form.date_exp_weekly.errors.append(
                    "Must choose a day of the week or a specific day!")

            starts = request.form.getlist("schedule-schedules-start")
            ends = request.form.getlist("schedule-schedules-end")
            is_active = form.is_active.data

            # check data for schedule time
            print(starts)
            print(ends)

            # sort with the start time
            for i in range(len(starts)):
                for j in range(i + 1, len(starts)):
                    if starts[i] > starts[j]:
                        [starts[i], starts[j]] = [starts[j], starts[i]]
                        [ends[i], ends[j]] = [ends[j], ends[i]]

            # check end time must bigger than start time
            for i in range(len(starts)):
                if starts[i] >= ends[i]:
                    form.schedules.errors.append(
                        "Ending time must be later than starting time!")
                    break

            # check for time conflick
            for i in range(len(starts) - 1):
                if ends[i] > starts[i + 1]:
                    form.schedules.errors.append(
                        "Schedule time conflick, please check and fix it!")
                    break

            print(starts)
            print(ends)

            if len(form.errors) == 0:

                items = []

                schedules = [{"start": starts[i], "end":ends[i]}
                             for i in range(len(starts))]

                date_exps = date_exp_weekly + date_exp_dates_list

                print(date_exps)

                for date_exp in date_exps:
                    item = ScheduleHandler.get(username, date_exp)

                    if item is None:
                        item = Schedule(
                            username=username,
                            date_exp=date_exp,
                            schedules=json.dumps(schedules),
                            is_active=is_active)

                        db.session.add(item)
                    else:
                        item.schedules = json.dumps(schedules)
                        is_active = is_active

                    items.append(item)
                # try:
                db.session.commit()

                # except:
                #     db.session.rollback()
                #     # return error message
                #     return {"error": "Error when adding an schedule"}

                # # success, return new item

                print(items)
                return {"items": [item.serialize() for item in items]}

        print(form.errors)
        # return form errors
        return {"errors": form.errors}

    @staticmethod
    def delete(username, date_exp):
        """Delete Schedules"""
        schedule = ScheduleHandler.get(username, date_exp)

        if schedule is None:
            return {}

        db.session.delete(schedule)
        db.session.commit()

        return {}
