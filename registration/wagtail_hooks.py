from registration.models import Attendant
from wagtail.admin.ui.tables import UpdatedAtColumn
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

class AttendantViewSet(SnippetViewSet):
    model = Attendant
    icon = "user"
    list_display = ["user_unique_id", "first_name", "last_name", "email", "company", "position","country", "phone", UpdatedAtColumn()]
    list_export = ["user_unique_id", "first_name", "last_name", "email", "company", "position","country", "phone"]
    list_per_page = 50
    inspect_view_enabled = True
    admin_url_namespace = "attendant_views"
    base_url_path = "internal/attendant"
    # filterset_class = OrderFilterSet

register_snippet(AttendantViewSet)