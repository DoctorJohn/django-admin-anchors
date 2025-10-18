from django.contrib import admin

from admin_anchors import admin_anchor


class TeamAdmin(admin.ModelAdmin):
    list_display = ["__str__", "captain_link", "captains_profile_link", "members_link"]

    @admin_anchor("captain")
    def captain_link(self, instance):
        return str(instance.captain)

    @admin_anchor("captain.profile")
    def captains_profile_link(self, instance):
        return "Captains profile"

    @admin_anchor("members")
    def members_link(self, instance):
        return f"{instance.members.count()} members"
