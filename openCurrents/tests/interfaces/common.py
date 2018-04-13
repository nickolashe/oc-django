"""Selection of common classess and methods for the unit tests."""

from django.contrib.auth.models import User

from datetime import datetime, timedelta
from django.utils import timezone

from openCurrents.models import \
    AdminActionUserTime, \
    Entity, \
    Item, \
    Ledger, \
    Offer, \
    Org, \
    OrgEntity, \
    OrgUser, \
    Project, \
    Event, \
    Transaction, \
    TransactionAction, \
    UserEntity, \
    UserEventRegistration, \
    UserTimeLog

from openCurrents.interfaces.ocuser import \
    OcUser, \
    InvalidUserException, \
    UserExistsException

from openCurrents.interfaces.orgs import (
    OrgUserInfo,
    OcOrg
)

from openCurrents.interfaces.auth import (
    OcAuth
)

from openCurrents.interfaces.orgadmin import OrgAdmin

from openCurrents.interfaces.common import diffInHours

import pytz
import uuid
import random
import string
import re

from django.test import Client

# ====== CONTENT =======
# _create_org
# _create_test_user
# _create_project
# _create_event
# _setup_user_event_registration
# _setup_volunteer_hours
# _setup_transactions
# _setup_ledger_entry


class SetUpTests(object):
    """Helper class to setup tests."""

    def generic_setup(
            self,
            npf_orgs_list,
            biz_orgs_list,
            volunteers_list,
            create_admins=True,
            create_projects=True
    ):
        """
        Take lists of initial data and create needed objects.

        npf_orgs_list - list of NPF orgs titles (string)
        biz_orgs_list - list of BIZ orgs titles (string)
        volunteers_list - list of volunteers names (string)
        create_admins - boolean, to create an admin per NPF/BIZ org
        create_projects - boolean, to create a project per each NPF org
        """
        # creating NPF org with projects if required
        org_i = 0
        for npf_org in npf_orgs_list:

            org_i += 1
            org = _create_org(npf_org, "npf")

            # creating projects
            if create_projects:
                _create_project(org, 'test_project_{}'.format(str(org_i)))

            # creating an NPF admin
            if create_admins:
                _create_test_user(
                    'npf_admin_{}'.format(str(org_i)),
                    org=org,
                    is_org_admin=True
                )

        # creating BIZ org
        biz_org_i = 0
        for biz_org in biz_orgs_list:

            biz_org_i += 1
            org = _create_org(biz_org, "biz")

            # creating an NPF admin
            if create_admins:
                _create_test_user(
                    'biz_admin_{}'.format(str(biz_org_i)),
                    org=org,
                    is_org_admin=True
                )

        # creating existing volunteers
        for volunteer in volunteers_list:
            _create_test_user(volunteer)

    def get_all_volunteers(self):
        """Return list of volunteers."""
        volunteers = []
        for user in User.objects.all():
            if not OcAuth(user.id).is_admin():
                volunteers.append(user)

        return volunteers

    def get_all_npf_admins(self):
        """Return list of NPF admins (user instance)."""
        npf_admins = []
        for user in OrgUser.objects.all():
            u = OcAuth(user.id)
            if u.is_admin_org():
                npf_admins.append(user.user)

        return npf_admins

    def get_all_biz_admins(self):
        """Return list of BIZ admins."""
        biz_admins = []
        for user in OrgUser.objects.all():
            u = OcAuth(user.id)
            if u.is_admin_biz():
                biz_admins.append(user.user)

        return biz_admins

    def get_all_npf_orgs(self):
        """Return list of NPF orgs."""
        return [org for org in Org.objects.filter(status='npf')]

    def get_all_biz_orgs(self):
        """Return list of BIZ orgs."""
        return [org for org in Org.objects.filter(status='biz')]

    def get_all_projects(self, org):
        """Return list of projects."""
        return [proj for proj in Project.objects.filter(org=org)]


def _create_org(org_name, org_status):
    """
    Create users and maps them to the org if needed.

    Takes:
        org_name - string
        org_status - string ('npf', 'biz')
    """
    new_org = OcOrg().setup_org(name=org_name, status=org_status)

    return new_org


