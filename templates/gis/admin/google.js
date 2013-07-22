{% extends "gis/admin/openlayers.js" %}
{% block base_layer %}new OpenLayers.Layer.Google("Google Streets", { numZoomLevels: 20});{% endblock %}

{% block extra_layers %}
var layercantones = new OpenLayers.Layer.WMS( "Cantones del Azuay","http://localhost:8080/",{layers: "entergis_canton", transparent:true},
					      {isBaseLayer: false});
var gphy = new OpenLayers.Layer.Google("Google Physical",
				       {type: G_PHYSICAL_MAP}
				       );
var ghyb = new OpenLayers.Layer.Google("Google Hybrid",
				       {type: G_HYBRID_MAP, numZoomLevels: 20}
				       );
var gsat = new OpenLayers.Layer.Google("Google Satellite",
				       {type: G_SATELLITE_MAP, numZoomLevels: 22}
				       );
{{ module }}.map.addLayers([layercantones]);
{{ module }}.map.setCenter(new OpenLayers.LonLat(-79.1, -2.9), 8);
{% endblock %}
