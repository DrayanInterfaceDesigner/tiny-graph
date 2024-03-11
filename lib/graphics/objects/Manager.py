
import threading
class Manager:
    def __init__(self):
        self.objects = []

    def add(self, obj):
        self.objects.append(obj)
        return obj

    def get_by_tag(self, tag:str):
        return [obj for obj in self.objects if obj.tag == tag]
    
    def get_by_range(self, prop:str, range:list):
        return [obj for obj in self.objects if range[0] <= getattr(obj, prop) <= range[1]]
    
    def get_by_distance(self, position, distance):
        return [[obj, obj.position.distance(position)] for obj in self.objects if obj.position.distance(position) <= distance]
        
    def get_by_property(self, prop:str, value:any):
        return [obj for obj in self.objects if getattr(obj, prop) == value]

    def remove(self, obj):
        obj.marked_for_removal = True
        self.objects.remove(obj)

    def update(self, dt):
        # sort objects by ['layer'] attribute, crescent order
        self.objects.sort(key=lambda x: x.layer)
        for obj in self.objects:
            obj.update(dt)
    
    def draw(self, ctx):
        for obj in self.objects:
            obj.draw(ctx)


# def draw(self, ctx):
#         # divide objects into 4 parts
#         size = len(self.objects)
#         parts = [self.objects[i*size//4:(i+1)*size//4] for i in range(4)]

#         # create and start a thread for each part
#         threads = []
#         lock = threading.Lock()
#         for part in parts:
#             thread = threading.Thread(target=self.draw_objects, args=(part, ctx, lock))
#             thread.start()
#             threads.append(thread)

#         # wait for all threads to finish
#         for thread in threads:
#             thread.join()

#     def draw_objects(self, objects, ctx, lock):
#         for obj in objects:
#             with lock:
#                 obj.draw(ctx)