
from flask import Blueprint, request, jsonify

from repositories.work_repository import WorkRepository
from utils import get_data, check_job, check_shift, calculate_earnings


work_bp = Blueprint("work", __name__)
work = WorkRepository()


#Jobs

@work_bp.route("/users/<int:user_id>/jobs",
               methods=["GET", "POST"])
def jobs(user_id):

    if request.method == "GET":
        return jsonify(work.get_jobs(user_id))

    data = get_data(["employer", "hourly_wage"])
    check_job(data)

    job = work.create_job(user_id, data)

    if job is None:
        return jsonify({"error": "User not found"}), 404

    return jsonify(job), 201


@work_bp.route(
    "/users/<int:user_id>/jobs/<int:job_id>",
    methods=["GET", "PUT", "DELETE"]
)
def job_details(user_id, job_id):

    if request.method == "GET":
        result = work.get_job(user_id, job_id)

    elif request.method == "DELETE":
        result = work.delete_job(user_id, job_id)

    else:
        data = get_data(["employer", "hourly_wage"])
        check_job(data)

        result = work.update_job(user_id, job_id, data)

    if result is None:
        return jsonify({"error": "Job not found"}), 404

    return jsonify(result)

#Shifts:

@work_bp.route("/users/<int:user_id>/shifts",
               methods=["GET", "POST"])
def shifts(user_id):

    if request.method == "GET":
        records = work.get_shifts(user_id)

        return jsonify([
            calculate_earnings(shift) for shift in records
        ])

    data = get_data([
        "job_id", "start_time", "end_time"
    ])

    check_shift(data)

    if type(data["job_id"]) is not int:
        raise ValueError("Invalid job ID")

    saved = work.create_shift(user_id, data)

    if saved is None:
        return jsonify({"error": "Job not found"}), 404

    shift = work.get_shift(user_id, saved["shift_id"])

    return jsonify(calculate_earnings(shift)), 201


@work_bp.route(
    "/users/<int:user_id>/shifts/<int:shift_id>",
    methods=["GET", "PUT", "DELETE"]
)
def shift_details(user_id, shift_id):

    if request.method == "DELETE":
        result = work.delete_shift(user_id, shift_id)

        if result is None:
            return jsonify({"error": "Shift not found"}), 404

        return jsonify({"message": "Shift deleted"})

    if request.method == "PUT":
        data = get_data([
            "job_id", "start_time", "end_time"
        ])

        check_shift(data)

        if type(data["job_id"]) is not int:
            raise ValueError("Invalid job ID")

        if work.get_job(user_id, data["job_id"]) is None:
            return jsonify({"error": "Job not found"}), 404

        saved = work.update_shift(
            user_id, shift_id, data
        )

        if saved is None:
            return jsonify({"error": "Shift not found"}), 404

    shift = work.get_shift(user_id, shift_id)

    if shift is None:
        return jsonify({"error": "Shift not found"}), 404

    return jsonify(calculate_earnings(shift))
