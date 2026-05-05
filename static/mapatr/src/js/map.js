'use strict';

const CASTERS = [
  // { name: 'BASE',               file: 'BASE.geojson',   color: '#888888' },
  // { name: 'SIRGAS (Exp)',       file: 'SIRGAS.geojson',  color: 'orange' },
  { name: 'IGS-RT',            file: 'IGS.geojson',     color: 'red' },
  { name: 'IBGE-IP (Br)',      file: 'IBGE.geojson',    color: 'green' },
  { name: 'REGNA-SGM (Uy)',    file: 'REGNA.geojson',   color: 'LightSkyBlue' },
  { name: 'RAMSAC-NTRIP (Ar)', file: 'IGN.geojson',     color: 'blue' },
];

const map = L.map('map').setView([-42, -60.5], 4);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  maxZoom: 18,
}).addTo(map);

L.control.scale({ imperial: false }).addTo(map);

function buildPopup(p) {
  const misc = p.misc ? `<li>${p.misc}</li>` : '';
  return `<div style="font-size:small">
    <span style="font-weight:bold;font-size:1.2em;color:${p.color}">${p.name}</span>
    <ul style="margin:4px 0 0 0;padding-left:1.2em">
      <li>${p.coordinates}</li>
      <li>${p.identifier}, ${p.country}</li>
      <li>${p.data_format}, ${p.nav_system}</li>
      ${misc}
    </ul>
  </div>`;
}

const overlays = {};
let pending = CASTERS.length;

CASTERS.forEach(({ name, file, color }) => {
  fetch(file)
    .then(r => r.json())
    .then(data => {
      const layer = L.geoJSON(data, {
        pointToLayer: (feature, latlng) =>
          L.circleMarker(latlng, {
            radius: 5,
            color: 'rgba(0,0,0,0.3)',
            weight: 2,
            fillColor: feature.properties.color || color,
            fillOpacity: 1,
          }),
        onEachFeature: (feature, layer) =>
          layer.bindPopup(buildPopup(feature.properties)),
      }).addTo(map);
      overlays[name] = layer;
    })
    .catch(() => { /* caster sin datos: ignorar */ })
    .finally(() => {
      pending--;
      if (pending === 0) {
        L.control.layers(null, overlays, { collapsed: false }).addTo(map);
      }
    });
});
