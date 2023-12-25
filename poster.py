from io import BytesIO

from discord_webhook import DiscordWebhook


class Poster:
    def __init__(self, webhook_urls, message_ids, role_ids):
        self.__webhook_urls = webhook_urls
        self.__message_ids = message_ids
        self.__role_ids = role_ids

    def post(self, schedules, week, is_holiday):
        """Posts the schedules on discord"""
        for group_id, schedule in schedules.items():
            message = self.__get_message(week, is_holiday, group_id)
            self.__post_schedule(group_id, schedule, message)

    def __post_schedule(self, group_id, schedule, message):
        """Posts the schedule of the group on discord"""
        webhook = DiscordWebhook(url=self.__webhook_urls[group_id], content=message, id=self.__message_ids[group_id])
        if schedule != "F":
            with BytesIO() as img_bin:
                schedule.save(img_bin, format="PNG")
                img_bin.seek(0)
                webhook.add_file(file=img_bin, filename=f"horaire.png")
                webhook.edit()
        else:
            webhook.clear_attachments()
            webhook.edit()

    def __get_message(self, week, is_holiday, group_id):
        """Returns the message to post on discord"""
        if is_holiday:
            return f"La semaine {week} est une semaine de congé :sunglasses: Profitez-en bien! <@&{self.__role_ids[group_id]}>"
        return f"Planning de la semaine {week} pour le <@&{self.__role_ids[group_id]}>"
