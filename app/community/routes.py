"""This module contains the routes for the community blueprint."""

from flask import current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.api.service import (
    categories_service,
    communities_service,
    user_communities_service,
)
from app.community import community_bp, forms, service
from app.constants import DISPLAY_COMMUNITY_NUM, FlashAlertTypeEnum, HttpRequestEnum
from app.extensions import db
from app.models.community import Community
from app.notice.events import NoticeTypeEnum, notice_event
from app.utils import get_pagination_details


@community_bp.route("/", methods=["GET"])
@community_bp.route("/<int:community_id>", methods=["GET"])
@login_required
def community(community_id: int = None):
    """Render the community page."""

    if community_id:
        community_entity = db.session.query(Community).get(community_id)
        return render_template(
            "community.html",
            render_id="community-list",
            render_url="/communities/community_list",
            communities=[community_entity],
        )

    # communities
    communities_result = communities_service(per_page=DISPLAY_COMMUNITY_NUM).get_json()
    communities = communities_result.get("data").get("communities")

    # pagination
    community_pagination = communities_result.get("pagination")
    pagination = get_pagination_details(
        current_page=community_pagination["page"],
        total_pages=community_pagination["total_pages"],
        total_items=community_pagination["total_items"],
    )

    return render_template(
        "community.html",
        render_id="community-list",
        render_url="/communities/community_list",
        communities=communities,
        pagination=pagination,
    )


@community_bp.route("/community_list", methods=["GET"])
@login_required
def community_list():
    """Render the community list page."""

    # requests
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=DISPLAY_COMMUNITY_NUM, type=int)

    # communities
    communities_result = communities_service(page=page, per_page=per_page).get_json()
    communities = communities_result.get("data").get("communities")

    # pagination
    community_pagination = communities_result.get("pagination")
    pagination = get_pagination_details(
        current_page=community_pagination["page"],
        total_pages=community_pagination["total_pages"],
        total_items=community_pagination["total_items"],
    )

    return render_template(
        "communityList.html",
        communities=communities,
        pagination=pagination,
    )


@community_bp.route("/user", methods=["GET"])
@login_required
def user_community():
    """Get the user's community."""

    # requests
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=6, type=int)

    # user communities
    user_communities_response = user_communities_service(
        page=page, per_page=per_page
    ).get_json()
    user_communities = user_communities_response.get("data").get("user_communities")

    # pagination
    pagination = get_pagination_details(
        user_communities_response.get("pagination")["page"],
        user_communities_response.get("pagination")["total_pages"],
        user_communities_response.get("pagination")["total_items"],
    )

    return render_template(
        "community.html",
        render_id="community-list",
        render_url="/communities/community_list/user",
        communities=user_communities,
        pagination=pagination,
    )


@community_bp.route("/community_list/user", methods=["GET"])
@login_required
def user_community_list():
    """Render the community list page."""

    # requests
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=6, type=int)

    # user communities
    user_communities_response = user_communities_service(
        page=page, per_page=per_page
    ).get_json()
    user_communities = user_communities_response.get("data").get("user_communities")

    # pagination
    pagination = get_pagination_details(
        user_communities_response.get("pagination")["page"],
        user_communities_response.get("pagination")["total_pages"],
        user_communities_response.get("pagination")["total_items"],
    )

    return render_template(
        "communityList.html",
        communities=user_communities,
        pagination=pagination,
    )


@community_bp.route("/management", methods=["GET", "POST"])
@community_bp.route("/management/<int:community_id>", methods=["GET", "POST"])
@login_required
def community_management(community_id: int = None):
    """Render the community management page."""

    form = forms.CommunityForm()
    form.creator_id.data = current_user.id

    # community
    community_entity = None
    if community_id:
        community_entity = db.session.query(Community).get(community_id)

    # categories
    categories = categories_service().get_json().get("data").get("categories")
    form.category_select.choices = [
        (category.get("id"), category.get("name")) for category in categories
    ]

    if form.validate_on_submit():
        if not community_entity:
            create_response = service.create_community_service(form)
            if create_response.get("code") == HttpRequestEnum.CREATED.value:
                community_entity = create_response.get("data")
                # add community to the database
                db.session.add(community_entity)
                current_app.logger.info(
                    "Community %s create successfully.", {community_entity.name}
                )
                notice_event(notice_type=NoticeTypeEnum.COMMUNITY_CREATED)
                flash(
                    "Community create successfully.", FlashAlertTypeEnum.SUCCESS.value
                )
            else:
                message = create_response.get("message")
                current_app.logger.error("Community create failed: %s.", {message})
                flash(message, FlashAlertTypeEnum.DANGER.value)

            return redirect(url_for("community.community_management"))

        # only the creator can update the community
        if community_entity.creator_id != form.creator_id.data:
            current_app.logger.error(
                "Community %s update failed, the creator is not the same.",
                {community_entity.name},
            )
            flash(
                "Only the creator can update the community.",
                FlashAlertTypeEnum.DANGER.value,
            )

            return redirect(url_for("community.community_management"))

        update_response = service.update_community_service(community_entity, form)
        if update_response.get("code") == HttpRequestEnum.SUCCESS_OK.value:
            data = update_response.get("data")
            # data not changed
            if not data:
                return redirect(url_for("community.community_management"))

            # update community to the database
            db.session.commit()
            current_app.logger.info(
                "Community %s update successfully.", {community_entity.name}
            )
            notice_event(notice_type=NoticeTypeEnum.COMMUNITY_UPDATED)
            flash("Community update successfully.", FlashAlertTypeEnum.SUCCESS.value)
        else:
            message = update_response.get("message")
            current_app.logger.error("Community %s update failed: %s.", {message})
            flash(message, FlashAlertTypeEnum.DANGER.value)

            return redirect(url_for("community.community_management"))

        if form.errors:
            for field, errors in form.errors.items():
                for error in errors:
                    current_app.logger.error(
                        "Community %s management error in field %s: %s",
                        {community_entity.name if community_entity else "creation"},
                        {getattr(form, field).label.text},
                        {error},
                    )
                    flash(
                        f"{getattr(form, field).label.text}, {error}",
                        FlashAlertTypeEnum.DANGER.value,
                    )

    return render_template(
        "communityManagement.html",
        form=form,
        community=community_entity,
    )
