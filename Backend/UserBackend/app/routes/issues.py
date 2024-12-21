from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db
from app.models.issue import Issue

issues = Blueprint("issues", __name__)


@issues.route("/report", methods=["POST"])
@jwt_required()
def report_issue():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()

        new_issue = Issue(
            user_id=current_user_id,
            title=data["title"],
            description=data["description"],
            category=data["category"],
            address=data["address"],
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            photo_url=data.get("photo_url"),
            severity=data.get("severity", "medium"),
        )

        db.session.add(new_issue)
        db.session.commit()

        return (
            jsonify(
                {"message": "Issue reported successfully", "issue_id": new_issue.id}
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


@issues.route("/list", methods=["GET"])
@jwt_required()
def get_issues():
    try:
        issues = Issue.query.all()
        return (
            jsonify(
                {
                    "issues": [
                        {
                            "id": issue.id,
                            "title": issue.title,
                            "description": issue.description,
                            "status": issue.status,
                            "category": issue.category,
                            "address": issue.address,
                            "created_at": issue.created_at.isoformat(),
                            "photo_url": issue.photo_url,
                        }
                        for issue in issues
                    ]
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@issues.route("/<int:issue_id>", methods=["GET"])
@jwt_required()
def get_issue(issue_id):
    try:
        issue = Issue.query.get_or_404(issue_id)
        return (
            jsonify(
                {
                    "id": issue.id,
                    "title": issue.title,
                    "description": issue.description,
                    "status": issue.status,
                    "category": issue.category,
                    "address": issue.address,
                    "created_at": issue.created_at.isoformat(),
                    "photo_url": issue.photo_url,
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@issues.route("/<int:issue_id>/status", methods=["PUT"])
@jwt_required()
def update_status(issue_id):
    try:
        issue = Issue.query.get_or_404(issue_id)
        data = request.get_json()

        issue.status = data["status"]
        db.session.commit()

        return jsonify({"message": "Status updated successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
