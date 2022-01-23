data_fpath = "data.csv"
stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

default_cfg = {
	"result_string": "gonna be some cool html but just me for now",
	"mesh_density": 100,
	"dim": 3,
	"xlim": [-6.5, 6.5],
	"ylim": [-6.5, 6.5],
	"axis_density": 10
}

graph_cfg = {
	"trace_params": {
		"hoverinfo": "all",
		"name": "Normal",
		"opacity": 0.8
	}
}

styles_layouts = {
	"go_fig": {
		"title": "IM TITLE, WHY AM I SO TINY", 
		"titlefont": {"family": "arial", "size": 8.0},
		"autosize": False,
		"scene_camera_eye": dict(x=1.87, y=0.88, z=+0.64),
        "width": 760, 
        "height": 760,
        "showlegend": False,
        "xaxis": {"showline": True, "zeroline": True},
        "yaxis": {"showline": True, "zeroline": True}
	},
	"results_header": {
		"font": {"family": "arial", "size": 10},
		"margin-top": "15px",
		"margin-bottom": "15px",
		"float": "left",
		"width": "250px",
		"margin-left": "25px"
	},
	"results_fields": {
		"font": {"family": "arial", "size": 10},
		"margin-top": "12px",
		"margin-bottom": "12px",
		"margin-right": "10px",
		"float": "left",
		"width": "235px",
		"font-style": "italic",
		"text-align": "right",
		"background-color": "#ffb7c5",
		"border-width": "5px",
		"border-color": "#de3163",
		"border-style": "inset"
	},
	"results_values": {
		"font": {"family": "arial", "size": 8},
		"margin-top": "12px",
		"margin-bottom": "12px",
		"float": "left",
		"text-align": "center",
		"width": "320px",
		"font-weight": "bold",
		"background-color": "#ffb7c5",
		"border-width": "5px",
		"border-color": "#de3163",
		"border-style": "inset"
	},
	"graph": {
    	"margin-top": "50px",
    	"margin-bottom": "50px",
    	"margin-left": "50px",
    	"margin-right": "50px"
    },
    "main_header": {
		"margin-bottom": "30px", 
		"text-align": "center", 
		"width": "860px",
		"justifyContent": "center", 
		"background-color": "#8ebf42",
		"border-width": "5px",
		"border-color": "#fff600",
		"border-style": "inset"
	},
	"about_blurb": {
		"float": "left",
		"width": "560px",
		"height": "250px",
		"background-color": "#8ebf42",
		"border-width": "5px",
		"border-style": "inset",
		"border-color": "#fff600",
		"right-margin": "10px"
	},
	"input_point": {
	 	"text-align": "center",
	 	"float": "left",
	 	"width": "90px",
	 	"margin-bottom": "22px",
		"margin-top": "22px"
	},
	"input_field": {
		"width": "150px",
		"text-align": "center",
		"background-color": "#f1f1f1",
		"float": "left",
		"margin-bottom": "22px",
		"margin-top": "22px"
	},
	"entry_box": {
		"margin-bottom": "10px", 
		"text-align":" center", 
		"width": "290px",
		"height": "250px",
		"float": "left",
		"background-color": "#8ebf42",
		"border-width": "5px",
		"border-style": "inset",
		"border-color": "#fff600"
	},
	"info_panel": {
		"width": "860px",
		"height": "200px",
		"float": "left",
		"background-color": "#8ebf42",
		"border-width": "5px",
		"border-style": "inset",
		"border-color": "#fff600"
	},
	"plot_bin": {
		"width": "860px",
		"height": "860px",
		"float": "left",
		"background-color": "#8ebf42",
		"border-width": "5px",
		"border-style": "inset",
		"border-color": "#fff600"
	}


}