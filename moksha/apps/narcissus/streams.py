from datetime import timedelta, datetime
from moksha.api.hub.producer import PollingProducer

import random

class RandomIPProducer(PollingProducer):
    frequency = timedelta(seconds=1.5)
    topic = 'httpdlight_http_rawlogs'

    def poll(self):
        """ This method is called by the MokshaHub reactor every `frequency` """

        msg = '%i.%i.%i.%i' % (*[random.randint(0,255) for i in range(4)])
        self.send_message(self.topic, msg)
