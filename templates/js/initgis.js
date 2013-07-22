var map;

function Geometry(symbol, maxSize, maxValue){
    this.symbol = symbol;
    this.maxSize = maxSize;
    this.maxValue = maxValue;
 
    this.getSize = function(value){
        switch(this.symbol) {
            case 'circle': // Returns radius of the circle
            case 'square': // Returns length of a side
                return Math.sqrt(value/this.maxValue)*this.maxSize;
            case 'bar': // Returns height of the bar
                return (value/this.maxValue)*this.maxSize;
            case 'sphere': // Returns radius of the sphere
            case 'cube': // Returns length of a side
                return Math.pow(value/this.maxValue, 1/3)*this.maxSize;
        }
    }
}

function initmap() {

    var max_value = 500000;
    var symbol = new Geometry('circle', 1, max_value);

    var options = {
        projection: new OpenLayers.Projection("EPSG:900913"),
        displayProjection: new OpenLayers.Projection("EPSG:4326"),
        units: "m",
        numZoomLevels: 18,
        maxResolution: 156543.0339,
    };

    map = new OpenLayers.Map('map', options);
    map.addControl(new OpenLayers.Control.LayerSwitcher());
    var template = {
        strokeColor : 'rgb(220,0,0)', 
        strokeWidth: 2,
        strokeOpacity: 0.9,
        fillColor : 'rgb(220,0,0)', 
        fillOpacity : 0.5, 
        pointRadius: "${getSize}"
    };

    var style = new OpenLayers.Style(template);
    var styleMap = new OpenLayers.StyleMap({
        'default': style, 
        'select': {
            fillColor: 'red',
            fillOpacity: 0.75
        }
    });


    
    var gmap = new OpenLayers.Layer.Google(
        "Google Streets", // the default
        {
	    'isBaseLayer':true
	}
    );

    var local = new OpenLayers.Layer.WMS(
        "Nacional por Provincias",
        "http://localhost:8000/",
        {layers: "NACIONAL_POR_PROVINCIAS"}
    );
    map.addLayers([gmap]);

    //creating a tool to read in WKT formatted geospatial data
    var wkt_f = new OpenLayers.Format.WKT();

    // Loop through all emprendimientos and make a vector layer for each como puntos
    {% for object in object_list %}
    var point_{{ object.id }} = wkt_f.read('{{ object.point }}');
    point_{{ object.id }}.data = { 'empr_name': "{{ object.nombre }}",'empr_code': "{{ object.f_code }}", };
    {% endfor %}

    // poligono de empremdimientos convex_hull
    var polygon = new OpenLayers.Format.WKT();
    var polygon_all = polygon.read('{{ poligono }}');
    var zone = new OpenLayers.Layer.Vector("Zonas");
    zone.addFeatures([polygon_all])

    var companies_vector = new OpenLayers.Layer.Vector("Emprendimientos");
//    companies_vector.addFeatures([{% for object in object_list %}point_{{ object.id }}{% if not forloop.last %},{% endif %}{% endfor %}]);

    var selectControl = new OpenLayers.Control.SelectFeature(companies_vector, 
							     {
								 hover: true,
								 onSelect: select_feature,
								 onUnselect: unselect_feature,
							     });
//    map.addLayer(companies_vector);
    map.addLayer(zone);
    map.addControl(selectControl);
    selectControl.activate();
    var lon=-79.2; 
    var lat=-2.9;
    var zoom=8;
    map.setCenter(new OpenLayers.LonLat(lon, lat), zoom);

    function onPopupClose(evt) {
        selectControl.unselect(selectedFeature);
    }
    function select_feature(feature) {
        selectedFeature = feature;
        popup = new OpenLayers.Popup.AnchoredBubble("chicken", 
                                new OpenLayers.LonLat(-85.1, -1.0),
                                new OpenLayers.Size(210,90), // Size of the bubble
						    "<div class='bubblewrap'><p class='county-hed'>" + feature.data.empr_name + "</p><p style='margin-bottom:0px;'>Codigo:&nbsp;" + feature.data.empr_code + "</p>", 
                                null, 
                                false, // closebox?
                                onPopupClose // on close function
                                );
        feature.popup = popup;
        map.addPopup(popup);
    }
    function unselect_feature(feature) {
        map.removePopup(feature.popup);
        feature.popup.destroy();
        feature.popup = null;
    }

};


function callBackData(data){
    if (data){
	var item = data;
    }
};

function getQuery(){
    q = $('#homepage-input').val();
    var params = {regexp: q};
    $.getJSON("/entergis/search/", params, function(data){
	if (data){
	    createLayer(data);
	}
    });
}

function addClickHandlers(){
    $('#buttonSearch').click(function(){getQuery();});
//    $('#browser').localScroll();
    $('#browser').treeview();
    var branches = $({% include 'tree_view.html' %}).appendTo("#browser");
 	$("#browser").treeview({
 		add: branches
 	});
}

$(document).ready(addClickHandlers);
