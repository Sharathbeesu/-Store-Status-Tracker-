from flask import Flask, request, jsonify
import csv
import datetime
import pytz
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
Base = declarative_base()

# Database configuration
engine = create_engine("sqlite:///loop_task.db", echo=True)
Session = sessionmaker(bind=engine)
session = Session()


# Define the database model for Store
class Store(Base):
    __tablename__ = "menu"
    store_id = Column(Integer, primary_key=True)
    timezone_str = Column(String)
    business_hours = Column(String)


# Define the database model for StoreStatus
class StoreStatus(Base):
    __tablename__ = "store_status"
    id = Column(Integer, primary_key=True)
    store_id = Column(Integer)
    timestamp_utc = Column(DateTime)
    status = Column(String)


# Define the database model for Report
class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True)
    report_id = Column(String)
    data = Column(String)


# Create the database tables if they don't exist
Base.metadata.create_all(engine)


@app.route("/trigger_report", methods=["POST"])
def trigger_report():
    # Get all stores from the database
    stores = session.query(Store).all()
    print("stores")
    report_data = []

    # Iterate over each store
    for store in stores:
        store_id = store.store_id
        timezone_str = store.timezone_str
        print(store_id)
    #     # Get the store's business hours
    #     business_hours = store.business_hours.split(",")

    #     # Convert business hours to datetime objects
    #     business_hours = [
    #         datetime.datetime.strptime(time, "%H:%M") for time in business_hours
    #     ]

    #     # Get the start and end times for business hours
    #     start_time_local = business_hours[0].time()
    #     end_time_local = business_hours[1].time()

    #     # Get the current timestamp in UTC
    #     current_time_utc = datetime.datetime.now(pytz.utc)

    #     # Get the start and end times for the last hour, day, and week
    #     start_time_last_hour = current_time_utc - datetime.timedelta(hours=1)
    #     start_time_last_day = current_time_utc - datetime.timedelta(days=1)
    #     start_time_last_week = current_time_utc - datetime.timedelta(weeks=1)

    #     # Get store statuses within the last hour, day, and week
    #     statuses_last_hour = (
    #         session.query(StoreStatus)
    #         .filter(
    #             StoreStatus.store_id == store_id,
    #             StoreStatus.timestamp_utc >= start_time_last_hour,
    #             StoreStatus.timestamp_utc <= current_time_utc,
    #         )
    #         .all()
    #     )

    #     statuses_last_day = (
    #         session.query(StoreStatus)
    #         .filter(
    #             StoreStatus.store_id == store_id,
    #             StoreStatus.timestamp_utc >= start_time_last_day,
    #             StoreStatus.timestamp_utc <= current_time_utc,
    #         )
    #         .all()
    #     )

    #     statuses_last_week = (
    #         session.query(StoreStatus)
    #         .filter(
    #             StoreStatus.store_id == store_id,
    #             StoreStatus.timestamp_utc >= start_time_last_week,
    #             StoreStatus.timestamp_utc <= current_time_utc,
    #         )
    #         .all()
    #     )

    #     # Compute the uptime and downtime
    #     uptime_last_hour, downtime_last_hour = compute_uptime_downtime(
    #         statuses_last_hour,
    #         start_time_last_hour,
    #         current_time_utc,
    #         start_time_local,
    #         end_time_local,
    #         timezone_str,
    #     )
    #     uptime_last_day, downtime_last_day = compute_uptime_downtime(
    #         statuses_last_day,
    #         start_time_last_day,
    #         current_time_utc,
    #         start_time_local,
    #         end_time_local,
    #         timezone_str,
    #     )
    #     uptime_last_week, downtime_last_week = compute_uptime_downtime(
    #         statuses_last_week,
    #         start_time_last_week,
    #         current_time_utc,
    #         start_time_local,
    #         end_time_local,
    #         timezone_str,
    #     )

    #     # Append the store's report data
    #     report_data.append(
    #         {
    #             "store_id": store_id,
    #             "uptime_last_hour": uptime_last_hour.total_seconds() // 60,
    #             "uptime_last_day": uptime_last_day.total_seconds() // 3600,
    #             "update_last_week": uptime_last_week.total_seconds() // 3600,
    #             "downtime_last_hour": downtime_last_hour.total_seconds() // 60,
    #             "downtime_last_day": downtime_last_day.total_seconds() // 3600,
    #             "downtime_last_week": downtime_last_week.total_seconds() // 3600,
    #         }
    #     )

    # # Generate report ID (you can use a random string generation library here)
    # report_id = "hello"

    # # Store the report data in the database
    # report = Report(report_id=report_id, data=str(report_data))
    # session.add(report)
    # session.commit()

    # # Save the report data to a CSV file
    # save_report_data_to_csv(report_data, report_id)

    # return jsonify({"report_id": report_id})


