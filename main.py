
import boto
import json

#http://stackoverflow.com/questions/924171/geo-fencing-point-inside-outside-polygon

def aws_connect_s3():

    print "Connecting to AWS S3 Bucket"
    s3 = boto.connect_s3()
    #bucket = s3.create_bucket('orion.geo.demo')  # bucket names must be unique
    
    bucket = s3.lookup('orion.geo.demo')

    if bucket is None:
        print "Bucket does not exist. Creating..."
        bucket = s3.create_bucket('orion.geo.demo')  # bucket names must be unique

    key = bucket.new_key('hello_world2.dat')
    key.set_contents_from_filename('hello.dat')
    key.set_acl('public-read')

def lf(file):
    path = "%s" %(file)
    json_data = None

    with open(path) as json_file:
        json_data = json.load(json_file)

    return json_data



def load_landmark():
    data = lf("landmark.json")

    #print json.loads(json.dumps(data))["data"]
    return json.loads(json.dumps(data))["data"]


def load_geofence():
    data = lf("geofence.json")

    #print json.loads(json.dumps(data))["data"]
    return json.loads(json.dumps(data))["data"]


def load_scan():
    data = lf("scan.json")

    #print json.loads(json.dumps(data))["data"]
    return json.loads(json.dumps(data))["data"]




def point_in_poly(x,y,poly):

    n = len(poly)
    inside = False

    print "polygon length: %s" % (n)
    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            print "pass 1"
            if y <= max(p1y,p2y):
                print "pass 2"
                if x <= max(p1x,p2x):
                    print "pass 3"
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside



if __name__ == "__main__":

    #aws_connect_s3()
    landmark = load_landmark()
    geofence = load_geofence()
    scan = load_scan()

    #print landmark['landmark']['lat']
    
    
    #polygon = [geofence['fence']['latsw'], geofence['fence']['latne'], geofence['fence']['lngsw'], geofence['fence']['lngne']]
    #polygon = [(geofence['fence']['latsw'], geofence['fence']['latne']),(geofence['fence']['lngsw'], geofence['fence']['lngne'])]
    polygon = [(geofence['fence']['latsw'], geofence['fence']['lngsw']),(geofence['fence']['latne'], geofence['fence']['lngne'])]
    
    #point = [scan['scan']['lat'], scan['scan']['lng']]

    point = [37.96747811844134, -87.35160827636719]

    print polygon
    print point

    #hit = point_in_poly(point[0], point[1], polygon)

    hit = point_in_poly(37.96747811844134, -87.35160827636719, polygon)
    print hit
    #print json.dumps(landmark)
    #print json.dumps(geofence)
    #print json.dumps(scan)




