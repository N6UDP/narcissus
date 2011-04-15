from moksha.api.hub import Consumer
from pprint import pformat
import GeoIP

class NarcissusConsumer(Consumer):

    # The message topic to listen to.
    topic = 'moksha.test'

    # Automatically decode message as JSON, and encode when using self.send_message
    jsonify = True

    def consume(self, message):
        self.log.info("%r.consume(%r)" % (self, message))

class HttpLightConsumer(Consumer):
    topic = 'httplight_http_rawlogs'
    jsonify = True

    geoip_url = "/usr/share/GeoIP/GeoLiteCity.dat"
    gi = GeoIP.open(geoip_url, GeoIP.GEOIP_MEMORY_CACHE)

    def consume(self, message):
        if not message:
            self.log.warn("%r got empty message." % self)
            return
        words = message.split()
        rec = self.gi.record_by_addr(words[0])
        if words[0] and rec and rec['latitude'] and rec['longitude']:
            obj = {
                'ip' : words[0],
                'lat' : rec['latitude'],
                'lon' : rec['longitude'],
            }
            self.log.info("%r got %s" % (self, pformat(obj)))
            self.send_message('http_latlon', obj)
        else:
            self.log.warn("%r failed on '%s'" % (self, message))
