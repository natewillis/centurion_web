import json

ISO8601_FORMAT_Z = "%Y-%m-%dT%H:%M:%S.%fZ"

class Packet:
    def __init__(self):
        self.properties = {}


class CZMLDocument:
    def __init__(self, start_time, stop_time, name=None):
        
        # hold packets
        self.packets = []

        # create preamble
        preamble = Packet()
        preamble.properties['id'] = "document"
        if name is None:
            preamble.properties['name']='simple'
        else:
            preamble.properties['name']=name
        preamble.properties['version']="1.0"
        preamble.properties['clock'] = {
            'interval': f'{start_time.strftime(ISO8601_FORMAT_Z)}/{stop_time.strftime(ISO8601_FORMAT_Z)}',
            'current_time': f'{start_time.strftime(ISO8601_FORMAT_Z)}',
            'multiplier': 60,
            'range': 'LOOP_STOP',
            'step': 'SYSTEM_CLOCK_MULTIPLIER'
        }
        self.packets.append(preamble) 

    def to_json(self):

        output_list = []
        for packet in self.packets:
            output_list.append(packet.properties)

        return json.dumps(output_list)
        