import React, {useEffect, useState} from 'react';
import { Map } from 'react-map-gl';

import maplibregl from 'maplibre-gl';
import DeckGL from '@deck.gl/react';
import { GeoJsonLayer } from '@deck.gl/layers';
import { AmbientLight, _SunLight as SunLight } from '@deck.gl/core';
import { scaleThreshold } from 'd3-scale';

// Source data GeoJSON
const DATA_URL = 'http://localhost:5000/static/coords.json';
const DATA_URL_POINTS = 'http://localhost:5000/static/pcoords.json';

export const COLOR_SCALE = scaleThreshold()
    .domain([-0.6, -0.45, -0.3, -0.15, 0, 0.15, 0.3, 0.45, 0.6, 0.75, 0.9, 1.05, 1.2])
    .range([
        [65, 182, 196],
        [127, 205, 187],
        [199, 233, 180],
        [237, 248, 177],
        [255, 255, 204],
        [255, 237, 160],
        [254, 217, 118],
        [254, 178, 76],
        [253, 141, 60],
        [252, 78, 42],
        [227, 26, 28],
        [189, 0, 38],
        [128, 0, 38],
    ]);

const INITIAL_VIEW_STATE = {
    latitude: 55.254,
    longitude: 30.13,
    zoom: 4,
    maxZoom: 16,
    pitch: 0,
};

const MAP_STYLE = 'https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json';

function getTooltip(x) {
    return (
        (x.object && x.object.properties && x.object.properties.st_id) && {
            html: `\
  <div><b>Станция #${x.object.properties.st_id}</b></div>
  <div>${x.object.properties.title}</div>
  `,
        }
    );
}

export default function MapData(props) {

    const [zoom, setZoom] = useState(1)
    const [zoomP, setZoomP] = useState(1)

    const layers = [

        new GeoJsonLayer({
            id: 'geojson',
            data: DATA_URL,
            opacity: 0.2,
            stroked: true,
            filled: false,
            extruded: false,
            wireframe: true,
            getLineColor: [120, 120, 120],
            getLineWidth: zoom,
            pickable: true,
        }),
        new GeoJsonLayer({
            id: 'geojson1',
            data: DATA_URL_POINTS,
            opacity: 1,
            filled: true, // Use filled instead of stroked for points
            radiusScale: 1000, // Adjust the scale according to your preference
            getRadius: zoomP, // You can also use a function to determine the radius dynamically
            getFillColor: [112, 54, 189], // Set the fill color for points
            pickable: true,
            onClick: (object) => {
                props.handleStationClicked(object.object.properties.st_id)
            }
        }),
    ];

    useEffect(() => {
        setZoomP(zoomP + 0.0001)
    }, [props.trainsByStations])



    return (
        <DeckGL
            layers={layers}
            initialViewState={INITIAL_VIEW_STATE}
            controller={true}
            getTooltip={getTooltip}
            onViewStateChange={({ viewState }) => {
                setZoom(20000 / Math.pow(1.7, viewState.zoom))
                setZoomP(8000 / Math.pow(1.3, viewState.zoom))
            }}
        >
            <Map reuseMaps mapLib={maplibregl} mapStyle={MAP_STYLE} preventStyleDiffing={false} />
        </DeckGL>
    );
}
