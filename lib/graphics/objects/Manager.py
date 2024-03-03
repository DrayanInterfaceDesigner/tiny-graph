

class Manager:
    def __init__(self):
        self.objects = []

    def add(self, obj):
        self.objects.append(obj)
        return obj

    def remove(self, obj):
        self.objects.remove(obj)

    def update(self, dt):
        # sort objects by ['layer'] attribute, crescent order
        self.objects.sort(key=lambda x: x.layer)
        for obj in self.objects:
            obj.update(dt)
    
    def draw(self, ctx):
        for obj in self.objects:
            obj.draw(ctx)