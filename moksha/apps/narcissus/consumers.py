from moksha.api.hub import Consumer
from pprint import pformat
from pygeoip import GeoIP, GEOIP_MEMORY_CACHE

import geojson
import simplejson

class HttpLightConsumer(Consumer):
    topic = 'httpdlight_http_rawlogs'

    geoip_url = '/'.join(__file__.split('/')[:-3] +
                         ["public/data/GeoLiteCity.dat"])
    gi = GeoIP(geoip_url, GEOIP_MEMORY_CACHE)

    def consume(self, message):
        if not message:
            #self.log.warn("%r got empty message." % self)
            return
        #self.log.debug("%r got message '%s'" % (self, message))
        words = message['body'].split()
        rec = self.gi.record_by_addr(words[0])
        if words[0] and rec and rec['latitude'] and rec['longitude']:
            obj = {
                'ip' : words[0],
                'lat' : rec['latitude'],
                'lon' : rec['longitude'],
            }
            #self.log.debug("%r built %s" % (self, pformat(obj)))
            self.send_message('http_latlon', obj)
        else:
            #self.log.warn("%r failed on '%s'" % (self, message))
            pass

class LatLon2GeoJsonConsumer(Consumer):
    topic = 'http_latlon'

    def consume(self, message):
        if not message:
            #self.log.warn("%r got empty message." % self)
            return
        #self.log.debug("%r got message '%s'" % (self, message))
        msg = message['body']

        feature = geojson.Feature(
            geometry=geojson.Point([msg['lon'], msg['lat']])
        )
        collection = geojson.FeatureCollection(features=[feature])
        obj = simplejson.loads(geojson.dumps(collection))
        self.send_message('http_geojson', obj)
