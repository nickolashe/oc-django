from django.conf.urls import url, include
from openCurrents import views

urlpatterns = [
    # template views
    url(r'^$', views.HomeView.as_view(), name='root'),
    url(r'^home/$', views.HomeView.as_view(), name='home'),
    url(r'^home/(?P<referrer>[\w\.@\+\-]*)/(?P<f_name>.*)/$', views.HomeView.as_view(), name='home'),
    url(r'^home/(?P<referrer>[\w\.@\+\-]*)$', views.HomeView.as_view(), name='home'),
    url(r'^home/(?P<referrer>[\w\.@\+\-]*)/(?P<status_msg>.*)/$',
        views.HomeView.as_view(), name='home'),
    url(r'^invite/(?P<referrer>[\w\.@\+\-]*)$', views.HomeView.as_view(), name='invite'),
    url(r'^check-email/(?P<user_email>[\w\.@\+\-]+)/$', views.CheckEmailView.as_view(), name='check-email'),
    url(r'^check-email/(?P<user_email>[\w\.@\+\-]+)/(?P<orgid>\d+)/$', views.CheckEmailView.as_view(), name='check-email'),
    url(r'^check-email/(?P<user_email>[\w\.@\+\-]+)/(?P<status>.*)/$', views.CheckEmailView.as_view(), name='check-email'),
    url(r'^communities/$', views.CommunitiesView.as_view(), name='communities'),
    url(r'^reset-password/(?P<user_email>[\w\.@\+\-]+)/$', views.ResetPasswordView.as_view(), name='reset-password'),
    url(r'^reset-password/(?P<user_email>[\w\.@\+\-]+)/(?P<token>\w{8}-\w{4}-\w{4}-\w{4}-\w{12})/$', views.ResetPasswordView.as_view(), name='reset-password'),
    url(r'^reset-password/(?P<user_email>[\w\.@\+\-]+)/(?P<token>\w{8}-\w{4}-\w{4}-\w{4}-\w{12})/(?P<status_msg>.*)/$', views.ResetPasswordView.as_view(), name='reset-password'),
    url(r'^business$', views.BusinessView.as_view(), name='business'),
    url(r'^check-email-password/$', views.CheckEmailPasswordView.as_view(), name='check-email-password'),
    url(r'^check-email-password/(?P<user_email>[\w\.@\+\-]+)/$', views.CheckEmailPasswordView.as_view(), name='check-email-password'),
    url(r'^check-email-password/(?P<user_email>[\w\.@\+\-]+)/(?P<status>.*)/$', views.CheckEmailPasswordView.as_view(), name='check-email-password'),
    url(r'^confirm-account/(?P<email>[\w\.@\+\-]+)/$',
        views.ConfirmAccountView.as_view(), name='confirm-account'),
    url(r'^confirm-account/(?P<email>[\w\.@\+\-]+)/(?P<token>\w{8}-\w{4}-\w{4}-\w{4}-\w{12})/$',
        views.ConfirmAccountView.as_view(), name='confirm-account'),
    url(r'^confirm-account/(?P<email>[\w\.@\+\-]+)/(?P<token>\w{8}-\w{4}-\w{4}-\w{4}-\w{12})/(?P<status_msg>.*)/$',
        views.ConfirmAccountView.as_view(), name='confirm-account'),
    url(r'^confirm-account/(?P<email>[\w\.@\+\-]+)/(?P<status_msg>.*)/$',
        views.ConfirmAccountView.as_view(), name='confirm-account'),
    url(r'^community$', views.CommunityView.as_view(), name='community'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^login/(?P<status_msg>.*)$', views.LoginView.as_view(), name='login'),
    url(r'^invite-friends/(?P<referrer>[\w\.@\+\-]*)$',
        views.InviteFriendsView.as_view(), name='invite-friends'),
    url(r'^approve-hours$', views.ApproveHoursView.as_view(), name='approve-hours'),
    url(r'^approve-hours/(?P<vols_approved>\d+)/(?P<vols_declined>\d+)/$', views.ApproveHoursView.as_view(), name='approve-hours'),
    url(r'^causes$', views.CausesView.as_view(), name='causes'),
    url(r'^edit-hours$', views.EditHoursView.as_view(), name='edit-hours'),
    url(r'^export-data$', views.ExportDataView.as_view(), name='export-data'),
    url(r'^faq$', views.FaqView.as_view(), name='faq'),
    url(r'^find-orgs$', views.FindOrgsView.as_view(), name='find-orgs'),
    url(r'^hours-approved$', views.HoursApprovedView.as_view(), name='hours-approved'),
    url(r'^inventory$', views.InventoryView.as_view(), name='inventory'),
    url(r'^mission$', views.MissionView.as_view(), name='mission'),
    url(r'^my-hours$', views.MyHoursView.as_view(), name='my-hours'),
    url(r'^nominate$', views.NominateView.as_view(), name='nominate'),
    url(r'^nomination-confirmed$', views.NominationConfirmedView.as_view(), name='nomination-confirmed'),
    url(r'^nomination-email$', views.NominationEmailView.as_view(), name='nomination-email'),
    url(r'^nonprofit$', views.NonprofitView.as_view(), name='nonprofit'),
    url(r'^offer', views.OfferView.as_view(), name='offer'),
    url(r'^org-signup/$', views.OrgSignupView.as_view(), name='org-signup'),
    url(r'^org-signup/(?P<status_msg>.*)/$', views.OrgSignupView.as_view(), name='org-signup'),
    url(r'^org-signup/(?P<org_name>.*)/$', views.OrgSignupView.as_view(), name='org-signup'),
    url(r'^org-signup/(?P<org_name>.*)/(?P<status_msg>.*)/$',
        views.OrgSignupView.as_view(), name='org-signup'),
    url(r'^our-story', views.OurStoryView.as_view(), name='our-story'),
    url(r'^public-record', views.PublicRecordView.as_view(), name='public-record'),
    url(r'^redeem-currents$', views.RedeemCurrentsView.as_view(), name='redeem-currents'),
    url(r'^request-currents$', views.RequestCurrentsView.as_view(), name='request-currents'),
    url(r'^sell$', views.SellView.as_view(), name='sell'),
    url(r'^send-currents$', views.SendCurrentsView.as_view(), name='send-currents'),
    url(r'^signup/$', views.SignupView.as_view(), name='signup'),
    url(r'^signup/(?P<status_msg>.*)/$', views.SignupView.as_view(), name='signup'),
    url(r'^org-approval$', views.OrgApprovalView.as_view(), name='org-approval'),
    url(r'^user-home/$', views.UserHomeView.as_view(), name='user-home'),
    url(r'^user-home/(?P<status_msg>.*)/$', views.UserHomeView.as_view(), name='user-home'),
    url(r'^verify-identity$', views.VerifyIdentityView.as_view(), name='verify-identity'),
    url(r'^time-tracker/$', views.TimeTrackerView.as_view(), name='time-tracker'),
    url(r'^time-tracker/(?P<status_msg>.*)/$', views.TimeTrackerView.as_view(), name='time-tracker'),
    url(r'^time-tracked$', views.TimeTrackedView.as_view(), name='time-tracked'),
    url(r'^volunteer$', views.VolunteerView.as_view(), name='volunteer'),
    url(r'^volunteer-requests$', views.VolunteerRequestsView.as_view(), name='volunteer-requests'),
    url(r'^profile$', views.ProfileView.as_view(), name='profile'),
    url(r'^profile/(?P<app_hr>(1|0))/$', views.ProfileView.as_view(), name='profile'),
    url(r'^profile/(?P<status_msg>.*)/$', views.ProfileView.as_view(), name='profile'),
    url(r'^admin-profile$', views.AdminProfileView.as_view(), name='admin-profile'),
    url(r'^admin-profile/(?P<vols_approved>\d+)/(?P<vols_declined>\d+)/$', views.AdminProfileView.as_view(), name='admin-profile'),
    url(r'^admin-profile/(?P<num_vols>\d+)/$', views.AdminProfileView.as_view(), name='admin-profile'),
    url(r'^edit-profile$', views.EditProfileView.as_view(), name='edit-profile'),
    url(r'^blog$', views.BlogView.as_view(), name='blog'),
    url(r'^marketplace$', views.MarketplaceView.as_view(), name='marketplace'),
    url(r'^edit-event/(?P<event_id>\d+)/$', views.EditEventView.as_view(), name='edit-event'),
    url(r'^create-event/(?P<org_id>\d+)/$', views.CreateEventView.as_view(), name='create-event'),
    url(r'^project-details$', views.ProjectDetailsView.as_view(), name='project-details'),
    url(r'^invite-volunteers$', views.InviteVolunteersView.as_view(), name='invite-volunteers'),
    url(r'^invite-volunteers/(?P<event_ids>.+)/$', views.InviteVolunteersView.as_view(), name='invite-volunteers'),
    url(r'^volunteers-invited/(?P<vol_no>\d+)/$', views.VolunteersInvitedView.as_view(), name='volunteers-invited'),
    url(r'^event-created/(?P<project>\w+)/(?P<num_events>\d+)/$', views.EventCreatedView.as_view(), name='event-created'),
    url(r'^live-dashboard/(?P<event_id>\d+)/$',
        views.LiveDashboardView.as_view(), name='live-dashboard'),
    url(r'^upcoming-events$', views.UpcomingEventsView.as_view(), name='upcoming-events'),
    url(r'^event-detail/(?P<pk>\d+)/$', views.EventDetailView.as_view(), name='event-detail'),
    url(r'^registration-confirmed/(?P<pk>\d+)/$',
        views.RegistrationConfirmedView.as_view(), name='registration-confirmed'),


    #temp 403, 404 and 500 views
    url(r'^403$', views.ForbiddenView.as_view(), name='403'),
    url(r'^404$', views.NotFoundView.as_view(), name='404'),
    url(r'^500$', views.ErrorView.as_view(), name='500'),


    # functional views
    url(r'^event_checkin/(?P<pk>\d+)/$', views.event_checkin, name='event_checkin'),
    url(r'^event_register/(?P<pk>\d+)/$', views.event_register, name='event_register'),
    url(r'^event_register_live/(?P<eventid>\d+)/$',
        views.event_register_live, name='event_register_live'),
    url(r'^org_user_list/(?P<org_id>\d+)/$', views.org_user_list, name='org_user_list'),
    url(r'^process_login/$', views.process_login, name='process_login'),
    url(r'^process_OrgNomination/$', views.process_OrgNomination, name='process_OrgNomination'),
    url(r'^process_logout/$', views.process_logout, name='process_logout'),
    url(r'^process_resend_verification/(?P<user_email>[\w\.@\+\-]+)/$', views.process_resend_verification, name='process_resend_verification'),
    url(r'^process_resend_password/(?P<user_email>[\w\.@\+\-]+)/$', views.process_resend_password, name='process_resend_password'),
    url(r'^password_reset_request/$', views.password_reset_request, name='password_reset_request'),
    url(r'^process_reset_password/(?P<user_email>[\w\.@\+\-]+)/$', views.process_reset_password, name='process_reset_password'),
    url(r'^process_signup/(?P<referrer>[\w\.@\+\-]*)$',
        views.process_signup, name='process_signup'),
    url(r'^process_signup/(?P<endpoint>(True|False))/$',
        views.process_signup, name='process_signup'),
    url(r'^process_signup/(?P<endpoint>(True|False))/(?P<verify_email>(True|False))/$',
        views.process_signup, name='process_signup'),
    url(r'^process_email_confirmation/(?P<user_email>[\w\.@\+\-]+)/$',
        views.process_email_confirmation, name='process_email_confirmation'),
    url(r'^process_org_signup/$', views.process_org_signup, name='process_org_signup'),
]

#handler404 = 'openCurrents.views.return_404'
#handler500 = 'openCurrents.views.return_500'
