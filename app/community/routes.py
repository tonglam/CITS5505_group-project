"""This module contains the routes for the community blueprint."""

from flask import redirect, render_template, request, url_for, jsonify
from flask_login import current_user

from app.community import community_bp, forms
from app.extensions import db
from app.models.category import Category
from app.models.community import Community




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

@community_bp.route("/editCommunity/<int:record_id>")
# @login_required
def edit(record_id: int):
    """Render the create page."""
    form = forms.CreateForm(request.form)
    record_entity = (
        db.session.query(Community)
        .filter_by(id=record_id, creator_id=current_user.id)
        .first()
    )
    optionList = db.session.query(Category).all()
    return render_template("createCommunity.html", optionList=optionList,record_entity=record_entity, form=form)


@community_bp.route("/add_community", methods=["POST"])
def add_community():
    form = forms.CreateForm(request.form)
    if form.validate_on_submit():
        community = Community(
            name=form.name.data,
            description=form.description.data,
            category_id=form.category_id.data,
            creator_id=current_user.id,
        )
        db.session.add(community)
        db.session.commit()
        optionList = db.session.query(Category).all()
        return redirect(url_for('community.community' ))
        # return render_template("createCommunity.html", optionList=optionList, form=form)
        # return redirect(url_for('community.create'))
    else:
        return render_template("createCommunity.html", optionList=optionList, form=form)
        # return redirect(url_for('community.create',form=form))


@community_bp.route("/update_community/<int:record_id>", methods=["POST", "DELETE"])
def update_community(record_id: int):
    record_entity = (
        db.session.query(Community)
        .filter_by(id=record_id, creator_id=current_user.id)
        .first()
    )
    if record_entity is None:
        return jsonify({"error": "Record not found"}), 404
    if request.method == "DELETE":
        db.session.delete(record_entity)
        db.session.commit()
    if request.method == "POST":
        form = forms.CreateForm(request.form)
        if form.validate_on_submit():
            record_entity.name = form.name.data
            record_entity.description = form.description.data
            record_entity.category_id = form.category_id.data
            
            db.session.commit()  # Submit changes to the database
            # After successful update, redirect to edit page
            return redirect(url_for('community.community' ))
        else:
            return redirect(url_for('community.edit', record_id=record_id))
            # return render_template("createCommunity.html", optionList=optionList, form=form)
    return jsonify({"message": "Community deleted successfully"}), 200
