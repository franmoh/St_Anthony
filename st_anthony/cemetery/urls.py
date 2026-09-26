from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("detail/", views.detail, name="detail"),
    path("plot/", views.plot, name="plot"),
    path("plot/<int:pk>/", views.plot_info, name="plot_info"),
    path("manage/plots/", views.manage_plots, name="manage_plots"),
    path("manage/plots/<int:pk>/", views.manage_plot_detail, name="manage_plot_detail"),
    path("manage/plots/<int:pk>/reserve/", views.reserve_plot, name="reserve_plot"),
    path(
        "manage/plots/<int:pk>/cancel-reservation/",
        views.cancel_reservation,
        name="cancel_reservation",
    ),
    path(
        "manage/plots/<int:pk>/reservation/<int:history_pk>/",
        views.reservation_certificate,
        name="reservation_certificate",
    ),
    path(
        "manage/plots/<int:pk>/mark-engraving-complete/",
        views.mark_engraving_complete,
        name="mark_engraving_complete",
    ),
    path(
        "manage/plot-contact/<int:mapping_pk>/",
        views.plot_contact_card,
        name="plot_contact_card",
    ),
    path(
        "manage/plot-contact/<int:mapping_pk>/edit/",
        views.edit_plot_contact,
        name="edit_plot_contact",
    ),
    path(
        "manage/plot-contact/<int:mapping_pk>/payment/edit/",
        views.edit_plot_contact_payment,
        name="edit_plot_contact_payment",
    ),
    path(
        "manage/plot-contact/<int:mapping_pk>/make-primary/",
        views.make_primary_contact,
        name="make_primary_contact",
    ),
    path(
        "manage/plot-contact/<int:mapping_pk>/delete/",
        views.delete_contact,
        name="delete_contact",
    ),
    path(
        "manage/plots/<int:pk>/contact/add/",
        views.add_contact,
        name="add_contact",
    ),
    path(
        "manage/plots/<int:pk>/contact/add/cancel/",
        views.cancel_add_contact,
        name="cancel_add_contact",
    ),
    path(
        "manage/plots/<int:pk>/deceased/add/",
        views.add_deceased,
        name="add_deceased",
    ),
    path(
        "manage/plots/<int:pk>/deceased/add/cancel/",
        views.cancel_add_deceased,
        name="cancel_add_deceased",
    ),
    path(
        "manage/deceased/<int:pk>/",
        views.deceased_card,
        name="deceased_card",
    ),
    path(
        "manage/deceased/<int:pk>/edit/",
        views.edit_deceased,
        name="edit_deceased",
    ),
    path(
        "manage/deceased/<int:pk>/delete/",
        views.delete_deceased,
        name="delete_deceased",
    ),
    path(
        "manage/plots/<int:pk>/note/",
        views.note_section,
        name="note_section",
    ),
    path(
        "manage/plots/<int:pk>/note/edit/",
        views.edit_note,
        name="edit_note",
    ),
    path(
        "manage/plots/<int:pk>/note/delete/",
        views.delete_note,
        name="delete_note",
    ),
    path(
        "detail/<int:pk>/note/",
        views.deceased_note_section,
        name="deceased_note_section",
    ),
    path(
        "detail/<int:pk>/note/edit/",
        views.edit_deceased_note,
        name="edit_deceased_note",
    ),
    path(
        "detail/<int:pk>/note/delete/",
        views.delete_deceased_note,
        name="delete_deceased_note",
    ),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("about-us/", views.about, name="about"),
    path("contact-us/", views.contact, name="contact"),
    path("contact-us/submit/", views.contact_submit, name="contact_submit"),
    path("newsletter/subscribe/", views.newsletter_subscribe, name="newsletter_subscribe"),
]
