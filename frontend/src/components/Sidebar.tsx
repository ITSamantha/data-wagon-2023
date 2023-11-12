import React, {useEffect, useState} from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faInfo } from '@fortawesome/free-solid-svg-icons'
import { faQuestion } from '@fortawesome/free-solid-svg-icons'
import { faCalendarAlt } from '@fortawesome/free-solid-svg-icons'
import axios from "axios";
import {SIDEBAR_STEPS} from "./App";


function Sidebar(props : any) {

    const API_URL_WAGONS = 'http://localhost:5000/api/actual_wagons'

    const [wagons, setWagons] = useState<any[]>([])
    useEffect(() => {
        axios.get(API_URL_WAGONS, {
            params: {
                train_id: props.trainId
            }
        }).then((response) => {
            if (response.status === 200 && response.data)
                setWagons(response.data.wagons ? response.data.wagons : [])
        })
    }, [props.trainId]);

    useEffect(() => {
        console.log(props.trainsByStations)
    }, [props.trainsByStations])


    return (
        <div className="Sidebar">
            <div className="Sidebar__Wrapper">
                <h1>Карта движения поездов</h1>
                <div className="Sidebar__Menu">
                    <div onClick={() => props.setOpenedStep(SIDEBAR_STEPS.INFO) } className={"Sidebar__Menu__Item " + (props.openedStep === SIDEBAR_STEPS.INFO && '_active')}>
                        <FontAwesomeIcon icon={faInfo} />
                    </div>
                    <div onClick={() => props.setOpenedStep(SIDEBAR_STEPS.CALENDAR) } className={"Sidebar__Menu__Item " + (props.openedStep === SIDEBAR_STEPS.CALENDAR && '_active')}>
                        <FontAwesomeIcon icon={faCalendarAlt} />
                    </div>
                    <div onClick={() => props.setOpenedStep(SIDEBAR_STEPS.FAQ) } className={"Sidebar__Menu__Item " + (props.openedStep === SIDEBAR_STEPS.FAQ && '_active')}>
                        <FontAwesomeIcon icon={faQuestion} />
                    </div>
                </div>
                <div className="Sidebar__Content">
                    {
                        props.openedStep === SIDEBAR_STEPS.INFO && (
                            <>
                                <h2>На текущей станции находится (или уже отправилось) {props.trainsByStations[props.selectedStation]?.length ?? 0 } поездов</h2>
                                {
                                    props.trainsByStations[props.selectedStation]?.map((el : any) => (
                                        <h1 style={{ marginTop: '5px', cursor: 'pointer' }} onClick={() => { props.handleLoadRoute(el) }}>Поезд #{el}</h1>
                                    ))
                                }
                            </>
                        )
                    }
                    {
                        props.openedStep === SIDEBAR_STEPS.CALENDAR && (
                            <>
                                <div className="Sidebar__Calendar">
                                    <h1>Поезд { props.trainId ? props.trainId : 'не выбран' }</h1>
                                    <p>Список вагонов, прикреплённых к поезду: </p>
                                    <p>{
                                        wagons.map((el, index) => (
                                            <>{el}{ index !== wagons.length - 1 && ', ' }</>
                                        ))
                                    }</p>
                                    {/* TODO: create title and train identification (from and to) */}
                                    {/* TODO: поезд содержит куда, маршрут, какие вагоны */}
                                    {/* TODO: какие вагоны прикрепили и откреприли */}
                                    {/* TODO: где какой вагон отгрузят */}
                                    {
                                        props.routeList.length > 0 ?
                                            props.routeList.map((el : any) => (
                                            <div className="Sidebar__Calendar__Item _active">
                                                <div className="Sidebar__Calendar__Item__Icon"></div>
                                                <div className="Sidebar__Calendar__Item__Content">
                                                    <h4>{ el.station }</h4>
                                                    <p>{ el.time }</p>
                                                </div>
                                            </div>
                                        )) : <>
                                            <h2>Выберите станцию для того, чтобы узнать, какие поезда находятся на ней.</h2>
                                        </>
                                    }
                                </div>
                            </>
                        )
                    }
                    {
                        props.openedStep === SIDEBAR_STEPS.FAQ && (
                            <>
                                <div className="Sidebar__Calendar">
                                    <h1>Здесь должно быть FAQ, но мы не успели.</h1>
                                    <p>На вкладке расписания только тестовые данные, т.к. сервер реального времени не успел добавить достаточное количество данных.</p>
                                </div>
                            </>
                        )
                    }
                </div>
            </div>
        </div>
    )

}

export default Sidebar