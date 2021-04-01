from django.db import models
from django.test import TestCase
from django.core.exceptions import ImproperlyConfigured
from admin_anchors.decorators import admin_anchor
from tests.models import Person, Profile, Article, Comment, Group, Member


class DecoratorsTestCase(TestCase):
    def test_non_relation_field_cannot_be_referenced(self):
        person = Person.objects.create()

        @admin_anchor(field_name="id")
        def id_anchor(self, instance):
            return "Profile"

        self.assertRaises(ImproperlyConfigured, id_anchor, None, person)

    def test_empty_anchor_generation(self):
        person = Person.objects.create()

        @admin_anchor(field_name="profile")
        def profile_anchor(self, instance):
            return "Profile"

        self.assertEqual(profile_anchor(None, person), "-")

    def test_one_to_one_rel_anchor_generation(self):
        person = Person.objects.create()
        profile = Profile.objects.create(person=person)
        self.assertIsInstance(person._meta.get_field("profile"), models.OneToOneRel)

        @admin_anchor(field_name="profile")
        def profile_anchor(self, instance):
            return "Profile"

        self.assertEqual(
            profile_anchor(None, person),
            f"<a href='/admin/tests/profile/{profile.id}/change/'>Profile</a>",
        )

    def test_one_to_one_field_anchor_generation(self):
        person = Person.objects.create()
        profile = Profile.objects.create(person=person)
        self.assertIsInstance(profile._meta.get_field("person"), models.OneToOneField)

        @admin_anchor(field_name="person")
        def person_anchor(self, instance):
            return "Person"

        self.assertEqual(
            person_anchor(None, profile),
            f"<a href='/admin/tests/person/{person.id}/change/'>Person</a>",
        )

    def test_foreign_key_anchor_generation(self):
        article = Article.objects.create()
        comment = Comment.objects.create(article=article)
        self.assertIsInstance(comment._meta.get_field("article"), models.ForeignKey)

        @admin_anchor(field_name="article")
        def article_anchor(self, instance):
            return "Article"

        self.assertEqual(
            article_anchor(None, comment),
            f"<a href='/admin/tests/article/{article.id}/change/'>Article</a>",
        )

    def test_many_to_one_rel_anchor_generation(self):
        article = Article.objects.create()
        Comment.objects.create(article=article)
        self.assertIsInstance(article._meta.get_field("comments"), models.ManyToOneRel)

        @admin_anchor(field_name="comments")
        def comments_anchor(self, instance):
            return "Comments"

        self.assertEqual(
            comments_anchor(None, article),
            f"<a href='/admin/tests/comment/?article__id={article.id}'>Comments</a>",
        )

    def test_many_to_many_rel_anchor_generation(self):
        member = Member.objects.create()
        self.assertIsInstance(member._meta.get_field("groups"), models.ManyToManyRel)

        @admin_anchor(field_name="groups")
        def groups_anchor(self, instance):
            return "Groups"

        self.assertEqual(
            groups_anchor(None, member),
            f"<a href='/admin/tests/group/?members__id={member.id}'>Groups</a>",
        )

    def test_many_to_many_field_anchor_generation(self):
        group = Group.objects.create()
        self.assertIsInstance(group._meta.get_field("members"), models.ManyToManyField)

        @admin_anchor(field_name="members")
        def members_anchor(self, instance):
            return "Members"

        self.assertEqual(
            members_anchor(None, group),
            f"<a href='/admin/tests/member/?groups__id={group.id}'>Members</a>",
        )
