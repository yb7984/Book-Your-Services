"""Modules file for handling request related to service"""

from models import Service, Appointment, db
from flask import request, jsonify
from forms import AppointmentForm
from utils import *
from views.modules.service import ServiceHandler
from google_calendar.google_calendar import GoogleCalendarHandler
import datetime


class AppointmentHandler:
    """Handler for appointment"""

    @staticmethod
    def list(username, per_page=12):
        """Get Appointment List"""

        page = int(request.args.get("page", 1))
        is_provider = request.args.get("is_provider", "0")

        filters = []
        if is_provider == "1":
            filters.append(Appointment.provider_username == username)
        else:
            filters.append(Appointment.customer_username == username)

        filters.append(Appointment.start >= datetime.datetime.now())

        return Appointment.query.filter(
            *tuple(filters)).order_by(Appointment.start).paginate(page, per_page=per_page)

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
            start = form.start.data
            end = form.end.data
            note = form.note.data

            if provider_username == customer_username:
                return {"error": "You are not supposed to book the service from yourself!"}

            item = Appointment(
                event_id='',
                service_id=service_id,
                provider_username=provider_username,
                customer_username=customer_username,
                start=datetime.datetime.combine(service_date, start),
                end=datetime.datetime.combine(service_date, end),
                note=note
            )

            if item.check_conflict():
                # time conflict return error
                return {"error": "Appointment time is not available now. Please choose another time frame!"}

            db.session.add(item)

            db.session.commit()

            # set the google calendar event
            AppointmentHandler.set_google_calendar(item)

            # todo email to the provider and the customer
            AppointmentHandler.email(item)

            return {"item": item.serialize()}
        return {"errors": form.errors}

    @staticmethod
    def set_google_calendar(appointment):
        """Set the google calendar event for the appointment"""

        if appointment.provider.calendar_id == "" or appointment.provider.calendar_email == "":
            # provider haven't set up google calendar
            return appointment

        event = GoogleCalendarHandler.events_build(
            appointment.summary,
            appointment.start,
            appointment.end,
            description=appointment.description,
            location=appointment.address
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

        return appointment

    @staticmethod
    def email(appointment):
        """Email the notification for the appointment"""

        mail.send_message(
            subject=appointment.summary,
            sender='bobowu98@gmail.com',
            recipients=[appointment.provider.email, appointment.customer.email],
            body=f"""
                Provider: {appointment.provider.full_name}
                Customer: {appointment.customer.full_name}
                Start: {appointment.start}
                End: {appointment.end}
                Location: {appointment.location_type_name}
                Address: {appointment.address}
                Note: {appointment.note}
                """
        )
