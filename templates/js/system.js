var mapPanel, toolbarItems = [];
var action;
var mymap;
var control;
var winhtml;

Ext.onReady(function() {

    var context = {
        getSize: function(feature) {
            return symbol.getSize(feature.data.num_socios) * Math.pow(2,mymap.getZoom()-1);
        }
    };

    Ext.QuickTips.init();
    toolbarItems.push( {% include 'site.html' %} );
    toolbarItems.push("-");

    var layerStyle = new OpenLayers.StyleMap({
        "default": new OpenLayers.Style({
            pointRadius: 10,//"${getSize}", // sized according to type attribute
            fillColor: "#66ccff",
            strokeColor: "#ff9933",
            strokeWidth: 2,
	    fillOpacity: 0.8,
        }, { context: context }),
        "select": new OpenLayers.Style({
            fillColor: "#d51717",
            strokeColor: "#3399ff"
        }, { context: context })
    });

    var wkt_f = new OpenLayers.Format.WKT();

    {% for object in object_list %}var point_{{ object.id }} = wkt_f.read('{{ object.point }}');
    point_{{ object.id }}.data = {
	'pointId':{{ object.id }}, 
	'name': "{{ object.nombre }}",
	'num_socios': {{ object.num_socios }},
	'url_info': "{{ object.url_info }}",
	'productos_json': "{{ object.productos_json }}"
    };
    {% endfor %}

/*    var wkt_cantones = new OpenLayers.Format.WKT();
    {% for obj in actores %}
    var poly_{{ obj.id }} = wkt_cantones.read('{{ obj.poly }}');
    poly_{{ obj.id }}.data = {
	'poly_id': {{ obj.id }},
	'name': "{{ obj.nombre }}",
	'tipo': "{{ obj.tipo }}"
    };
    {% endfor %}

    var wkt_areas = new OpenLayers.Format.WKT();

    {% for obj in areas %}
    var poly_{{ obj.id }} = wkt_areas.read('{{ obj.poly }}')
    poly_{{ obj.id }}.data = {
	'poly_id': {{ obj.id }},
	'name': "{{ obj.nombre }}"
    };
    {% endfor %}
    */


    function onPopupClose(evt){
	selectCtrl.unselect(selectedFeature);
    }

    function select_feature(feature){
	selectedFeature = feature;
	if (feature.geometry.x){
	    var x = feature.geometry.x;
	    var y = feature.geometry.y;
	}else{
	    var x = feature.geometry.bounds.left;
	    var y = feature.geometry.bounds.bottom;
	}

	var data = feature.data;
	winhtml = '';
	if (data.tipomodel == 'emprendimiento'){
	    winhtml =  '<b>Nombre: '+data.nombre+'</b><br><b>Actividad: '+data.activity+'</b><br><b>Sitio: '+data.url_info+'</b><br><b>Socios: '+data.num_socios+'</b><br><b>Area Produccion: '+data.area_produccion+'</b><br><b>Productos: '+data.productos_json+'</b><br><b>Ubicaciones: '+data.ubicaciones_json+'</b><br><b>Parroquia: '+data.parroquia+'</b>'
	}else if (data.tipomodel == 'zonaprod'){
	    winhtml = '<b>Nombre: '+data.nombre+'</b><br><b>Actividad: '+data.actividad+'</b><br><b>Productos: '+data.productos_json+'</b><br><b>Parroquia: '+data.parroquias_json+'</b>'
	}else{
	    winhtml = '<b>Nombre: '+data.nombre+'</b><br><b>Info: '+data.direccion+'</b><br><b>Sitio: '+data.url_info+'</b><br><b>Tecnicos: '+data.tecnicos_json+'</b>'
	}

	popup = new OpenLayers.Popup("chicken",
				     new OpenLayers.LonLat(x, y),
				     new OpenLayers.Size(210,90),
				     winhtml,
				     null,
				     false,
				     onPopupClose
				    );
	feature.popup = popup;
	mymap.addPopup(popup);
    }

    function unselect_feature(feature){
        mymap.removePopup(feature.popup);
        feature.popup.destroy();
        feature.popup = null;	
    }


    var areas_vector = new OpenLayers.Layer.Vector("Areas Productivas", {styleMap: layerStyle});
//    areas_vector.addFeatures([{%for obj in areas %}poly_{{ obj.id }}{% if not forloop.last %},{% endif %}{% endfor %}]);

    var actores_vector = new OpenLayers.Layer.Vector("Actores", {styleMap:layerStyle});
//    actores_vector.addFeatures([{%for obj in actores %}poly_{{ obj.id }}{% if not forloop.last %},{% endif %}{% endfor %}]);

    var companies_vector = new OpenLayers.Layer.Vector("Emprendimientos",{ styleMap:layerStyle});
    companies_vector.addFeatures([{% for object in object_list %}point_{{ object.id }}{% if not forloop.last %},{% endif %}{% endfor %}]);
    // create select feature control
    var selectCtrl = new OpenLayers.Control.SelectFeature([companies_vector],
							  {
							      highlightOnly:true,
							      clickout: true,
							      onSelect: select_feature,
							      onUnselect: unselect_feature,
							  });
							  
    var layerprovincias = new OpenLayers.Layer.WMS( "Provincias del Ecuador","http://"+document.location.hostname+":8080/",
					  {layers: "entergis_provincia",transparent:true}, {isBaseLayer: false});
    var layercantones = new OpenLayers.Layer.WMS( "Cantones del Azuay","http://localhost:8080/",
						  {layers: "entergis_canton", transparent:true}, {isBaseLayer: false});

    var gmap = new OpenLayers.Layer.Google( "Google (Base)", {isBaseLayer:true});

    mymap = new OpenLayers.Map({allOverlays: false, controls:[new OpenLayers.Control.PanZoom()]});
    mymap.addLayers([gmap, layerprovincias, layercantones]);//, companies_vector, actores_vector, areas_vector]);
    mymap.addControl(selectCtrl);
    selectCtrl.activate();


    mymap.addControl(new OpenLayers.Control.MousePosition());
    toolbarItems.push(new Ext.Toolbar.Spacer());
    action = new GeoExt.Action({
	text: "Navegar",
	map: mymap,
	toggleGroup: "group",
	waitMsg: "Cargando...",
	control: new OpenLayers.Control.Navigation(),
	tooltip:"Activa la opcion de navegacion",
    });
    toolbarItems.push(action);
    toolbarItems.push("-");
    toolbarItems.push(new Ext.Toolbar.Spacer());
    action = new GeoExt.Action({
	map: mymap,
	control: new OpenLayers.Control.ZoomBox(),
	toggleGroup: "group",
	text: "Zoom",
	tooltip: "Seleccione un cuadro",
    });
    toolbarItems.push([action,"-"])

    var jsonreader = new Ext.data.JsonReader({
	totalProperty: 'results',
	root: 'data',
	fields: [{"name":"nombre"}]
    });


    toolbarItems.push( {text:'Administración', handler: function(){window.location = '/admin/'}}, '-',{text: "Acerca de",handler: function(){treeConfigWin.show();}});

    var scaleStore = new GeoExt.data.ScaleStore({map:mymap});
    var zoomSelector = new Ext.form.ComboBox({
	store: scaleStore,
	emptyText: 'Zoom',
	tpl: '<tpl for="."><div class="x-combo-list-item">1 : {[parseInt(values.scale)]}</div></tpl>',
	editable: false,
	triggerAction: 'all',
	mode: 'local'
    });

    zoomSelector.on('select',
		    function(cmb, rec, index){mymap.zoomTo(rec.data.level);},
		    this
    );

    mymap.events.register('zoomend', this, function() {
        var scale = scaleStore.queryBy(function(record){
            return this.map.getZoom() == record.data.level;
        });

        if (scale.length > 0) {
            scale = scale.items[0];
            zoomSelector.setValue("1 : " + parseInt(scale.data.scale));
        } else {
            if (!zoomSelector.rendered) return;
            zoomSelector.clearValue();
        }
    });

    var statusBar = new Ext.ux.StatusBar({
        defaultText: 'EnterGIS - ' + '<a href="http://www.gnuthink.com">Gnuthink Software Cia. Ltda.</a>',
        id: 'right-statusbar',
        statusAlign: 'right', // the magic config
        items: ['Escala:',zoomSelector,'-','Red de Emprendimientos',' ',' ']
    });

    mapPanel = new GeoExt.MapPanel({
        border: true,
        region: 'center',
        map: mymap,
        center: new OpenLayers.LonLat(-79.1, -2.9),
        zoom: 9,
	tbar: toolbarItems,
	bbar: statusBar,
    });
    var LayerNodeUI = Ext.extend(
        GeoExt.tree.LayerNodeUI, new GeoExt.tree.RadioButtonMixin()
    );
    // using OpenLayers.Format.JSON to create a nice formatted string of the
    var treeConfig = new OpenLayers.Format.JSON().write([
	{
	    text: "Google Maps",
            nodeType: "gx_baselayercontainer"}, 
	{
	    text: "Capas",
            nodeType: "gx_overlaylayercontainer",
            expanded: false,
            loader: {
		baseAttrs: {
                    radioGroup: "foo",
                    uiProvider: "use_radio"
		}
            },
	},
    ], true); 

    // create the tree with the configuration from above
    var tree = new Ext.tree.TreePanel({
	id:'tree',
        title: "Capas",
	height:200,
        autoScroll: true,
        loader: new Ext.tree.TreeLoader({
            applyLoader: false,
            uiProviders: {
                "use_radio": LayerNodeUI
            }
        }),
        root: {
            nodeType: "async",
            children: Ext.decode(treeConfig)
        },
        listeners: {
            "radiochange": function(node){
            }
        },
        rootVisible: false,
        lines: true,
	rowHeight:1,
    });

    var treeConfigWin = new Ext.Window({
	autoScroll: true,
        layout: "fit",
        hideBorders: true,
        closeAction: "hide",
        width: 300,
        height: 400,
        title: "Información acerca del Sistema",
        items: [{
            xtype: "form",
            layout: "fit",
            items: [{
                id: "treeconfig",
                xtype: "panel",
		html: {% include "about.html" %}
            }],
            buttons: [{
                text: "Cerrar",
                handler: function() {
                    treeConfigWin.hide();
                }
            }]
        }]
    });

    var treesearch = new Ext.ux.tree.CheckTreePanel({
	autoScroll: true,
	containerScroll: true,
	bubbleCheck: 'none',
	cascadeCheck: 'none',
        root: {
            nodeType: "async",
	    text: 'Filtros',
	    id: 'resource',
//	    autoScroll: true
        },
	tools: [{
	    id: 'refresh',
	    qtip: 'Recargar',
	    handler:function(){
		treesearch.getRootNode().reload();
	    }
	}],
	region: 'center',
	dataUrl:'/entergis/emprendimientos/',
	listeners:{
	    // el nombre del vector debe pasarse desde los datos cargados en el nodo
	    checkchange:function(node, checked){
		var layers = mymap.getLayersBy('isBaseLayer', false);
		if (checked){
		    var item_id = node.attributes.id;
		    var name = node.attributes.text
		    var geojson_layer = new OpenLayers.Format.GeoJSON();
		    var new_vector = new OpenLayers.Layer.Vector(name, {styleMap: layerStyle});
		    var data = node.attributes.data;
		    var feat = geojson_layer.read(data);
		    new_vector.addFeatures(feat);
		    mymap.addLayer(new_vector);
		    layers = selectCtrl.layers;
		    layers.push(new_vector);
		    selectCtrl = new OpenLayers.Control.SelectFeature(layers,
								   {
								       clickout: true,
								       onSelect: select_feature,
								       onUnselect: unselect_feature,
								   });
		    mymap.addControl(selectCtrl);
		    selectCtrl.activate();
		}else{
		    var text = node.attributes.text;
		    var lay2del = mymap.getLayersByName(text);
		    for (var i=0;i<lay2del.length;i++){
			var capa = lay2del[i];
			mymap.removeLayer(capa);
			selectCtrl.destroy();
//			capa.destroy();
		    }
		}
	    }
	},
    });

    var detail2 = new Ext.Panel({
	title:"Emprendimientos",
        autoScroll:true,
	region: 'south',
        collapsible: true,
        border:false,
	split:false,
	items:[treesearch]
    });

    var detail1 = new Ext.Panel({
	title: 'Mapa Politico Cantonal',
        collapsible: true,
        autoScroll:true,
        border:false,
	split:true,
	items:[tree],
	region:'north'
    });

    var detailsPanel = new Ext.Panel({
        region: 'west',
	width: 220,
        title: 'Informacion de Sistema',
        split: true,
	collapsible: true,
        items:[detail1,detail2],
	collapsed: false,
	autoScroll: true,
    });

    mapPanel.region = 'center';

    var viewport = new Ext.Viewport({
        layout: "fit",
	minwidth:600,
        items: {
            layout: "border",
            deferredRender: false,
            items: [mapPanel,detailsPanel]
        },
    });

  setTimeout(function(){
    Ext.get('loading').remove();
    Ext.get('loading-mask').fadeOut({remove:true});
  }, 2000);

});

