import json

ISO8601_FORMAT_Z = "%Y-%m-%dT%H:%M:%S.%fZ"
METERS_PER_NAUTICAL_MILE = 1852


class Packet:
    def __init__(self):
        self.properties = {}

    def initialize_from_json(self):
        pass

    def initialize_flight_path(self, id, name, model_static_path, flight_path_datetime, flight_path):
        self.properties['id'] = id
        self.properties['name'] = name
        self.properties['model'] = {
            "gltf": model_static_path,
            "scale": 1.0,
            "minimumPixelSize": 64
        }
        self.properties['position'] = {
            "interpolationAlgorithm": "LAGRANGE",
            "interpolationDegree": 1,
            "cartographicDegrees": []
        }
        for position in flight_path:
            print(f'position in cesium flight path packet is {position}')
            self.properties['position']['cartographicDegrees'].extend(
                [
                    (flight_path_datetime + position[2]).strftime(ISO8601_FORMAT_Z),
                    position[0].x,
                    position[0].y,
                    position[1] * METERS_PER_NAUTICAL_MILE
                ]
            )
        self.properties['orientation'] = {
            "velocityReference": f'#{id}#position'
        }


class CZMLDocument:
    def __init__(self, start_time, stop_time, name=None):
        
        # hold packets
        self.packets = []

        # hold ids
        self.packet_id = 0

        # hold init
        self.start_time = start_time

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

    def next_packet_id(self):
        self.packet_id += 1
        return self.packet_id

    def to_json_string(self):

        output_list = []
        for packet in self.packets:
            output_list.append(packet.properties)

        return json.dumps(output_list)
    
    def to_json(self):

        output_list = []
        for packet in self.packets:
            output_list.append(packet.properties)

        return output_list
    
    def add_flight_path_packets(self, model_static_path, flight_path_datetime, flight_paths):
        print(f'in cesium document flight path flight_paths are {flight_paths}')
        for flight_path in flight_paths:
            packet = Packet()
            packet.initialize_flight_path(self.next_packet_id(), "Pickup", model_static_path, flight_path_datetime, flight_path)
            self.packets.append(packet)

        
