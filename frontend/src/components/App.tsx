import React, {useEffect, useState} from 'react'
import Sidebar from "./Sidebar";
import '../styles/main.scss'
import MapData from "./MapData";
import axios from "axios";

interface Route {
    station : string,
    time : string,
}
export enum SIDEBAR_STEPS {
    INFO,
    CALENDAR,
    FAQ
}

function App() {

    const API_URL_TIME = 'http://localhost:5000/api/train_destinations'
    const API_URL_DISL = 'http://localhost:5000/api/actual_destinations'

    const [trainsByStations, setTrainsByStations] = useState<any>({})
    const [routeList, setRouteList] = useState<Route[]>([])
    const [selectedStation, setSelectedStation] = useState<any>(0)
    const [openedStep, setOpenedStep] = useState<SIDEBAR_STEPS>(SIDEBAR_STEPS.INFO)
    const [trainId, setTrainId] = useState<any>(0)

    // "train_id": dest.train_id,
    //  "st_id": dest.st_id,
    //  "longitude": dest.longitude,
    //  "latitude": dest.latitude

    const handleLoadRoute = (_trainId : any) => {
        setOpenedStep(SIDEBAR_STEPS.CALENDAR)
        setTrainId(_trainId)
        axios(API_URL_TIME, {
            params: {
                'train_id' : _trainId
            }
        })
            .then(response => {
                setRouteList(response.data)
            })
    }

    const sendRequestToServerDisl = () => {
        axios(API_URL_DISL)
            .then(response => {
                let data = response.data
                let distributionByStations = {}
                data.forEach((el : any) => {
                    // @ts-ignore
                    if (!distributionByStations[el.st_id]?.length) {
                        // @ts-ignore
                        distributionByStations[el.st_id] = []
                    }
                    // @ts-ignore
                    distributionByStations[el.st_id].push(el.train_id)
                })
                setTrainsByStations(distributionByStations)
            })
    }

    useEffect(() => {
        sendRequestToServerDisl()
        let int = setInterval(() => {
            sendRequestToServerDisl()
        }, 10000)
        return () => { clearInterval(int) }
    }, []);


    const handleStationClicked = (stationId : any) => {
        setOpenedStep(SIDEBAR_STEPS.INFO)
        setSelectedStation(stationId)
    }

    return (
        <div className="App">
            <div className="App__Sidebar">
                <MapData trainsByStations={trainsByStations} handleStationClicked={handleStationClicked} />
            </div>
            <div className="App__Content">
                <Sidebar trainId={trainId} openedStep={openedStep} setOpenedStep={setOpenedStep} handleLoadRoute={handleLoadRoute} selectedStation={selectedStation} trainsByStations={trainsByStations} routeList={routeList} />
            </div>
        </div>
    )

}

export default App
