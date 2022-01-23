# MUH DEPENDENCIES
#######################################################################
import dash
from dash import dcc, html 
import plotly.graph_objects as go
from csv import reader
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output
import sys

sys.path.append("/Users/danielmathison/twigs/widgets")

from plane_calc import environment as env


class Plane():
	fpath = env.data_fpath
	results_string = env.default_cfg.get("results_string")
	output = {}

	def __init__(self):
		self.app = dash.Dash(__name__, external_stylesheets=env.stylesheets)
		self.graph = dcc.Graph(
    		id="graph",
    		figure=self._render_default(fpath=self.fpath).get("fig"),
    		style=env.styles_layouts.get("graph")
		)
		self._configure_layout()

		@self.app.callback(
			[
				Output("graph", "figure"),
				Output("results", "children")
			],
			[	
				Input("p1", "value"),
				Input("p2", "value"),
				Input("p3", "value")
			]
		)	
		def cb_render(pt1, pt2, pt3):
			update = self.load_data(pt1, pt2, pt3)
			return update.get("fig"), update.get("data")

	# toolbox methods 
	#############################################################################################
	@staticmethod
	def _generate_mesh(xlim, ylim, nn=env.default_cfg.get("mesh_density")):
		# outer product column vec by row vec to get x-grid
		xx = np.outer(np.linspace(xlim[0], xlim[1], nn), np.ones(nn))
		yy = np.outer(np.linspace(ylim[0], ylim[1], nn), np.ones(nn)).T
		return (xx, yy)

	@staticmethod
	def _plot_plane_pt_normal(pt, normal, xlim, ylim, nn=env.default_cfg.get("mesh_density")):
		(xx, yy) = Plane._generate_mesh(xlim, ylim, nn)
		dd = -pt.dot(normal)
		zz = (-normal[0] * xx - normal[1] * yy - dd) * 1. / normal[2]
		return go.Surface(x=list(xx), y=list(yy), z=list(zz), colorscale="Viridis", opacity=0.5, name="Plane")

	@staticmethod
	def _package_points(pt1, pt2, fig=None, trace_details=None):
		# Get vector connecting points
		vec = np.array([pt2[i] - pt1[i] for i in range(env.default_cfg.get("dim"))])

		# pygolf below because why not? Legible version in comments
		######
		######
		######
		###   
		###		dim_vals = []  # bin values by axis [ [x_values], [y_values], [z_values]]
		###		for dim in [0, 1, 2]:  # x, y, z coordinates
		###			dim_vals = append([ pt1[dim] , pt2[dim] ])  # all (x, y, or, z)-values gathered
		###			
		###		# create a dict with the newly formed lists as values and fundamental axes as keys
		###		data_dict = dict(zip(["x", "y", "z"))
		###
		### 	# convert to dataframe
		###		df = DataFrame(data_dict)  
		###
		######
		######
		######

		# Store two points as a dataframe object
		df = pd.DataFrame(dict(zip(["x", "y", "z"], [[pt1[i], pt2[i]] for i in range(env.default_cfg.get("dim"))])))
		raw_params = {
			"x": df.x.values,
			"y": df.y.values,
			"z": df.z.values
		}

		if trace_details:
			raw_params.update(**trace_details)

		# Plot the adjoining vector 
		fig.add_trace(trace=go.Scatter3d(**raw_params))

		return (df, vec)
	#############################################################################################


	# "main" wrapper function for calculations/graphic generation
	#############################################################################################
	def _do_all(self, pt1, pt2, pt3):
		# Create plotly.graphics_objects object
		fig = go.Figure()
			
		(df_vec1, vec1) = Plane._package_points(pt1, pt2, fig=fig, trace_details={"name": "AB"})
		(df_vec2, vec2) = Plane._package_points(pt1, pt3, fig=fig, trace_details={"name": "AC"})

		# Find unit normal vector to plane and add trace
		normal = np.cross(vec1, vec2)

		# Bonus: we can invoke the triple product here and compute
		# the area of the triangle formed on the three input points
		ppid_vol = (normal[0] ** 2) + (normal[1] ** 2) + (normal[2] ** 2)
		tri_area = np.sqrt(ppid_vol) / 2
		terminus = [pt1[i] + normal[i] for i in range(env.default_cfg.get("dim"))]

		(df_norm, vec_norm) = Plane._package_points(
			pt1=pt1, 
			pt2=terminus, 
			fig=fig, 
			trace_details=env.graph_cfg.get("trace_params")
		)
		normal_magnitude = np.sqrt(sum(comp**2 for comp in vec_norm))
		unit_normal = [comp / normal_magnitude for comp in vec_norm]

		# Add the plane to the trace (through pt1, normal found above)
		fig.add_trace(trace=Plane._plot_plane_pt_normal(
				pt=np.array(pt1), 
				normal=normal,
				xlim=env.default_cfg.get("xlim"),
				ylim=env.default_cfg.get("ylim"),
				nn=env.default_cfg.get("axis_density")
			)
		)
		fig.update_layout(**env.styles_layouts.get("go_fig"))

		self.output.update(
			normal=normal,
			unit_normal=unit_normal,
			area=tri_area,
			equation=self._format_equation(normal=normal, pt1=pt1)
		)

		return {
			"fig": fig,
			"data": self._generate_results_string(pt1=pt1, pt2=pt2, pt3=pt3)
		}
	#############################################################################################


	# Consume/load ops (high-level CRUD)
	#############################################################################################
	def load_data(self, pt1, pt2, pt3):
		if pt1 and pt2 and pt3:
			if not isinstance(pt1, list):
				tmp_pt1 = []
				tmp_pt2 = []
				tmp_pt3 = []

				for val in pt1.strip().split(","):
					try:
						val = float(val)
					except ValueError:
						val = float(int(val))
					tmp_pt1.append(val)
				for val in pt2.strip().split(","):
					try:
						val = float(val)
					except ValueError:
						val = float(int(val))
					tmp_pt2.append(val)
				for val in pt3.strip().split(","):
					try:
						val = float(val)
					except ValueError:
						val = float(int(val))
					tmp_pt3.append(val)

				pt1 = tmp_pt1
				pt2 = tmp_pt2
				pt3 = tmp_pt3

			with open(self.fpath, "w") as outfile:
				write_str = ""
				for pt in [pt1, pt2, pt3]:
					write_str += f"{pt[0]}, {pt[1]}, {pt[2]}\n"
					
				outfile.write(write_str.strip())

			return self._do_all(pt1, pt2, pt3)

		return {
			"fig": self.graph.figure, 
			"data": self.results_string
		}

	def _render_default(self, fpath):
		lines = []
		with open(fpath, "r") as infile:
			file_reader = reader(infile)
			for line in file_reader:
				lines.append(line)

		pt1 = [float(val) for val in lines[0]]
		pt2 = [float(val) for val in lines[1]]
		pt3 = [float(val) for val in lines[2]]

		return self._do_all(pt1, pt2, pt3)
	#############################################################################################


	# Parsing / formatting methods
	#############################################################################################
	def _generate_results_string(self, pt1, pt2, pt3):
		input_data = html.P(
			children=[
				f"Results:", html.Br(), html.Br(),
				f"Point A: {pt1}", html.Br(), html.Br(),
				f"Point B: {pt2}", html.Br(), html.Br(),
				f"Point C: {pt3}"
			],
			style=env.styles_layouts.get("results_header")
		)

		results_template = html.P(
			children=[
				f"Area of triangle ABC: ", html.Br(), html.Br(),
				f"Normal vector to ABC's plane: ", html.Br(), html.Br(),
				f"Unit normal vector to ABC's plane: ", html.Br(), html.Br(),
				f"Equation of ABC's plane: "
			],
			style=env.styles_layouts.get("results_fields")
		)

		results_data = html.P(
			children=[
				f"{self.output.get('area'):.2f} sq. units", html.Br(), html.Br(),
				f"<{self.output.get('normal')[0]:.2f}, {self.output.get('normal')[1]:.2f}, {self.output.get('normal')[2]:.2f}>", html.Br(), html.Br(),
				f"<{self.output.get('unit_normal')[0]:.2f}, {self.output.get('unit_normal')[1]:.2f}, {self.output.get('unit_normal')[2]:.2f}>", html.Br(), html.Br(),
				f"{self.output.get('equation')}"
			],
			style=env.styles_layouts.get("results_values")
		)

		data_wrapper = html.Div(
			children=[
				results_template, 
				results_data
			],
			style={
				"text-align": "left", 
				"justifyContent": "center"
			}
		)

		return html.Div(children=[input_data, data_wrapper])

	def _format_equation(self, normal, pt1):
		equation_str = f"{normal[0]:.3f}x "
		
		if normal[1] < 0:
			equation_str += f"- {np.abs(normal[1]):.3f}y "
		else:
			equation_str += f"+ {normal[1]:.3f}y "

		if normal[2] < 0:
			equation_str += f"- {np.abs(normal[2]):.3f}z "
		else:
			equation_str += f"+ {normal[2]:.3f}z "

		dd = -normal.dot(np.array(pt1))
		if dd < 0:
			equation_str += f"- {np.abs(dd):.3f} = 0"
		else: 
			equation_str += f"+ {dd:.3f} = 0"

		return equation_str

	def _configure_layout(self):
		# Site header HTML
		header = html.H2(
			children="Common Plane Calculator",
			style=env.styles_layouts.get("main_header")
		)

		# Site blurb HTML
		about_div = html.Div(
			children=[
				html.P(
					children='''This is normally where you'd write something about what the tool 
						is useful for, but I don't think anyone's going to come wondering 
						or wondering so I'm hoping a good amount of words will fill the space
						sufficiently enough for everyone to gloss right over it. Here's some bold text!
					''',
					style={
						"margin-top": "7px",
						"margin-left": "7px",
						"margin-right": "7px"
					}
				),
				html.P(
					children="Enter three points to get the results.",
					style={
						"margin-top": "40px",
						"font-weight": "bold",
						"text-align": "center",
						"font": {"family": "calibri", "size": 20}
					}
				)
			],
			style=env.styles_layouts.get("about_blurb")
		)

		# Data entry (point 1) HTML
		pt1_div = html.Div(
			children=[	
				html.P(
					children="Point A: ",
					style=env.styles_layouts.get('input_point')
				),
			    dcc.Input(
			    	id="p1", 
			    	type="text", 
			    	placeholder="(x1, y1, z1)", 
			    	debounce=True, 
			    	style=env.styles_layouts.get("input_field")
			    )
			]
		)

		# Data entry (point 2) HTML
		pt2_div = html.Div(
			children=[	
				html.P(
					children="Point B: ",
					style=env.styles_layouts.get("input_point")
				),
			    dcc.Input(
			    	id="p2", 
			    	type="text", 
			    	placeholder="(x2, y2, z2)", 
			    	debounce=True, 
			    	style=env.styles_layouts.get("input_field")
			    )
			]
		)

		# Data entry (point 3) HTML
		pt3_div = html.Div(
			children=[	
				html.P(
					children="Point C: ",
					style=env.styles_layouts.get("input_point")
				),
			    dcc.Input(
			    	id="p3", 
			    	type="text", 
			    	placeholder="(x3, y3, z3)", 
			    	debounce=True, 
			    	style=env.styles_layouts.get("input_field")
			    )
			]
		)

		# Wrap data entry objects
		menu_div = html.Div(children=[pt1_div, pt2_div, pt3_div], style=env.styles_layouts.get("entry_box"))
		row1 = html.Div(children=[about_div, menu_div], style={"margin-bottom": "30px"})

		# Preformat the HTML div that will eventually 
		# hold result data (row 2). This will be populated
		# upon user entry and process execution via callback
		info_panel = html.P(
			id="results",
			children=html.Div(children=[self.results_string]),
			style=env.styles_layouts.get("info_panel")
		)

		# Wrap result skeleton HTML
		row2 = html.Div(children=[info_panel])

		# Wrap graphic output HTML and row 3
		vis_div = html.Div(children=[self.graph], style=env.styles_layouts.get("plot_bin"))
		row3 = html.Div(children=[vis_div])

		# Compile layout HTML and assign to app attribute
		self.app.layout = html.Div(
			children=[
				header, 
				row1, row2, 
				row3
			], 
			style={
				"text-align": "left", 
				"justifyContent": "center"
			}
		)
	#############################################################################################

