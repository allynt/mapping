# mapping

Simple API to generate _vector tiles_ from _GeoJSON_ using `tippecanoe`.

__API:__

endpoint (POST): &lt;server&gt;:5000/api/v1/tippecanoe/

input:
```
{
  basename: "name of generated tileset",
  geojson: "raw geojson data",
  min_zoom: "minimum zoom level (optional)",
  max_zoom: "maximum zoom level (optional)",
  min_detail: "minimum detail level (optional)",
  max_detail: "maximum detail level (optional)",
}
```

output: 
_binary vector tile data_
