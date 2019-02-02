from pyproj import Proj, transform

SourceSystem = 'EPSG:26912'
OutputSystem = 'EPSG:4326'
inProj = Proj(init=SourceSystem)
outProj = Proj(init=OutputSystem)
x1,y1 = 428774.9288,4537853.049


x2,y2 = transform(inProj,outProj,x1,y1)
print x2,y2