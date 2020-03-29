from flask import Flask, render_template, request, jsonify, url_for
from form import MapForm
import pathFind,busFind


#from config import Config

app = Flask(__name__)

app.config['SECRET_KEY'] = '4cfbdadf2d991953407bb0942aa37e3a'


@app.route('/')
def home_page():
    form = MapForm()
    BestPathChoice = request.args.get('BestPathChoice')
    MRTLRTLocation = request.args.get('MRTLocation')
    HDBLocation = request.args.get('HDBLocation')

    if MRTLRTLocation is not None:
        startarrsplit=MRTLRTLocation.split(",")
        startarr=[float(startarrsplit[1]),float(startarrsplit[0])]
    else:
        startarr = (103.9156265, 1.3947758)


    if HDBLocation is not None:
        endarrsplit = HDBLocation.split(",")
        endarr = [float(endarrsplit[1]), float(endarrsplit[0])]
    else:
        endarr = (103.9160709, 1.4031447)

    pathArray = pathFind.search(startarr, endarr, output="coords")


    busArray = busFind.search(startarr, endarr, output="coords")

    latlong2 = []

    latlong = []
    busStr = "The buses you can take is: "


    # if BestPathChoice == "walk":
    for row in pathArray:
        lat = row[1]
        long = row[0]
        newCoordinates = [float(long), float(lat)]
        latlong2.append(newCoordinates)

    if BestPathChoice == "bus":
        print(startarr)
        print(endarr)
        print(busArray)
        if busArray is not None:
            for bus in range(len(busArray[0])):
                busStr += (busArray[0][bus] + " ")

        # for row in range(1,len(busArray)):
        #     lat = row[1]
        #     long = row[0]
        #     newCoordinates = [float(long), float(lat)]
        #     latlong.append(newCoordinates)

    #print (busStr)

    latlong.insert(0,startarr)
    latlong.append(endarr)
    #print(startarr)
    #print(endarr)
    #print(latlong)
    #print(busArray)


    print(latlong2)






    data = latlong2
    #print(latlong)
    #print("here")
    #cleanData(data)
    #print(geoDict2)

    return render_template('home.html', form=form, methods=['GET'], path=BestPathChoice, station=MRTLRTLocation,
                           hdb=HDBLocation, data=data,busServices = busStr)



if __name__ == '__main__':
    app.run(debug=True)