def _create_test_user(
    user_name,
    password='password',
    org=None,
    is_org_admin=False
):
    """
    Create users and maps them to the org if needed.

    Takes:
        user_name - string

        org - Org object. A NPF admin will be created, if Org is provided and is_org_admin = True.
        An org user will be created if org is provided and is_org_admin = False.
        If no org provided - a volunteer will be created.

        is_org_admin - if True, the user will be made an org admin, if org is provided.
    """
    test_user = OcUser().setup_user(
        username=user_name,
        email=user_name + '@email.cc',
        first_name=user_name + '_first_name',
        last_name=user_name + '_last_name'
    )

    if org:
        # mapping user to org
        oui = OrgUserInfo(test_user.id)
        oui.setup_orguser(org)

        # making a user an org admin
        if is_org_admin:
            oui.make_org_admin(org.id)

    test_user.set_password(password)
    test_user.save()
    return test_user


def _create_project(org, project_name):
    """
    Create project.

    org - Org object
    project_name - string
    """
    project = Project(
        org=org,
        name=project_name
    )
    project.save()
    return project


def _create_event(
    project,
    creator_id,
    datetime_start,
    datetime_end,
    description="Test Event",
    location="test_location",
    is_public=False,
    event_type="MN",
    coordinator=None
):
    """Create an event with given parameters."""
    event = Event(
        project=project,
        description=description,
        location=location,
        is_public=is_public,
        datetime_start=datetime_start,
        datetime_end=datetime_end,
        coordinator=coordinator,
        creator_id=creator_id
    )
    event.save()
    return event


def _setup_user_event_registration(
    user,
    event,
    is_confirmed=False
):
    """Create a user event registration with given parameters."""
    user_event_registration = UserEventRegistration(
        user=user,
        event=event,
        is_confirmed=is_confirmed
    )
    user_event_registration.save()
    return user_event_registration


def _setup_volunteer_hours(
    volunteer,
    npf_admin,
    org,
    project,
    datetime_start,
    datetime_end,
    description="Manually tracked time ",
    event_type="MN",
    is_verified=False,
    action_type='req'
):
    """
    Set up volunteers manually recprded hours.

    function takes:
        volunteer = User objects
        npf_admin = npf admin object
        org = Org object
        project = Project object
        description = provided string will be added to the end of default string
        event_type = string "MN" or "GR" (defautl "MN")
        datetime_start = datetime.datetime
        datetime_end = datetime.datetime
        is_verified = False/True (default False)
        action_type = 'app'/'dec'/'req' (default 'req')
    and creates respective records in testing DB.
    """
    event = Event.objects.create(
        project=project,
        is_public=True,
        description="finished event",
        location="test_location",
        coordinator=npf_admin,
        event_type=event_type,
        datetime_start=datetime_start,
        datetime_end=datetime_end
    )

    volunteer_timelog = UserTimeLog.objects.create(
        user=volunteer,
        event=event,
        datetime_start=datetime_start,
        datetime_end=datetime_end,
        is_verified=is_verified
    )

    actiontimelog = AdminActionUserTime.objects.create(
        user=npf_admin,
        usertimelog=volunteer_timelog,
        action_type=action_type
    )

    return volunteer_timelog, actiontimelog, event


def _setup_transactions(
    biz_org,
    biz_admin,
    transaction_currents_amount,
    transaction_price_reported,
    price_actual=None,
    pop_type='rec',
    offer_item_name="Test Item",
    currents_share=40,
    action_type='req'
):
    """
    Create pending or approved transactions.

    biz_org - biz org instance;
    biz_admin - biz admin user instance;
    transaction_currents_amount - int or float;
    transaction_price_reported - int or float;
    offer_item_name - string;
    currents_share - int or float;
    action_type - string. Possible values: 'req', 'app', 'red', 'dec'
    """
    offer_item = Item(name=offer_item_name)
    offer_item.save()

    offer = Offer(
        org=biz_org,
        item=offer_item,
        currents_share=currents_share
    )
    offer.save()

    if price_actual is None:
        price_actual = transaction_price_reported

    transaction = Transaction(
        user=biz_admin,
        offer=offer,
        price_reported=transaction_price_reported,
        currents_amount=transaction_currents_amount,
        price_actual=price_actual
    )
    transaction.save()

    action = TransactionAction(
        transaction=transaction,
        action_type=action_type
    )
    action.save()


