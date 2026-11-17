
from flask import Blueprint, request, jsonify

from repositories.academic_repository import AcademicRepository
from repositories.user_repository import UserRepository
from utils import get_data, check_period, check_task


academic_bp = Blueprint("academic", __name__)
academic = AcademicRepository()
repo = UserRepository()


#Semesters

@academic_bp.route("/users/<int:user_id>/semesters",
                   methods=["GET", "POST"])
def semesters(user_id):

    if request.method == "GET":
        return jsonify(academic.get_semesters(user_id))

    data = get_data([
        "semester_name", "start_date", "end_date"
    ])

    check_period(data["start_date"], data["end_date"])

    semester = academic.create_semester(user_id, data)

    if semester is None:
        return jsonify({"error": "User not found"}), 404

    return jsonify(semester), 201


@academic_bp.route(
    "/users/<int:user_id>/semesters/<int:semester_id>",
    methods=["GET", "PUT", "DELETE"]
)
def semester_details(user_id, semester_id):

    if request.method == "GET":
        result = academic.get_semester(user_id, semester_id)

    elif request.method == "DELETE":
        result = academic.delete_semester(user_id, semester_id)

    else:
        data = get_data([
            "semester_name", "start_date", "end_date"
        ])

        check_period(data["start_date"], data["end_date"])

        result = academic.update_semester(
            user_id, semester_id, data
        )

    if result is None:
        return jsonify({"error": "Semester not found"}), 404

    return jsonify(result)


#Courses

@academic_bp.route("/users/<int:user_id>/courses",
                   methods=["GET", "POST"])
def courses(user_id):

    if request.method == "GET":
        return jsonify(academic.get_courses(user_id))

    data = get_data([
        "semester_id", "course_code", "course_name"
    ])

    if type(data["semester_id"]) is not int:
        raise ValueError("Invalid semester ID")

    course = academic.create_course(user_id, data)

    if course is None:
        return jsonify({"error": "Semester not found"}), 404

    return jsonify(course), 201


@academic_bp.route(
    "/users/<int:user_id>/courses/<int:course_id>",
    methods=["GET", "PUT", "DELETE"]
)
def course_details(user_id, course_id):

    if request.method == "GET":
        result = academic.get_course(user_id, course_id)

    elif request.method == "DELETE":
        result = academic.delete_course(user_id, course_id)

    else:
        data = get_data([
            "semester_id", "course_code", "course_name"
        ])

        if type(data["semester_id"]) is not int:
            raise ValueError("Invalid semester ID")

        if academic.get_semester(
            user_id, data["semester_id"]
        ) is None:
            return jsonify({"error": "Semester not found"}), 404

        result = academic.update_course(
            user_id, course_id, data
        )

    if result is None:
        return jsonify({"error": "Course not found"}), 404

    return jsonify(result)


#Tasks

@academic_bp.route("/users/<int:user_id>/tasks",
                   methods=["GET", "POST"])
def tasks(user_id):

    if request.method == "GET":
        return jsonify(academic.get_tasks(user_id))

    data = get_data(["title", "due_date"])
    check_task(data)

    course_id = data.get("course_id")

    if course_id is not None:
        if type(course_id) is not int:
            raise ValueError("Invalid course ID")

        if academic.get_course(user_id, course_id) is None:
            return jsonify({"error": "Course not found"}), 404

    if repo.find_by_id(user_id) is None:
        return jsonify({"error": "User not found"}), 404

    task = academic.create_task(user_id, data)

    return jsonify(task), 201


@academic_bp.route(
    "/users/<int:user_id>/tasks/<int:task_id>",
    methods=["GET", "PUT", "DELETE"]
)
def task_details(user_id, task_id):

    if request.method == "GET":
        result = academic.get_task(user_id, task_id)

    elif request.method == "DELETE":
        result = academic.delete_task(user_id, task_id)

    else:
        data = get_data(["title", "due_date"])
        check_task(data)

        course_id = data.get("course_id")

        if course_id is not None:
            if type(course_id) is not int:
                raise ValueError("Invalid course ID")

            if academic.get_course(user_id, course_id) is None:
                return jsonify({"error": "Course not found"}), 404

        result = academic.update_task(user_id, task_id, data)

    if result is None:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(result)
