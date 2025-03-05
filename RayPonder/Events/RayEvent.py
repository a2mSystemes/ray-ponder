from RayPonder.Events import RayEventType, EventProducerType

class RayEvent:
    def __init__(self, ray_event=RayEventType.Unknown, producer=None, producer_type=EventProducerType.Unknown):
        self.producer = producer
        self.producer_type = producer_type
        self.ray_event = ray_event
        
class PhyRayEvent(RayEvent):
    def __init__(self, ray_event, producer ):
        super().__init__(producer_type=EventProducerType.Keyboard)
        self.producer = producer
        self.ray_event = ray_event
        
class PlayerEvent(RayEvent): 
    def __init__(self, producer_type=EventProducerType.Player):
        super().__init__(producer_type=producer_type)
    
