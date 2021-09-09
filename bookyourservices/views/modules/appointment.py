"""Modules file for handling request related to service"""

from models import Service, Appointment, db
from flask import request, jsonify
from forms import AppointmentForm
from utils import *
from views.modules.service import ServiceHandler
from google_calendar.google_calendar import GoogleCalendarHandler
import datetime
import config


class AppointmentHandler:
    """Handler for appointment"""

    @staticmethod
    def list(username, per_page=12):
        """Get Appointment List"""

        page = int(request.args.get("page", 1))
        is_provider = request.args.get("is_provider", "0")
        is_past = request.args.get("is_past", "0")

        filters = []
        orders = []
        if is_provider == "1":
            filters.append(Appointment.provider_username == username)
        else:
            filters.append(Appointment.customer_username == username)

        if is_past == "1":
            # pass appointments
            filters.append(Appointment.start < datetime.datetime.now())
            orders.append(Appointment.start.desc())
        else:
            # upcoming appointments
            filters.append(Appointment.start >= datetime.datetime.now())
            orders.append(Appointment.start)

        filters.append(Appointment.is_active == True)

        return Appointment.query.filter(
            *tuple(filters)).order_by(*tuple(orders)).paginate(page, per_page=per_page)

    @staticmethod
    def insert(username):
        """New Appointment"""
        form = AppointmentForm(obj=request.json, prefix="appointment")

        if form.validate():
            event_id = ''
            service_id = form.service_id.data
            provider_username = form.provider_username.data
            customer_username = login_username()
            service_date = form.service_date.data
            times = form.times.data
            note = form.note.data

            if provider_username == customer_username:
                return {"error": "You are not supposed to book the service from yourself!"}

            if len(times) == 0:
                form.times.errors.append("Must select an appointment time!")

            [start, end] = times.split("-")

            item = Appointment(
                event_id='',
                service_id=service_id,
                provider_username=provider_username,
                customer_username=customer_username,
                start=datetime.datetime.combine(
                    service_date, datetime.time.fromisoformat(start)),
                end=datetime.datetime.combine(
                    service_date, datetime.time.fromisoformat(end)),
                note=note
            )

            if not item.available:
                # time conflict return error
                return {"error": "Selected appointment time is not available now. Please choose another time frame!"}

            if len(form.errors) == 0:

                db.session.add(item)
                db.session.commit()

                # set the google calendar event
                AppointmentHandler.set_google_calendar(item)

                # todo email to the provider and the customer
                AppointmentHandler.email(item)

                return {"item": item.serialize()}
        return {"errors": form.errors}

    @staticmethod
    def update(username, appointment_id):
        """Update Appointment"""
        form = AppointmentForm(obj=request.json, prefix="appointment")

        item = Appointment.query.get(appointment_id)

        if item is None:
            return {"error", "Error when updating appointment!"}

        if login_admin_username() is None and item.customer_username != username and item.provider_username != username:
            return {"error", "Unauthorized visit!"}

        if form.validate():
            service_date = form.service_date.data
            times = form.times.data
            note = form.note.data

            if len(times) == 0:
                form.times.errors.append("Must select an appointment time!")

            [start, end] = times.split("-")

            item.start = datetime.datetime.combine(
                service_date, datetime.time.fromisoformat(start))
            item.end = datetime.datetime.combine(
                service_date, datetime.time.fromisoformat(end))
            item.note = note

            if not item.available:
                # time conflict return error
                return {"error": "Selected appointment time is not available now. Please choose another time frame!"}

            if len(form.errors) == 0:
                db.session.commit()

                # set the google calendar event
                AppointmentHandler.set_google_calendar(item)

                # email to the provider and the customer
                AppointmentHandler.email(item, action="Updated")

                return {"item": item.serialize()}
        return {"errors": form.errors}

    @staticmethod
    def delete(username, appointment_id):
        """Delete Appointment"""
        item = Appointment.query.get(appointment_id)

        if item is None:
            return {}

        if login_admin_username() is None and item.customer_username != username and item.provider_username != username:
            return {"error", "Unauthorized visit!"}

        item.is_active = False

        # set the google calendar event
        AppointmentHandler.set_google_calendar(item)

        # email to the provider and the customer
        AppointmentHandler.email(item, action="Deleted")

        db.session.commit()

        return {}

    @staticmethod
    def set_google_calendar(appointment):
        """Set the google calendar event for the appointment"""

        if is_testing():
            # return if is testing
            return appointment

        if appointment.provider.calendar_id == "" or appointment.provider.calendar_email == "":
            # provider haven't set up google calendar
            return appointment

        if appointment.is_active == True:
            event = GoogleCalendarHandler.events_build(
                appointment.summary,
                appointment.start,
                appointment.end,
                description=appointment.description,
                location=""
            )

            if appointment.event_id != "":
                # update
                event["id"] = appointment.event_id
                event = GoogleCalendarHandler.events_update(
                    event, appointment.provider.calendar_id)
            else:
                event = GoogleCalendarHandler.events_insert(
                    event, appointment.provider.calendar_id)

            if event["id"]:
                appointment.event_id = event["id"]

                # update the database
                db.session.commit()
        else:
            # delete the event
            if appointment.event_id != "":
                GoogleCalendarHandler.events_delete(
                    event_id=appointment.event_id, calendar_id=appointment.provider.calendar_id)

            appointment.event_id = ""
            db.session.commit()

        return appointment

    @staticmethod
    def email(appointment, action="new"):
        """Email the notification for the appointment"""
        if not is_testing():
            # send email if not testing
            mail.send_message(
                subject=f"{ action.upper() }:{ appointment.summary }",
                sender=config.MAIL_SENDER,
                recipients=[appointment.provider.email,
                            appointment.customer.email],
                body=f"""
                    Provider: {appointment.provider.full_name}
                    Customer: {appointment.customer.full_name}
                    Start: {appointment.start}
                    End: {appointment.end}
                    Note: {appointment.note}
                    """
            )
