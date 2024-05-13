"""This module contains the routes for the community blueprint."""

from flask import jsonify, render_template, request
from flask_login import current_user, login_required

from app.api.service import communities_service
from app.community import community_bp, forms
from app.extensions import db
from app.models.category import Category
from app.models.community import Community


@community_bp.route("/")
@login_required
def community():
    """Render the community page."""
    communities = communities_service().get_json().get("data").get("communities")
    return render_template("community.html", communities=communities)


@community_bp.route("/edit/<int:community_id>")
@login_required
def edit(community_id: int):
    """Render the create page."""
    form = forms.CreateForm(request.form)
    record_entity = (
        db.session.query(Community)
        .filter_by(id=community_id, creator_id=current_user.id)
        .first()
    )
    option_list = db.session.query(Category).all()
    return render_template(
        "createCommunity.html",
        optionList=option_list,
        record_entity=record_entity,
        form=form,
    )


@community_bp.route("/add_community", methods=["POST", "GET"])
@login_required
def add_community():
    """Render the create page. or do add with community"""
    if request.method == "GET":
        form = forms.CreateForm(request.form)
        option_list = db.session.query(Category).all()
        return render_template(
            "createCommunity.html", optionList=option_list, form=form
        )
    if request.method == "POST":
        form = forms.CreateForm(request.form)
        if form.validate_on_submit():
            new_community = Community(
                name=form.name.data,
                description=form.description.data,
                category_id=form.category_id.data,
                creator_id=current_user.id,
            )
            db.session.add(new_community)
            db.session.commit()
            return (
                jsonify({"message": "Create success", "ok": "ok", "id": community.id}),
                200,
            )
        # If you get here, it means the verification has not passed.
        message = ""
        for field, errors in form.errors.items():
            for error in errors:
                message += f"{field.capitalize()}: {error}"
        return jsonify({"message": message, "ok": "notok"}), 200
    return jsonify({"message": "method not support", "ok": "notok"}), 200


@community_bp.route("/update_community/<int:community_id>", methods=["POST", "DELETE"])
@login_required
def update_community(community_id: int):
    """Update the details of a community given its ID."""
    record_entity = (
        db.session.query(Community)
        .filter_by(id=community_id, creator_id=current_user.id)
        .first()
    )
    if record_entity is None:
        return jsonify({"message": "Record not found", "ok": "notok"}), 200
    if request.method == "DELETE":
        db.session.delete(record_entity)
        db.session.commit()
        return jsonify({"message": "Community deleted successfully", "ok": "ok"}), 200
    if request.method == "POST":
        form = forms.CreateForm(request.form)
        if form.validate_on_submit():
            record_entity.name = form.name.data
            record_entity.description = form.description.data
            record_entity.category_id = form.category_id.data
            db.session.commit()  # Submit changes to the database
            # After successful update, redirect to edit page
            return (
                jsonify({"message": "Edit success", "ok": "ok", "id": community_id}),
                200,
            )
        # If you get here, it means the verification has not passed.
        message = ""
        for field, errors in form.errors.items():
            for error in errors:
                message += f"{field.capitalize()}: {error}"
        return jsonify({"message": message, "ok": "notok", "id": community_id}), 200
    return jsonify({"message": "method not support", "ok": "notok"}), 200
