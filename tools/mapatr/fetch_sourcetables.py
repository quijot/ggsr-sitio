#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Descarga sourcetables de casters NTRIP y genera archivos GeoJSON.
Output: static/mapatr/{CASTER}.geojson

Los casters NTRIP responden con "SOURCETABLE 200 OK" en lugar de HTTP estándar,
por lo que se usa socket en lugar de urllib.

Sin dependencias externas (solo stdlib Python 3).
Uso: python tools/mapatr/fetch_sourcetables.py
"""

import json
import pathlib
import socket
import sys
from urllib.parse import urlparse

OUTPUT_DIR = pathlib.Path(__file__).parent.parent.parent / "static" / "mapatr"

TIMEOUT = 20  # segundos por caster

CASTERS = [
    # {"name": "SIRGAS", "url": "http://200.3.123.65:2101/",          "color": "orange",       "align": "right", "bline": "middle"},
    {"name": "IGN",    "url": "http://ntrip.ign.gob.ar:2101/",      "color": "blue",         "align": "left",  "bline": "baseline"},
    {"name": "REGNA",  "url": "http://201.217.132.178:2101/",       "color": "LightSkyBlue", "align": "left",  "bline": "baseline"},
    {"name": "IBGE",   "url": "http://gps-ntrip.ibge.gov.br:2101/", "color": "green",        "align": "left",  "bline": "baseline"},
    {"name": "IGS",    "url": "http://www.igs-ip.net:2101/",        "color": "red",          "align": "left",  "bline": "middle"},
]


def fetch_sourcetable(url):
    """
    Descarga el sourcetable de un caster NTRIP usando socket raw.
    Los casters NTRIP responden con "SOURCETABLE 200 OK" en lugar de
    "HTTP/1.1 200 OK", por lo que urllib.request no los puede parsear.
    """
    parsed = urlparse(url)
    host = parsed.hostname
    port = parsed.port or 2101
    path = parsed.path or "/"

    request = (
        f"GET {path} HTTP/1.0\r\n"
        f"Host: {host}\r\n"
        f"User-Agent: NTRIP BKG Ntrip Client/20190609\r\n"
        f"\r\n"
    ).encode()

    with socket.create_connection((host, port), timeout=TIMEOUT) as s:
        s.sendall(request)
        chunks = []
        while True:
            chunk = s.recv(8192)
            if not chunk:
                break
            chunks.append(chunk)

    raw = b"".join(chunks).decode("utf-8", errors="replace")

    # Saltar los headers de la respuesta (antes de la primera línea en blanco)
    _, sep, body = raw.partition("\r\n\r\n")
    if not sep:
        _, sep, body = raw.partition("\n\n")
    return body if sep else raw


def parse_features(text, color, align, bline):
    features = []
    for line in text.splitlines():
        if not line.startswith("STR"):
            continue
        arr = line.split(";")
        if len(arr) < 18:
            continue
        try:
            lat = float(arr[9])
            lon = float(arr[10])
        except ValueError:
            continue

        carrier_val = arr[5]
        carrier = ("L%s" % carrier_val) if carrier_val not in ("0", "") else "No info"
        solution = "network" if arr[12] != "0" else "single base"
        misc = arr[18].strip() if len(arr) > 18 else ""

        def esc(s):
            return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ").strip()

        features.append({
            "type": "Feature",
            "properties": {
                "name":           esc(arr[1]),
                "identifier":     esc(arr[2]),
                "data_format":    esc(arr[3]),
                "format_details": esc(arr[4]),
                "carrier":        carrier,
                "nav_system":     esc(arr[6]),
                "network":        esc(arr[7]),
                "country":        esc(arr[8]),
                "coordinates":    "%s, %s" % (lat, lon),
                "solution":       solution,
                "misc":           esc(misc),
                "color":          color,
                "align":          align,
                "bline":          bline,
            },
            "geometry": {"type": "Point", "coordinates": [lon, lat]},
        })
    return features


def write_geojson(path, features):
    data = {
        "type": "FeatureCollection",
        "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
        "features": features,
    }
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    errors = []
    for c in CASTERS:
        name = c["name"]
        print(f"  {name} ({c['url']})... ", end="", flush=True)
        try:
            text = fetch_sourcetable(c["url"])
            features = parse_features(text, c["color"], c["align"], c["bline"])
            write_geojson(OUTPUT_DIR / f"{name}.geojson", features)
            print(f"OK ({len(features)} estaciones)")
        except Exception as e:
            print(f"ERROR: {e}")
            write_geojson(OUTPUT_DIR / f"{name}.geojson", [])
            errors.append(name)

    if errors:
        print(f"\nAdvertencia: fallaron los siguientes casters: {errors}", file=sys.stderr)
        print(f"\nGeoJSON generados en {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
