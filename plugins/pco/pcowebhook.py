from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings
from plugins.pco import msg_attachment, announcements, live
import json
import logging
from datetime import datetime


class PcoWebhook(WillPlugin):
    """pcowebhook is for catching and dealing with Planning Center Webhooks"""

    @route("/slack/webhook", method='POST')
    def pco_webhook_endpoint(self):
        print("Got Slack webhook")
        logging.info("Got a webhook")
        data = self.request.json
        print(data)
        # self.add_to_schedule(when=datetime.now(), item=self.parse_pco_webhook(data))
        # self.parse_pco_webhook(data)
        return "Successfully recieved webhook!"

    @route("/pco/webhook", method='POST')
    def pco_webhook_endpoint(self):
        print("Got webhook")
        logging.info("Got a webhook")
        data = self.request.json
        # self.add_to_schedule(when=datetime.now(), item=self.parse_pco_webhook(data))
        self.parse_pco_webhook(data)
        return "Successfully recieved webhook!"

    def parse_pco_webhook(self, data):
        """Parsing should be done here and passed to other methods to deal with the event."""
        data = data['data'][0]
        endpoint = data['attributes']['name']
        payload = json.loads(data['attributes']['payload'])
        payload = payload['data']
        if endpoint == 'people.v2.events.person.updated':
            logging.info(("Person ID: %s" % payload['id']))
            logging.info(endpoint)
            pass
        elif endpoint == 'people.v2.events.person.created':
            self.person_created(payload)
        elif endpoint == 'services.v2.events.plan.live.updated':
            logging.info(endpoint)
            logging.info(("%s" % payload))
            self.live_service_updated(payload)
        return

    def person_created(self, data):
        if announcements.announcement_is_enabled(self, announcement='new_person_created'):
            pcoaddress = "https://people.planningcenteronline.com/people/" + data['id']
            attachment = msg_attachment.SlackAttachment("Lets all welcome %s!" % data['attributes']['name'],
                                                        text="New Person added to Planning Center!\n"
                                                             "Lets all welcome %s!" %
                                                             data['attributes']['name'],
                                                        button_text="Open in People",
                                                        button_url=pcoaddress)
            self.say("", channel=announcements.announcement_channel(self), attachments=attachment.slack())

    def live_service_updated(self, data):
        if announcements.announcement_is_enabled(self, announcement='live_service_update'):
            # pcoaddress = "https://people.planningcenteronline.com/people/" + data['id']
            meta_data = live.parse_live_hook(data)
            attachment = live.get_plan_item(meta_data['service_type'], meta_data['plan_id'], meta_data['item_id'])
            self.say("", channel=announcements.announcement_channel(self), attachments=attachment.slack())