def _setup_ledger_entry(
    entity_from,
    entity_to,
    currency='cur',
    amount=100.30,
    is_issued=False,
    action=None,
    transaction=None
):
    """
    USE IT UNTILL WE HAVE ledger.OcLedger.add_fiat implemented.

    entity_from -   Entity objects (eg User and Org)
    entity_to -     Entity objects (eg User and Org)
    currency -      string 'cur' or 'usd'
    amount -        Int of Float
    is_issued -     boolean
    action -        AdminActionUserTime instance
    transaction -   TransactionAction instance
    """
    ledger_rec = Ledger(
        entity_from=entity_from,
        entity_to=entity_to,
        currency=currency,
        amount=amount,
        is_issued=is_issued,
        action=action,
        transaction=transaction
    )

    ledger_rec.save()

    return


class SetupAdditionalTimeRecords():
    """SetUp class for TestApproveHoursRandomDates and TestApproveHoursCornerCases."""

    def _get_earliest_monday(self):
        """Get earliest monday for approve-hours page."""
        try:
            earliest_request_date = self.org_admin.get_hours_requested().\
                order_by('usertimelog__datetime_start').first().\
                usertimelog.datetime_start
        except:
            earliest_request_date = self.org_admin.get_hours_approved().\
                order_by('usertimelog__datetime_start').first().\
                usertimelog.datetime_start

        earliest_monday = earliest_request_date - timedelta(
            days=(earliest_request_date.weekday()))
        earliest_monday = earliest_monday.replace(hour=00, minute=00, second=00)

        return earliest_monday

    def _current_week_records(self, earliest_monday):
        current_week_sunday = earliest_monday + timedelta(days=6)
        current_week_sunday = current_week_sunday.replace(
            hour=23, minute=59, second=59
        )
        admin_actions_requested = self.org_admin.get_hours_requested().\
            order_by('usertimelog__datetime_start')

        current_week_records = []
        for rec in admin_actions_requested:
            if earliest_monday <= rec.usertimelog.datetime_start <= current_week_sunday:
                current_week_records.append(rec)

        return current_week_records

    def _compare_shown_records(self, current_week_records, response):
        records_num = len(current_week_records)

        # asserting num of displayed records and num of real records in DB
        num_of_recs_in_context_week = 0
        for i in response.context[0]['week'][0].items()[0][1].items()[0][1].items()[2:]:
            num_of_recs_in_context_week += len(i[1]) - 1

        self.assertEqual(
            records_num,
            num_of_recs_in_context_week
        )
        return records_num

    def setUp(self):
        """Set testing environment."""
        biz_orgs_list = ['BIZ_org_1']
        npf_orgs_list = ['NPF_org_1', 'NPF_org_2']
        volunteers_list = ['volunteer_1']

        test_setup = SetUpTests()
        test_setup.generic_setup(npf_orgs_list, biz_orgs_list, volunteers_list)

        # setting orgs
        self.org_npf = test_setup.get_all_npf_orgs()[0]
        self.org_npf2 = test_setup.get_all_npf_orgs()[1]
        # self.org_biz = test_setup.get_all_biz_orgs()[0]

        # set up project
        self.project = test_setup.get_all_projects(self.org_npf)[0]
        self.project2 = test_setup.get_all_projects(self.org_npf2)[0]

        # creating an npf admin
        all_admins = test_setup.get_all_npf_admins()
        self.npf_admin = all_admins[0]
        self.npf_admin2 = all_admins[1]
        self.org_admin = OrgAdmin(self.npf_admin.id)

        # assigning existing volunteers to variables
        all_volunteers = test_setup.get_all_volunteers()

        self.volunteer_1 = all_volunteers[0]

        # oc instances
        self.oc_npf_adm = OcUser(self.npf_admin.id)
        # self.org_biz_adm = BizAdmin(self.biz_admin.id)
        self.oc_vol_1 = OcUser(self.volunteer_1.id)

        # user entities
        self.vol_1_entity = UserEntity.objects.get(user=self.volunteer_1)
        self.user_enitity_id_vol_1 = UserEntity.objects.get(
            user=self.volunteer_1).id

        # setting up client
        self.client = Client()
        self.client.login(username=self.npf_admin.username, password='password')
