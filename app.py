from flask import Flask, render_template, request, jsonify, url_for
from form import MapForm
import pathFind,busFind


#from config import Config

app = Flask(__name__)

app.config['SECRET_KEY'] = '4cfbdadf2d991953407bb0942aa37e3a'


@app.route('/')
def home_page():
    form = MapForm()
    global buslist, busliststr
    global busStatus, choiceStatus
    firststartup = True
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

    busArray = busFind.search(startarr, endarr)

    #print(busArray)
    latlong = []

    if BestPathChoice == "walk":
        firststartup = False
        choiceStatus = "walk"
        for row in pathArray:
            lat = row[1]
            long = row[0]
            newCoordinates = [float(long), float(lat)]
            latlong.append(newCoordinates)

        latlong.insert(0,startarr)
        latlong.append(endarr)

    elif BestPathChoice == "bus":
        firststartup = False
        choiceStatus = "bus"
        if busArray is None:
            busStatus = False
        if busArray is not None:
            busStatus = True
            for row in busArray[1:]:
                lat = row[0][1]
                long = row[0][0]
                #print(long)
                newCoordinates = [float(long), float(lat)]
                latlong.append(newCoordinates)

            latlong.insert(0,startarr)
            latlong.append(endarr)
            buslist = busArray[0]
            busliststr = "Bus services available: "
            for b in buslist:
                busliststr += b + ", "


    print(latlong)

    data = latlong

    if firststartup is True:
        nobusstr = ""
        return render_template('home.html', form=form, methods=['GET'], path=BestPathChoice, station=MRTLRTLocation,
                               hdb=HDBLocation, data=data, bus=nobusstr)

    elif firststartup is False and choiceStatus == "walk":
        nobusstr = ""
        return render_template('home.html', form=form, methods=['GET'], path=BestPathChoice, station=MRTLRTLocation,
                               hdb=HDBLocation, data=data, bus=nobusstr)

    elif choiceStatus == "bus" and busStatus is False and firststartup is False:
        busliststrNone = "No bus services available"
        return render_template('home.html', form=form, methods=['GET'], path=BestPathChoice, station=MRTLRTLocation,
                               hdb=HDBLocation, data=data, bus=busliststrNone)

    elif choiceStatus == "bus" and busStatus is True and firststartup is False:
        print("has value")
        newbusliststr = busliststr[:-2]
        return render_template('home.html', form=form, methods=['GET'], path=BestPathChoice, station=MRTLRTLocation,
                               hdb=HDBLocation, data=data, bus=newbusliststr)


if __name__ == '__main__':
    app.run(debug=True)
