from django.db import models


class Person(models.Model):
    pass


class Profile(models.Model):
    person = models.OneToOneField(
        Person, on_delete=models.CASCADE, related_name="profile"
    )


class Article(models.Model):
    pass


class Comment(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="comments"
    )


class Member(models.Model):
    pass


class Group(models.Model):
    members = models.ManyToManyField(Member, related_name="groups")
