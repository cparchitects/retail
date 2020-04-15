import clr

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc = DocumentManager.Instance.CurrentDBDocument

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import XYZ, Line, Wall

width = IN[0]
depth = IN[1]
level = UnwrapElement(IN[2])
wallType = UnwrapElement(IN[3])

pt1 = XYZ(0, 0, 0)
pt2 = XYZ(width, 0, 0)
pt3 = XYZ(width, depth, 0)
pt4 = XYZ(0, depth, 0)

pts = [pt1, pt2, pt3, pt4]
walls = []

TransactionManager.Instance.EnsureInTransaction(doc)
for n, pt in enumerate(pts):
	try:
            wall_line = Line.CreateBound(pt, pts[n+1])
	except IndexError:
            wall_line = Line.CreateBound(pt, pts[0])
	wall = Wall.Create(doc, wall_line, level.Id, False)
	walls.append(wall.ToDSType(False))

TransactionManager.Instance.TransactionTaskDone()	

OUT = walls