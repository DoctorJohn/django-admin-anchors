from django.test import TestCase
from admin_anchors.utils import create_admin_anchor
from tests.models import Person


class UtilsTestCase(TestCase):
    def test_resolve_changelist_page(self):
        link = create_admin_anchor(
            page_name="changelist",
            app_label="tests",
            model_name="member",
            label="Members",
        )
        expectation = "<a href='/admin/tests/member/'>Members</a>"
        self.assertEqual(link, expectation)

    def test_resolve_filtered_changelist_page(self):
        link = create_admin_anchor(
            page_name="changelist",
            app_label="tests",
            model_name="member",
            label="Members",
            query={"groups__id": 1},
        )
        expectation = "<a href='/admin/tests/member/?groups__id=1'>Members</a>"
        self.assertEqual(link, expectation)

    def test_resolve_change_page(self):
        person = Person()
        person.save()
        link = create_admin_anchor(
            page_name="change",
            app_label="tests",
            model_name="person",
            label="Person",
            args=[person.pk],
        )
        expectation = f"<a href='/admin/tests/person/{person.pk}/change/'>Person</a>"
        self.assertEqual(link, expectation)
