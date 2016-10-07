class ParentF:
    def WhoAreYou(self):
        print("ParentF")

class PointF(ParentF):
    def WhoAreYou(self):
        print("PointF")

class LineF(ParentF):
    def WhoAreYou(self):
        print("LineF")
        
class TriangleF(ParentF):
    def WhoAreYou(self):
        print("TriangleF")
        
class SquareF(ParentF):
    def WhoAreYou(self):
        print("SquareF")

class CircleF(ParentF):
    def WhoAreYou(self):
        print("CircleF")

v_Objs = [CircleF(), TriangleF(), LineF(), SquareF(), PointF()]

for i in range(0, len(v_Objs)):
    print(i)
    v_Objs[i].WhoAreYou()
    i = i + 1

