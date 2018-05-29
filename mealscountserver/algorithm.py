# from django.shortcuts import render, render_to_response
#
# from bokeh.plotting import figure, output_file, show
# from bokeh.embed import components
#
#
# def index(request):
# 	x= [1,3,5,7,9,11,13]
# 	y= [1,2,3,4,5,6,7]
# 	title = 'y = f(x)'
#
# 	plot = figure(title= title ,
# 				  x_axis_label= 'X-Axis',
# 				  y_axis_label= 'Y-Axis',
# 				  plot_width =400,
# 				  plot_height =400)
#
# 	plot.line(x, y, legend= 'f(x)', line_width = 2)
# 	#Store components
# 	script, div = components(plot)
#
# 	#Feed them to the Django template.
# 	return render_to_response( 'bokeh/index.html',
# 							   {'script' : script , 'div' : div} )

# See mealcountsschool.py for a definition of objects in the mealCountsSchoolsArray
def processSchools(mealCountsSchoolsArray):


	#script, div = components(plots)

	return 1,2 #components(plots)
