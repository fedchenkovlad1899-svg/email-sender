from .users import (
    RegisterView,
    LoginView,
    ProfileView,
    LogoutView,
    ChangePasswordView,
    UserListView,
    UserDetailView,
    UserStatusView,
    UserDeleteView
)

from .contacts import (
    ContactListView,
    ContactCreateView,
    ContactRetrieveView,
    ContactUpdateView,
    ContactDeleteView
)
from .message_templates import (
    MessageTemplateListView,
    MessageTemplateCreateView,
    MessageTemplateRetrieveView,
    MessageTemplateUpdateView,
    MessageTemplateDeleteView
)
from .contact_groups import (
    ContactGroupListView,
    ContactGroupCreateView,
    ContactGroupRetrieveView,
    ContactGroupUpdateView,
    ContactGroupDeleteView
)
from .campaigns import (
    CampaignListView,
    CampaignCreateView,
    CampaignRetrieveView,
    CampaignUpdateView,
    CampaignDeleteView
)
from  .email_logs import (
    EmailLogListView,
    EmailLogRetrieveView
)