@app.route("/get_report", methods=["GET"])
def get_report():
    report_id = request.args.get("report_id")

    report = session.query(Report).filter(Report.report_id == report_id).first()

    if report:
        return jsonify({"status": "Complete", "report_data": report.data})

    return jsonify({"status": "Running"})


def compute_uptime_downtime(
    statuses, start_time, end_time, start_time_local, end_time_local, timezone_str
):
    timezone = pytz.timezone(timezone_str)

    uptime = datetime.timedelta()
    downtime = datetime.timedelta()

    prev_status = None

    for status in statuses:
        timestamp_utc = status.timestamp_utc

        # Convert timestamp from UTC to local time
        timestamp_local = timestamp_utc.astimezone(timezone).time()

        if prev_status is None:
            # Set the initial status
            prev_status = status.status
        else:
            # Compute the duration between the current and previous status
            duration = datetime.datetime.combine(
                datetime.date.today(), timestamp_local
            ) - datetime.datetime.combine(datetime.date.today(), prev_timestamp_local)

            if prev_status == "active":
                # Update uptime
                if (
                    timestamp_local >= start_time_local
                    and timestamp_local <= end_time_local
                ):
                    uptime += duration
                else:
                    # Adjust duration based on business hours
                    if timestamp_local < start_time_local:
                        duration -= datetime.datetime.combine(
                            datetime.date.today(), start_time_local
                        ) - datetime.datetime.combine(
                            datetime.date.today(), timestamp_local
                        )
                    elif timestamp_local > end_time_local:
                        duration -= datetime.datetime.combine(
                            datetime.date.today(), timestamp_local
                        ) - datetime.datetime.combine(
                            datetime.date.today(), end_time_local
                        )

                    downtime += duration
            else:
                # Update downtime
                downtime += duration

        prev_status = status.status
        prev_timestamp_local = timestamp_local

    # Compute the duration between the last observation and the current time
    duration = datetime.datetime.combine(
        datetime.date.today(), end_time_local
    ) - datetime.datetime.combine(datetime.date.today(), prev_timestamp_local)

    if prev_status == "active":
        # Update uptime
        if end_time_local >= start_time_local and end_time_local <= end_time_local:
            uptime += duration
        else:
            # Adjust duration based on business hours
            if end_time_local < start_time_local:
                duration -= datetime.datetime.combine(
                    datetime.date.today(), start_time_local
                ) - datetime.datetime.combine(datetime.date.today(), end_time_local)
            elif end_time_local > end_time_local:
                duration -= datetime.datetime.combine(
                    datetime.date.today(), end_time_local
                ) - datetime.datetime.combine(datetime.date.today(), end_time_local)

            downtime += duration
    else:
        # Update downtime
        downtime += duration

    return uptime, downtime


def save_report_data_to_csv(report_data, report_id):
    fieldnames = [
        "store_id",
        "uptime_last_hour",
        "uptime_last_day",
        "uptime_last_week",
        "downtime_last_hour",
        "downtime_last_day",
        "downtime_last_week",
    ]

    with open(f"report_{report_id}.csv", mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(report_data)


if __name__ == "__main__":
    app.run()
