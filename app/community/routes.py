"""This module contains the routes for the community blueprint."""

import logging
import sys

from flask import Flask, redirect, render_template, request, url_for, jsonify
from flask_login import current_user, login_required

from app.community import community_bp, forms
from app.extensions import db
from app.models.category import Category
from app.models.community import Community

logging.basicConfig(level=logging.DEBUG)
# 创建日志处理程序，输出到标准输出流
handler = logging.StreamHandler(sys.stdout)


@community_bp.route("/")
# @login_required
def community():
    """Render the community page."""
    infolist = db.session.query(Community).all()
    return render_template("community.html", infolist=infolist)


@community_bp.route("/createCommunity")
# @login_required
def create():
    """Render the create page."""
    form = forms.CreateForm(request.form)
    optionList = db.session.query(Category).all()
    return render_template("createCommunity.html", optionList=optionList, form=form)


@community_bp.route("/add_community", methods=["POST"])
def add_community():
    form = forms.CreateForm(request.form)
    if form.validate_on_submit():
        print("1111------------------------------321")
        print(form.name.data)
        print(form.description.data)
        print(form.category_id.data)
        print("------------------------------")
        community = Community(
            name=form.name.data,
            description=form.description.data,
            category_id=form.category_id.data,
            creator_id=current_user.id,
        )
        db.session.add(community)
        db.session.commit()
        optionList = db.session.query(Category).all()
        return render_template("createCommunity.html", optionList=optionList, form=form)
        # return redirect(url_for('community.create'))
    else:
        print("error------------------------------error")
        print("Form validation failed:", form.errors)
        return render_template("createCommunity.html", optionList=optionList, form=form)
        # return redirect(url_for('community.create',form=form))


@community_bp.route("/delete_community/<int:record_id>", methods=["GET", "DELETE"])
def delete_community(record_id: int):
    print(current_user.id)
    print("||")
    print(record_id)
    record_entity = (
        db.session.query(Community)
        .filter_by(id=record_id, creator_id=current_user.id)
        .first()
    )
    if record_entity is None:
        return jsonify({"error": "Record not found"}), 404

    # if request.method == "GET":
    #     return ApiResponse(data={"record": record_entity.to_dict()}).json()

    if request.method == "DELETE":
        db.session.delete(record_entity)
        db.session.commit()
    return jsonify({"message": "Community deleted successfully"}), 200
