# openCurrents platform architecture - a bird's eye overview

## Goal
We are building an alternative currency platform where users can earn *currents* for volunteering their time with non-profits. Once a non-profit approves volunteer hours, they become issued currents and can then be spent with businesses which post offers on the platform.

## Data models
### Orgs
Both non-profits and businesses are modeled using [Org](https://github.com/opencurrents/opencurrents/blob/develop/openCurrents/models.py#L17) model. The *status* field differentiates between the two types of organizations.

### Users
To represent users we are using Django's internal auth *User* model.
Users can be affiliated with Orgs through [OrgUser](https://github.com/opencurrents/opencurrents/blob/develop/openCurrents/models.py#L50) mapping.
Some users can have admin permissions for an org. These are modeled using Django's internal auth *Group* model. The convention is to name the group *admin_$id*, where id is the id of the organization. Any member of the group is granted admin privileges on the respective org.
In some cases unverified users are created with email only so we can start tracking their hours even before they verify their account.

### Event
Events are created by non-profit admins. All volunteer tracked hours are associated with events. Events can be either *group* or *manual*. Several volunteers can check in to group events, which are usually held at set times and locations (*live-dashboard*). Manual events are created each time volunteer submits individual requests for approval of their hours (*time-tracker*).

### UserTimeLog
This model registers all hours submitted by / for volunteers. *is_verified* flag determines whether the requests have been approved or not.

#### AdminActionUserTime
The purpose of this auxiliary model is to track actions non-profit admins take on hour requests from [UserTimeLog](#usertimelog) model. Initial volunteer request generates an action of type *request* in this table. Subsequently, the admin can either *approve* or *decline* the request.

### Offer

### Transaction

#### TransactionAction
### Ledger




## Business logic interfaces
Much of openCurrents business logic has been separated into [interfaces](https://github.com/opencurrents/opencurrents/tree/develop/openCurrents/interfaces).

### List of interfaces

* [OcUser](https://github.com/opencurrents/opencurrents/blob/develop/openCurrents/interfaces/ocuser.py)
  * To set up a user and all the related fixtures, call:
https://github.com/opencurrents/opencurrents/blob/develop/openCurrents/interfaces/ocuser.py#L38
More on creating fixture in [Creating test fixtures](#creating-test-fixtures)
  * User's available balance in currents is composed of earned currents minus pending offer redemptions. To get user's available balance in currents call:
https://github.com/opencurrents/opencurrents/blob/develop/openCurrents/interfaces/ocuser.py#L103

  * User's pending balance in currents is equal to sum of volunteer hours request. To get user's pending balance in currents:
https://github.com/opencurrents/opencurrents/blob/develop/openCurrents/interfaces/ocuser.py#L142

  * User's available USD balance is equal to the sum of offer redemptions in *redeemed* status. To get user's available balance in USD:
https://github.com/opencurrents/opencurrents/blob/develop/openCurrents/interfaces/ocuser.py#L174

  * User's available USD balance is equal to the sum of offer redemptions in *requested* or *approved* status. To get user's pending balance in USD:
https://github.com/opencurrents/opencurrents/blob/develop/openCurrents/interfaces/ocuser.py#L187

* [OcOrg](https://github.com/opencurrents/opencurrents/blob/develop/openCurrents/interfaces/orgs.py#L76)
  * To set up an org and all the related fixtures, call:
https://github.com/opencurrents/opencurrents/blob/develop/openCurrents/interfaces/orgs.py#L86

* [OrgUser](https://github.com/opencurrents/opencurrents/blob/develop/openCurrents/interfaces/orgs.py#L18)
  * To set up an *OrgUser* mapping, call:
https://github.com/opencurrents/opencurrents/blob/develop/openCurrents/interfaces/orgs.py#L24
  * The following method checks whether a user has admin privilege for a given org:
https://github.com/opencurrents/opencurrents/blob/develop/openCurrents/interfaces/orgs.py#L54

* Organizations (non-profits) are the entities issuing currents. The act of approving hours volunteered for a given org by that org's admin issues currents to the volunteer. [OrgAdmin](https://github.com/opencurrents/opencurrents/blob/develop/openCurrents/interfaces/orgadmin.py) interface offers the following methods to the org admin:
  * [get_hours_requested](https://github.com/opencurrents/opencurrents/blob/develop/openCurrents/interfaces/orgadmin.py#L31) is a method to obtain hours volunteered for the given org that are pending approval
  * [get_hours_approved](https://github.com/opencurrents/opencurrents/blob/develop/openCurrents/interfaces/orgadmin.py#L37) is a method to obtain approved volunteer hours for the given org

* Businesses receive currents from users in exchange for their products or services. [BizAdmin](https://github.com/opencurrents/opencurrents/blob/develop/openCurrents/interfaces/bizadmin.py) interface offers the following methods to the biz admin:
  * [get_balance_available](https://github.com/opencurrents/opencurrents/blob/develop/openCurrents/interfaces/bizadmin.py#L33) is a method to obtain business' available balance in currents. Available balance results from offer redemptions that have been approved.
  * [get_balance_pending](https://github.com/opencurrents/opencurrents/blob/develop/openCurrents/interfaces/bizadmin.py#L45) is a method to obtain business' pending balance in currents. Pending balance results from redemptions that have not been approved yet.
  * [get_offers_all](https://github.com/opencurrents/opencurrents/blob/develop/openCurrents/interfaces/bizadmin.py#L57) is a method to obtain all of the business' marketplace offers.

* Ledger
## Creating test fixtures
A python [script](https://github.com/opencurrents/opencurrents/blob/develop/openCurrents/scripts/setup_fixtures.py) is available to assist you in creating all the necessary test fixtures. It creates 2 non-profits (GreatDeeds and GoodVibes) and 2 businesses (ConsciousBiz and GreenBiz). GreatDeeds and ConsciousBiz have 2 admin users each, while GoodVibes and GreenBiz have a single admin each. There are also 2 volunteer users. All users are assigned the password 'oc'.

The script will also create several events for each of the non-profits, active offers for each of the businesses as well as volunteer hour and offer redemption requests in various states of approval for all of the 8 users. All of these fixtures are generated in a random way with the idea of capturing as many test cases as possible.
