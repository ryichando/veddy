#
# Author: Ryoichi Ando (https://ryichando.graphics)
# License: CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/)
#
import os, subprocess, argparse, fnmatch, sys, pathlib, utility, re, signal
import xml.etree.ElementTree as ET
#
# Global variables
g_arguments = {}
g_info = {}
g_materials = []
g_functions = []
g_streams = []
g_audiotracks = {}
g_configurations = {}
g_label_counter = {}
g_exports = {}
g_current_xml_path = []
g_all_tags = [
	'filter','reference','composite','input', 'enable','filter_input',
	'all_inputs','pipe','for_each','group','rolling','print',
	'set','variable','default', 'if', 'clear','exit','convert_to_inputs',
	'assert_inputs_match', 'interpret','assert','reset',
]
#
def infer_info():
	#
	shape = None
	fps = None
	#
	if 's' in g_configurations:
		shape = tuple([ int(x) for x in g_configurations['s'].split('x')])
	#
	for material in g_materials:
		if material.counter:
			if not shape:
				shape = material.shape
			if not fps:
				fps = material.fps
	if not shape:
		shape = (480,360)
	if not fps:
		fps = 30
	return {
		'shape' : shape,
		'fps' : fps,
	}
#
def replace_arguments( value, arguments ):
	#
	arguments = arguments | g_info
	for x,y in g_arguments.items():
		arguments[x] = y
	#
	default_globals = {
		'_bgcolor_' : 'black',
		'_fgcolor_' : 'white',
	}
	for x,y in default_globals.items():
		if not x in arguments:
			arguments[x] = y
	#
	escape_dict = {
		'#gte' : '>=',
		'#gt' : '>',
	}
	for x,y in escape_dict.items():
		value = value.replace(x,y)
	#
	for x,y in arguments.items():
		value = re.sub(f'(\${x})([^a-zA-Z0-9])',f'{y}\\2',value)
		if value.endswith('$'+x):
			value = value.removesuffix('$'+x)+y
		value = value.replace('${'+x+'}',y)
	#
	if '$' in value:
		print( f'argument substitution faild: {value}' )
		sys.exit()
	#
	return value
#
# ffmpeg filter generator
def ffmpeg_filter( video_inputs, video_outputs, filter_name, variables, enable_expr ):
	#
	cmd = ''.join([f'[{v}]' for v in video_inputs])
	cmd += filter_name
	#
	variable_pairs = []
	if variables:
		variable_pairs.extend([f'{key}={value}' if key else value for key,value in variables.items()])
	if enable_expr:
		variable_pairs.append(f"enable='{enable_expr}'")
	cmd += '=' + ':'.join(variable_pairs)
	#
	cmd += ''.join([f'[{v}]' for v in video_outputs])
	return cmd
#
def all_the_same( name, infos ):
	if infos:
		return all(x[name] == infos[0][name] for x in infos)
	else:
		return True
#
def pick_first_image( path ):
	if not os.path.exists(path):
		path_obj = pathlib.Path(path)
		if os.path.exists(path_obj.parent):
			for file in os.listdir(path_obj.parent):
				name = path_obj.name
				hit = re.search('%.*d',name)
				if hit:
					name = name.replace(hit[0],'')
				hit = re.search('\d+',file)
				if hit:
					mod_file = file.replace(hit[0],'')
				else:
					mod_file = file
				if name in mod_file:
					return str(path_obj.parent) + '/' + file
		print( f'Could not find any file matches "{path}"' )
		sys.exit()
	else:
		return path
#
def evaluate( value, arguments, func_table ):
	if value:
		value = replace_arguments(value.replace(',','\,'),arguments)
		for field in match_eval(value):
			evaluated = eval(match_eval(field,True)[0],arguments|func_table)
			value = value.replace(field,str(evaluated))
		return value
	else:
		return value
#
# Generate a unique label
def generate_label( name='v' ):
	if name in g_label_counter:
		g_label_counter[name] += 1
	else:
		g_label_counter[name] = 0
	return name+'-'+str(g_label_counter[name])
#
# Find an instance of reference from a name
def find_reference( name, type=[] ):
	if 'stream' in type:
		for stream in g_streams:
			if stream.name == name:
				return stream
	if 'material' in type:
		for material in g_materials:
			if material.name == name:
				return material
	if 'function' in type:
		for function in g_functions:
			if function.name == name:
				return function
	#
	print( f'Reference "{name}" was not found.')
	sys.exit()
#
# Match eval(...)
def match_eval( text, only_inside=False ):
	result = []
	while True:
		eval_str = 'eval('
		start = text.find(eval_str)
		if start >= 0:
			i = start+len(eval_str)
			bracket_counter = 1
			while i <= len(text):
				if text[i] == '(':
					bracket_counter += 1
				elif text[i] == ')':
					bracket_counter -= 1
				if bracket_counter == 0:
					if only_inside:
						result.append(text[start+len(eval_str):i])
					else:
						result.append(text[start:i+1])
					text = text[i+1:]
					break
				i += 1
		else:
			break
	return result
#
def generate_function_table( input_infos=[], filtered_infos=[] ):
	#
	def get_filtered_count():
		return len(filtered_infos)
	#
	def get_filtered_duration( index=0 ):
		return filtered_infos[index]['duration']
	#
	def get_filtered_durations():
		return [ x['duration'] for x in filtered_infos ]
	#
	def get_input_count():
		return len(input_infos)
	#
	def get_input_duration( index=0 ):
		return input_infos[index]['duration']
	#
	def get_input_durations():
		return [ x['duration'] for x in input_infos ]
	#
	def get_filtered_width(index=0):
		return filtered_infos[index]['shape'][0]
	#
	def get_filtered_height(index=0):
		return filtered_infos[index]['shape'][1]
	#
	def get_filtered_fps(index=0):
		return filtered_infos[index]['fps']
	#
	def get_filtered_widths():
		return [x['shape'][0] for x in filtered_infos]
	#
	def get_filtered_heights():
		return [x['shape'][1] for x in filtered_infos]
	#
	def get_filtered_fpses():
		return [x['fps'] for x in filtered_infos]
	#
	def get_input_width(index=0):
		return input_infos[index]['shape'][0]
	#
	def get_input_height(index=0):
		return input_infos[index]['shape'][1]
	#
	def get_input_fps(index=0):
		return input_infos[index]['fps']
	#
	def get_input_widths():
		return [x['shape'][0] for x in input_infos]
	#
	def get_input_heights():
		return [x['shape'][1] for x in input_infos]
	#
	def get_input_fpses():
		return [x['fps'] for x in input_infos]
	#
	def get_material_width( index ):
		return g_materials[index].shape[0]
	#
	def get_material_height( index ):
		return g_materials[index].shape[1]
	#
	def get_material_duration( index ):
		return g_materials[index].duration
	#
	def get_material_fps( index ):
		return g_materials[index].fps
	#
	def get_material_name( index ):
		return g_materials[index].name
	#
	def convert_path( relpath ):
		converted_path = relpath
		if relpath:
			if relpath.startswith('/'):
				converted_path = os.path.join(os.path.dirname(g_current_xml_path[0]),relpath[1:])
			else:
				converted_path = os.path.join(os.path.dirname(g_current_xml_path[-1]),relpath)
		return converted_path
	#
	return {
		'count' : get_filtered_count,
		'width' : get_filtered_width,
		'height' : get_filtered_height,
		'fps' : get_filtered_fps,
		'duration' : get_filtered_duration,
		'widths' : get_filtered_widths,
		'heights' : get_filtered_heights,
		'fpses' : get_filtered_fpses,
		'durations' : get_filtered_durations,
		'input_count' : get_input_count,
		'input_width' : get_input_width,
		'input_height' : get_input_height,
		'input_fps' : get_input_fps,
		'input_duration' : get_input_duration,
		'input_widths' : get_input_widths,
		'input_heights' : get_input_heights,
		'input_fpses' : get_input_fpses,
		'input_durations' : get_input_durations,
		'material_width' : get_material_width,
		'material_height' : get_material_height,
		'material_duration' : get_material_duration,
		'material_fps' : get_material_fps,
		'material_name' : get_material_name,
		'convert_path' : convert_path,
	}
#
# Generate ffmpeg filter command
def generate( root, arguments, inputs, input_infos, inherit_outputs=[], inherit_infos=[], sequential=False, inherit_arguments=False ):
	#
	arguments = arguments if inherit_arguments else arguments.copy()
	outputs = inherit_outputs.copy()
	infos = inherit_infos.copy()
	filtered_infos = []
	commands = []
	name = root.attrib['name'] if 'name' in root.attrib else 'root'
	#
	for elm in root:
		#
		if infos:
			latest_info = infos[-1]
		else:
			latest_info = infer_info()
		#
		g_info['_width_'] = str(latest_info['shape'][0])
		g_info['_height_'] = str(latest_info['shape'][1])
		g_info['_fps_'] = str(latest_info['fps'])
		#
		def func_table():
			return generate_function_table(input_infos,filtered_infos)
		#
		if not elm.tag in g_all_tags:
			print( f'Unknown tag found "{elm.tag}"')
			sys.exit()
		#
		if elm.tag == 'assert_inputs_match':
			name = elm.attrib['name']
			root_name = root.attrib['name'] if 'name' in root.attrib else ''
			if not all_the_same(name,input_infos):
				print( f'{root.tag}({root_name}): incoming {name} are not the same' )
				print( [ x[name] for x in input_infos ] )
				sys.exit()
		#
		if elm.tag == 'set':
			key = elm.attrib['name']
			val = evaluate(elm.attrib['value'],arguments,func_table())
			if val:
				arguments[key] = val
			elif key in arguments:
				del arguments[key]
		#
		if elm.tag == 'clear':
			if 'name' in elm.attrib:
				name = elm.attrib['name']
				if name in arguments:
					del arguments[name]
			else:
				arguments.clear()
		#
		if elm.tag == 'filter':
			#
			(filtered_cmd,filtered_outputs,filtered_infos) = generate(elm,arguments,inputs,input_infos)
			if filtered_cmd:
				commands.extend(filtered_cmd)
			#
			if sequential:
				filtered_outputs = outputs + filtered_outputs
				filtered_infos = infos + filtered_infos
			#
			variables = {}
			interpret_variables = {}
			for entry in elm:
				if entry.tag == 'variable':
					name = entry.attrib['name'] if 'name' in entry.attrib else ''
					if name == 'enable':
						print( 'enable should be specified through "enable" tag.' )
						sys.exit()
					value = evaluate(entry.attrib['value'],arguments,func_table())
					if value:
						variables[name] = value
			#
			for entry in elm:
				if entry.tag == 'interpret':
					names = entry.attrib['name'].split(',') if 'name' in entry.attrib else []
					value = evaluate(entry.attrib['value'],arguments,func_table())
					for name in names:
						interpret_variables[name] = value
			#
			enable_expr = None
			for entry in elm:
				if entry.tag == 'enable':
					enable_expr = evaluate(entry.attrib['expression'],arguments,func_table())
			#
			def interpret(text):
				for key,value in interpret_variables.items():
					text = text.replace(key,value)
				return text
			#
			output_count = int(evaluate(elm.attrib['output_count'],arguments,func_table())) if 'output_count' in elm.attrib else 1
			output_labels = []
			output_infos = []
			new_info = {}
			#
			# Set duration
			duration_mode = interpret(evaluate(elm.attrib['duration'],arguments,func_table())) if 'duration' in elm.attrib else 'shortest'
			#
			filtered_durations = [ x['duration'] for x in filtered_infos ]
			if duration_mode == 'shortest':
				new_info['duration'] = min(filtered_durations)
			elif duration_mode == 'longest':
				new_info['duration'] = max(filtered_durations)
			elif duration_mode == 'sum':
				new_info['duration'] = sum(filtered_durations)
			elif duration_mode == 'inf' or duration_mode == '':
				new_info['duration'] = float('inf')
			elif match_eval(duration_mode):
				new_info['duration'] = float(evaluate(duration_mode,arguments,func_table()))
			else:
				try:
					new_info['duration'] = float(duration_mode)
				except:
					print( f'Unsupported mode {duration_mode}')
					sys.exit(-1)
			#
			# Set shape
			if 'shape' in elm.attrib:
				shape_mode = interpret(evaluate(elm.attrib['shape'],arguments,func_table()))
				if shape_mode == 'first':
					new_info['shape'] = filtered_infos[0]['shape']
				else:
					new_info['shape'] = tuple([ int(x) for x in shape_mode.split('x') ])
			elif 'width' in elm.attrib or 'height' in elm.attrib:
				width = int(eval(interpret(evaluate(elm.attrib['width'],arguments,func_table())))) if 'width' in elm.attrib else filtered_infos[0]['shape'][0]
				height = int(eval(interpret(evaluate(elm.attrib['height'],arguments,func_table())))) if 'height' in elm.attrib else filtered_infos[0]['shape'][1]
				new_info['shape'] = (width,height)
			else:
				new_info['shape'] = filtered_infos[0]['shape']
			#
			# Set fps
			fps_mode = eval(interpret(evaluate(elm.attrib['fps'],arguments,func_table()))) if 'fps' in elm.attrib else 'first'
			if fps_mode == 'first':
				new_info['fps'] = filtered_infos[0]['fps']
			else:
				new_info['fps'] = float(fps_mode)
			#
			while output_count > 0:
				output_labels.append(generate_label(elm.attrib['name']))
				output_infos.append(new_info)
				output_count -= 1
			#
			commands.append(ffmpeg_filter(filtered_outputs,output_labels,elm.attrib['name'],variables,enable_expr))
			#
			if sequential:
				outputs = output_labels
				infos = output_infos
			else:
				outputs.extend(output_labels)
				infos.extend(output_infos)
		#
		if elm.tag == 'composite':
			#
			(filtered_cmd,filtered_outputs,filtered_infos) = generate(elm,arguments,inputs,input_infos)
			if filtered_cmd:
				commands.extend(filtered_cmd)
			if sequential:
				filtered_outputs = outputs + filtered_outputs
				filtered_infos = infos + filtered_infos
			#
			ref_name = elm.attrib['name']
			new_arguments = {}
			for tag in elm.attrib:
				if not tag == 'name':
					new_arguments[tag] = evaluate(elm.attrib[tag],arguments|new_arguments,func_table())
			#
			(filtered_cmd,filtered_outputs,filtered_infos) = find_reference(ref_name,['function']).generate(new_arguments,filtered_outputs,filtered_infos)
			if filtered_cmd:
				commands.extend(filtered_cmd)
			#
			if sequential:
				outputs = filtered_outputs
				infos = filtered_infos
			else:
				outputs.extend(filtered_outputs)
				infos.extend(filtered_infos)
		#
		if elm.tag == 'pipe':
			(filtered_cmd,filtered_outputs,filtered_infos) = generate(elm,arguments,inputs,input_infos,sequential=True)
			if filtered_cmd:
				commands.extend(filtered_cmd)
			if sequential:
				filtered_outputs = outputs + filtered_outputs
				filtered_infos = infos + filtered_infos
			#
			if sequential:
				outputs = filtered_outputs
				infos = filtered_infos
			else:
				outputs.extend(filtered_outputs)
				infos.extend(filtered_infos)
		#
		if elm.tag == 'reference':
			ref_name = elm.attrib['name']
			(filtered_cmd,filtered_outputs,filtered_infos) = find_reference(ref_name,['material','stream']).generate({},inputs,input_infos)
			if filtered_cmd:
				commands.extend(filtered_cmd)
			if sequential:
				filtered_outputs = outputs + filtered_outputs
				filtered_infos = infos + filtered_infos
			#
			if sequential:
				outputs = filtered_outputs
				infos = filtered_infos
			else:
				outputs.extend(filtered_outputs)
				infos.extend(filtered_infos)
		#
		if elm.tag == 'filter_input':
			idx = int(elm.attrib['index']) if 'index' in elm.attrib else 0
			(filtered_cmd,filtered_outputs,filtered_infos) = generate(elm,arguments,[inputs[idx]],[input_infos[idx]])
			if filtered_cmd:
				commands.extend(filtered_cmd)
			assert( len(filtered_outputs) == 1 )
			inputs[idx] = filtered_outputs[0]
			input_infos[idx] = filtered_infos[0]
		#
		if elm.tag == 'input':
			idx = int(elm.attrib['index']) if 'index' in elm.attrib else 0
			if sequential:
				outputs = [inputs[idx]]
				infos = [input_infos[idx]]
			else:
				outputs.append(inputs[idx])
				infos.append(input_infos[idx])
		#
		if elm.tag == 'all_inputs':
			if sequential:
				outputs = inputs
				infos = input_infos
			else:
				outputs.extend(inputs)
				infos.extend(input_infos)
		#
		if elm.tag == 'group':
			(filtered_cmd,filtered_outputs,filtered_infos) = generate(elm,arguments,inputs,input_infos)
			if filtered_cmd:
				commands.extend(filtered_cmd)
			outputs.extend(filtered_outputs)
			infos.extend(filtered_infos)
		#
		if elm.tag == 'for_each':
			#
			if not sequential:
				print( 'for_each is only allowed within pipe' )
				sys.exit()
			#
			new_outputs = []
			new_infos = []
			#
			enum_name = None
			if 'enumerate' in elm.attrib:
				enum_name = elm.attrib['enumerate']
			#
			for i,(output,info) in enumerate(zip(outputs,infos)):
				new_arguments = arguments.copy()
				if enum_name:
					new_arguments[enum_name] = str(i)
				(filtered_cmd,filtered_outputs,filtered_infos) = generate(elm,new_arguments,inputs,input_infos,inherit_outputs=[output],inherit_infos=[info],sequential=True)
				if filtered_cmd:
					commands.extend(filtered_cmd)
				new_outputs.extend(filtered_outputs)
				new_infos.extend(filtered_infos)
			#
			outputs = new_outputs
			infos = new_infos
		#
		if elm.tag == 'rolling':
			#
			if not sequential:
				print( 'rolling is only allowed within pipe' )
				sys.exit()
			#
			first_output = outputs[0]
			first_info = infos[0]
			#
			enum_name = None
			if 'enumerate' in elm.attrib:
				enum_name = elm.attrib['enumerate']
			#
			for i,(second_output,second_info) in enumerate(zip(outputs[1:],infos[1:])):
				new_arguments = arguments.copy()
				if enum_name:
					new_arguments[enum_name] = str(i)
				(filtered_cmd,filtered_outputs,filtered_infos) = generate(elm,new_arguments,inputs,input_infos,inherit_outputs=[first_output,second_output],inherit_infos=[first_info,second_info],sequential=True)
				if filtered_cmd:
					commands.extend(filtered_cmd)
				assert( len(filtered_outputs) == 1 )
				assert( len(filtered_infos) == 1 )
				first_output = filtered_outputs[0]
				first_info = filtered_infos[0]
			#
			outputs = [first_output]
			infos = [first_info]
		#
		if elm.tag == 'assert':
			value = evaluate(elm.attrib['value'],arguments,func_table())
			if not value == 'True':
				message = evaluate(elm.attrib['name'],arguments,func_table())
				print( f'[{root.tag}]: assertion faild; name = "{message}"' )
				sys.exit()
		#
		if elm.tag == 'if':
			#
			variables = []
			for entry in elm:
				if entry.tag == 'variable':
					variables.append(evaluate(entry.attrib['value'],arguments,func_table()))
			#
			def proceed(entry):
				if sequential:
					(filtered_cmd,filtered_outputs,filtered_infos) = generate(entry,arguments,inputs,input_infos,inherit_outputs=outputs,inherit_infos=infos,sequential=True,inherit_arguments=True)
				else:
					(filtered_cmd,filtered_outputs,filtered_infos) = generate(entry,arguments,inputs,input_infos,inherit_arguments=True)
				if filtered_cmd:
					commands.extend(filtered_cmd)
				if sequential:
					outputs.clear()
					infos.clear()
				outputs.extend(filtered_outputs)
				infos.extend(filtered_infos)
			#
			condtype = elm.attrib['name']
			if condtype == 'equal':
				assert( len(variables) == 2 )
				is_equal = str(variables[0]) == str(variables[1])
				try:
					float(variables[0]) == float(variables[1])
				except:
					pass
				for entry in elm:
					if is_equal and entry.tag == 'then':
						proceed(entry)
					elif not is_equal and entry.tag == 'else':
						proceed(entry)
			elif condtype == 'set':
				assert( len(variables) == 1 )
				is_set = variables[0] in arguments and not arguments[variables[0]] == ''
				for entry in elm:
					if is_set and entry.tag == 'then':
						proceed(entry)
					elif not is_set and entry.tag == 'else':
						proceed(entry)
			elif condtype == 'switch':
				assert( len(variables) == 1 )
				var = variables[0]
				for entry in elm:
					if entry.tag == 'case' and entry.attrib['value'] == var:
						proceed(entry)
						break
					elif entry.tag == 'otherwise':
						proceed(entry)
						break
		#
		if elm.tag == 'print':
			#
			if sequential:
				(filtered_cmd,filtered_outputs,filtered_infos) = generate(elm,arguments,inputs,input_infos,inherit_outputs=outputs,inherit_infos=infos,sequential=True)
			else:
				(filtered_cmd,filtered_outputs,filtered_infos) = generate(elm,arguments,inputs,input_infos)
			#
			verbose = int(elm.attrib["verbose"]) if "verbose" in elm.attrib else 0
			name = elm.attrib["name"] if "name" in elm.attrib else root.tag
			value = evaluate(elm.attrib['value'],arguments,func_table()) if "value" in elm.attrib else None
			#
			if filtered_cmd:
				commands.extend(filtered_cmd)
			#
			if sequential:
				outputs = filtered_outputs
				infos = filtered_infos
			else:
				outputs.extend(filtered_outputs)
				infos.extend(filtered_infos)
			#
			def get_numeric_valued_dict(d):
				d = d.copy()
				for key,value in d.items():
					try:
						d[key] = int(value)
						d[key] = float(value)
					except:
						pass
				return d
			#
			def my_str_arrays(d):
				if len(d) == 1:
					return str(d)
				else:
					return '[\n   ' + '\n   '.join([ str(x) for x in d ]) + '\n]'
			#
			if value:
				print( f'{name}: {value}' )
			else:
				print( f'>>> {name}' )
				if verbose > 0:
					print( f'arguments (_global_) = {get_numeric_valued_dict(g_info)}' )
				print( f'arguments (global) = {get_numeric_valued_dict(g_arguments)}' )
				print( f'arguments (local) = {get_numeric_valued_dict(arguments)}' )
				if inputs:
					if verbose > 0:
						print( f'inputs = {inputs}' )
					print( f'input_infos = {my_str_arrays(input_infos)}' )
				if verbose > 0:
					print( f'outputs = {filtered_outputs}' )
				print( f'infos = {my_str_arrays(filtered_infos)}' )
				print( '<<<' )
		#
		if elm.tag == 'exit':
			raise ValueError('<exit> tag hit')
		#
		if elm.tag == 'convert_to_inputs':
			inputs = outputs.copy()
			input_infos = infos.copy()
			outputs.clear()
			infos.clear()
		#
		if elm.tag == 'reset':
			arguments.clear()
	#
	return commands,outputs,infos
#
# Material class
class Material:
	#
	def __init__( self, root, dirpath ):
		self.fps = int(evaluate(root.attrib['fps'],g_arguments,generate_function_table())) if 'fps' in root.attrib else 60
		self.shape = (0,0)
		self.should_trim = False
		self.duration = float('inf')
		self.name = root.attrib['name']
		self.path = None
		if 'path' in root.attrib:
			self.path = evaluate(root.attrib['path'],g_arguments,generate_function_table())
		elif 'url' in root.attrib:
			url = root.attrib['url']
			username = root.attrib['username'] if 'username' in root.attrib else ''
			password = root.attrib['password'] if 'password' in root.attrib else ''
			self.path = utility.download(url,dirpath,username,password)
			if not self.path:
				print( f'Downloadong {url} faild.' )
				sys.exit()
		#
		if self.path and not self.path[0] == '/':
			self.path = dirpath + '/' + self.path
		#
		self.is_image = False
		self.is_video = False
		if self.path:
			if self.path.endswith(utility.get_image_extensions()):
				self.is_image = True
			if self.path.endswith(utility.get_video_extensions()):
				self.is_video = True
			if self.is_image:
				self.shape = utility.get_image_resolution(pick_first_image(self.path))
				count = utility.get_frame_count(self.path)
				if count == 1:
					if 'duration' in root.attrib:
						self.duration = float(evaluate(root.attrib['duration'],g_arguments,generate_function_table()))
						self.should_trim = True
					else:
						self.duration = float('inf')
				else:
					self.duration = count / self.fps
			elif self.is_video:
				self.fps = utility.get_video_fps(self.path)
				self.shape = utility.get_video_resolution(self.path)
				self.duration = utility.get_video_duration(self.path)
		self.reset()
	#
	def reset(self):
		self.counter = 0
		self.used_counter = 0
		self.source_labels = []
		self.generated = False
	#
	def recursively_increment_counter(self):
		self.source_labels.append(generate_label(self.name))
		self.counter += 1
	#
	def generate( self, arguments, inputs, input_infos ):
		#
		info = {
			'duration' : self.duration,
			'shape' : self.shape,
			'fps' : self.fps,
		}
		if self.counter == 1:
			if self.should_trim:
				new_label = generate_label('img-trim')
				cmd = f'[{self.input_index}]trim=start=0:end={self.duration},fps={self.fps}[{new_label}]'
				self.input_index = new_label
				return ([cmd],[new_label],[info])
			else:
				new_label = generate_label('img-fps')
				cmd = f'[{self.input_index}]fps={self.fps}[{new_label}]'
				self.input_index = new_label
				return ([cmd],[new_label],[info])
		else:
			if not self.generated:
				cmd = [f'[{self.input_index}]split={len(self.source_labels)}'+''.join([f'[{label}]' for label in self.source_labels])]
				self.generated = True
			else:
				cmd = ''
			#
			self.used_counter += 1
			assert( self.used_counter <= self.counter )
			return (cmd,[self.source_labels[self.used_counter-1]],[info])
	#
	def generate_input_cmd( self, input_index ):
		if self.counter:
			self.input_index = input_index
			if '%' in self.path:
				return f'-r {self.fps} -i {self.path}'
			else:
				if self.path.endswith(utility.get_image_extensions()):
					return f'-loop 1 -i {self.path}'
				if self.path.endswith(utility.get_video_extensions()):
					return f'-i {self.path}'
		else:
			return ''
#
# AudioTrack class
class AudioTrack:
	#
	def __init__( self, root, dirpath ):
		self.name = root.attrib['name'] if 'name' in root.attrib else None
		self.audios = []
		self.volume = float(root.attrib['volume']) if 'volume' in root.attrib else 1.0
		for elm in root:
			if elm.tag == 'insert':
				time = float(elm.attrib['at'])
				audio = []
				for entry in elm:
					if entry.tag == 'audio':
						path = entry.attrib['path']
						if not path[0] == '/':
							path = dirpath + '/' + path
						if not os.path.exists(path):
							print( f'File {path} does not exist.')
							sys.exit()
						audio.append({'path':path})
				if audio:
					self.audios.append((time,audio))
	#
	def generate_input_cmd( self, input_index ):
		cmd = []
		for time,audio in self.audios:
			for a in audio:
				a['input_index'] = input_index
				cmd.append(f'-i {a["path"]}')
				input_index += 1
		return cmd
	#
	def generate( self, video_duration ):
		#
		silence_label = generate_label('silence')
		all_labels = []
		cmd = [f'anullsrc[{silence_label}]']
		for time,audio in self.audios:
			if len(audio) == 1:
				new_label = generate_label('audio')
				all_labels.append(new_label)
				cmd.append(f'[{audio[0]["input_index"]}]adelay={int(1000*time)}:all=1[{new_label}]')
			else:
				new_label = generate_label('audio')
				all_labels.append(new_label)
				cmd.append(''.join([f'[{a["input_index"]}]' for a in audio])+f'concat=n={len(audio)}:v=0:a=1,adelay={int(1000*time)}:all=1[{new_label}]')
		#
		output = generate_label('audio-output')
		nums = len(all_labels)+1
		if nums > 1:
			cmd.append( f'[{silence_label}]'+''.join([f'[{tag}]' for tag in all_labels])+f'amix=inputs={nums}:duration=first:dropout_transition=0.1,volume={2*self.volume},atrim=end={video_duration}[{output}]' )
			return cmd,output
		else:
			return [],''
#
# Function class
class Function:
	#
	def __init__( self, root ):
		self.root = root
		self.name = root.attrib['name']
	#
	def generate( self, arguments, inputs, input_infos ):
		#
		arguments = arguments.copy()
		func_table = generate_function_table(input_infos,[])
		#
		for elm in self.root.findall('default'):
			name = elm.attrib['name']
			if not name in arguments:
				if 'required' in elm.attrib:
					print( f'function "{self.name}": "{name}" must be defined.' )
					sys.exit()
				arguments[name] = evaluate(elm.attrib['value'],arguments,func_table)
		#
		return generate(self.root,arguments,inputs,input_infos)
#
# Stream class
class Stream:
	#
	def __init__( self, root, dirpath, default_name ):
		self.root = root
		self.name = root.attrib['name'] if 'name' in root.attrib else default_name
		if 'name' in root.attrib:
			self.main_stream = 0
		else:
			self.main_stream = 1
		self.dirpath = dirpath
		self.references = [elm.attrib['name'] for elm in root.findall('.//reference')]
		self.transition = root.attrib['transition'] if 'transition' in root.attrib else ''
		self.reset()
	#
	def reset(self):
		self.counter = 0
		self.used_counter = 0
		self.source_labels = []
		self.generated = False
	#
	def recursively_increment_counter(self):
		self.source_labels.append(generate_label(self.name))
		self.counter += 1
		if self.counter == 1:
			for name in self.references:
				find_reference(name,['stream','material']).recursively_increment_counter()
	#
	def join_cmd( self, cmd, outputs, infos ):
		#
		if len(outputs) > 1:
			#
			assert( all_the_same('fps',infos) )
			assert( all_the_same('shape',infos) )
			#
			# concatenate using concat filter
			new_label = generate_label(self.name)
			concat_cmd = ffmpeg_filter(outputs,[new_label],'concat',{'n':len(outputs)},None)
			return (cmd+[concat_cmd],[new_label],[{
				'duration' : sum([x['duration'] for x in infos]),
				'shape' : infos[0]['shape'],
				'fps' : infos[0]['fps'],
			}])
		else:
			return (cmd,outputs,infos)
	#
	def internal_generate( self, arguments, inputs, input_infos ):
		#
		if self.transition:
			(cmd,filtered_outputs,filtered_infos) = generate(self.root,arguments,inputs,input_infos)
			new_arguments = arguments.copy()
			new_arguments['type'] = self.transition
			extended = True
			for tag in self.root.attrib:
				if not tag == 'name' and not tag == 'transition':
					new_arguments[tag] = self.root.attrib[tag]
				if tag == 'extended':
					extended = True if self.root.attrib[tag] == '1' else False
			if filtered_outputs:
				first_output = filtered_outputs[0]
				first_info = filtered_infos[0]
				for second_output,second_info in zip(filtered_outputs[1:],filtered_infos[1:]):
					(_cmd,_outputs,_infos) = find_reference('extended_transition' if extended else 'transition',['function']).generate(new_arguments,[first_output,second_output],[first_info,second_info])
					cmd.extend(_cmd)
					assert( len(_outputs) == 1 )
					assert( len(_infos) == 1 )
					first_output = _outputs[0]
					first_info = _infos[0]
			outputs = [first_output]
			infos = [first_info]
			return (cmd,outputs,infos)
		else:
			return generate(self.root,arguments,inputs,input_infos)
	#
	def generate( self, arguments={}, inputs=[], input_infos=[] ):
		#
		if self.counter == 1:
			(cmd,outputs,infos) = self.internal_generate(arguments,inputs,input_infos)
			return self.join_cmd(cmd,outputs,infos)
		else:
			#
			if not self.generated:
				(cmd,outputs,infos) = self.internal_generate(arguments,inputs,input_infos)
				(cmd,outputs,infos) = self.join_cmd(cmd,outputs,infos)
				assert( len(outputs) == 1 )
				cmd.append(f'[{outputs[0]}]split={len(self.source_labels)}'+''.join([f'[{label}]' for label in self.source_labels]))
				self.generated = True
				self.save_infos = infos
			else:
				cmd = ''
			#
			self.used_counter += 1
			assert( self.used_counter <= self.counter )
			return (cmd,[self.source_labels[self.used_counter-1]],self.save_infos)
#
def reset():
	g_label_counter.clear()
	g_info.clear()
	for material in g_materials:
		material.reset()
	for stream in g_streams:
		stream.reset()
#
def parse_xml( path ):
	#
	# Start parsing
	g_current_xml_path.append(os.path.dirname(path))
	root = ET.parse(path).getroot()
	filename_base = os.path.basename(path).split('.')[0]
	#
	# Check the version
	assert( root.attrib['version'] == '0.0.1' )
	for elm in root:
		#
		# Load set
		if elm.tag == 'global':
			g_arguments[elm.attrib['name']] = evaluate(elm.attrib['value'],{},None)
		#
		# Import external file
		if elm.tag == 'import':
			parse_xml(os.path.dirname(path)+'/'+elm.attrib['path'])
		#
		# Load function
		if elm.tag == 'function':
			g_functions.append(Function(elm))
		#
		# Load material
		if elm.tag == 'material':
			g_materials.append(Material(elm,os.path.dirname(path)))
		#
		# Load stream
		if elm.tag == 'stream':
			g_streams.append(Stream(elm,os.path.dirname(path),filename_base))
		#
		# Load audio
		if elm.tag == 'audiotrack':
			name = elm.attrib['name'] if 'name' in elm.attrib else 'xml_default_audio'
			g_audiotracks[name] = AudioTrack(elm,os.path.dirname(path))
		#
		# Load configuration
		if elm.tag == 'ffmpeg_config':
			g_configurations[elm.attrib['name']] = elm.attrib['value']
		#
		if elm.tag == 'config':
			config_table = {
				'fps' : 'r',
				'crf' : 'crf',
				'bitrate' : 'b:v',
				'pixel_format' : 'pix_fmt',
				'shape' : 's',
			}
			name = elm.attrib['name']
			if name in config_table.keys():
				value = replace_arguments(elm.attrib['value'],g_arguments)
				g_configurations[config_table[name]] = value
		#
		# Load exports
		if elm.tag == 'export':
			#
			export_path = evaluate(elm.attrib['path'],g_arguments,generate_function_table()) if 'path' in elm.attrib else elm.attrib['stream'] + '.mp4'
			if export_path:
				if not export_path[0] == '/':
					export_path = os.path.dirname(path) + '/' + export_path
			else:
				n = len(g_exports.keys())
				if n == 0:
					export_path = filename_base + '.mp4'
				else:
					export_path = f'{filename_base}-{n+1}' + '.mp4'
			audiotrack = elm.attrib['audiotrack'] if 'audiotrack' in elm.attrib else None
			timestamp = elm.attrib['timestamp'] if 'timestamp' in elm.attrib else None
			g_exports[elm.attrib['stream']] = {
				'path' : export_path,
				'audiotrack' : audiotrack,
				'timestamp' : timestamp,
			}
	#
	g_current_xml_path.pop()
#
def signal_handler(*args):
	print( 'Sinal detected. Aborting...' )
	sys.exit()

if __name__ == '__main__':
	#
	signal.signal(signal.SIGINT, signal_handler)
	signal.signal(signal.SIGTERM, signal_handler)
	#
	# Parse arguments
	parser = argparse.ArgumentParser()
	parser.add_argument('xml_path', nargs='*', help='XML file path')
	parser.add_argument('--complex_filter', action='store_true', help='print complex_filter')
	parser.add_argument('--preview', action='store_true',help='Enter preview mode')
	parser.add_argument('--timestamp', action='store_true',help='Show time stamp')
	parser.add_argument('--stream', help='stream name to preview')
	parser.add_argument('--starts_from', type=float, help='seconds to begin')
	parser.add_argument('--duration', type=float, help='seconds duration')
	parser.add_argument('--port', type=int, default=8020, help='preview http port' )
	parser.add_argument('--scale', type=float, default="1.0", help='output scaling factor')
	parser.add_argument('--set', nargs='+', help="set global variables")
	args = parser.parse_args()
	#
	if not args.xml_path:
		parser.print_help(sys.stderr)
		sys.exit(1)
	#
	# Parse XML file
	for xml_path in args.xml_path:
		#
		g_arguments.clear()
		g_materials.clear()
		g_functions.clear()
		g_streams.clear()
		g_audiotracks.clear()
		g_configurations.clear()
		g_label_counter.clear()
		g_exports.clear()
		g_current_xml_path.clear()
		#
		if os.path.exists('/mount'):
			root_parse_xml = '/mount/'+xml_path
		else:
			root_parse_xml = xml_path
		g_current_xml_path.append(root_parse_xml)
		#
		if args.set:
			for x in args.set:
				key,value = x.split('=')
				print( f'set global {key} = {value}')
				g_arguments[key] = value
		#
		parse_xml(str(pathlib.Path(__file__).parent)+'/'+'functions.xml')
		parse_xml(root_parse_xml)
		#
		# Fill missing configs
		default_configs = {
			'pix_fmt' : 'yuv420p',
			'crf' : '18',
		}
		for key,value in default_configs.items():
			if not key in g_configurations:
				g_configurations[key] = value
		#
		# If the scaling is specified, do so
		rescale_via_vf = False
		if not args.scale == 1.0:
			if 's' in g_configurations:
				(w,h) = tuple([ int(x) for x in g_configurations['s'].split('x')])
				g_configurations['s'] = f'{int(args.scale*w)}x{int(args.scale*h)}'
			else:
				rescale_via_vf = True
		#
		# If only one stream is found, say that it's the stream to export
		if not g_exports:
			count = 0
			main_stream_name = None
			for stream in g_streams:
				if stream.main_stream:
					count += 1
					main_stream_name = stream.name
			if count == 1:
				path = f'{main_stream_name}.mp4' if stream.dirpath[0] == '/' else stream.dirpath + '/' + f'{main_stream_name}.mp4'
				g_exports[main_stream_name] = {
					'path':path,
					'audiotrack':None,
					'timestamp':False
				}
			else:
				print( f'{count} non-named streams found. Nothing to export. Provide <export ...> tag.' )
		#
		# If stream is specified together with preview, set it as an only thing to preview
		if args.preview and args.stream:
			g_exports.clear()
			g_exports[args.stream] = {
				'path':'args.stream'+'.mp4', # will not be used anyway
				'audiotrack':None,
				'timestamp':False
			}
		#
		for name,info in g_exports.items():
			#
			# Recursively increment reference counter
			reset()
			stream = find_reference(name,['stream'])
			stream.recursively_increment_counter()
			#
			# Generate input commands
			index = 0
			input_commands = []
			for material in g_materials:
				cmd = material.generate_input_cmd(index)
				if cmd:
					input_commands.append(cmd)
					index += 1
			#
			# Generate filter command
			try:
				(commands,outputs,infos) = stream.generate({})
			except ValueError as e:
				print(e)
				continue
			#
			# If no outputs are found, skip the loop
			if not outputs:
				print( f'No output. Skipping "{name}"...' )
				continue
			#
			# If more than one outputs are found, we are not sure what to do. Skip as well
			if len(outputs) > 1:
				print( f'Multiple outputs ({len(outputs)}). Skipping "{name}"...' )
				continue
			#
			# If audio track is specified, load it
			if len(g_audiotracks) == 1 and 'xml_default_audio' in g_audiotracks:
				audiotrack = g_audiotracks['xml_default_audio']
				input_commands.extend(audiotrack.generate_input_cmd(index))
				generation_command,audio_output = audiotrack.generate(infos[0]['duration'])
				if audio_output:
					commands.extend(generation_command)
			else:
				audiotrack_name = info['audiotrack']
				audio_output = None
				if audiotrack_name:
					if not audiotrack_name in g_audiotracks:
						print( f'{audiotrack_name} was not found.')
						sys.exit()
					else:
						audiotrack = g_audiotracks[audiotrack_name]
						input_commands.extend(audiotrack.generate_input_cmd(index))
						generation_command,audio_output = audiotrack.generate(infos[0]['duration'])
						if audio_output:
							commands.extend(generation_command)
			#
			# Specify starting time in seconds if requested
			time_trim_command = []
			if args.starts_from or args.duration:
				start_time = min(args.starts_from,infos[0]['duration']) if args.starts_from else 0.0
				end_time = min(start_time+args.duration,infos[0]['duration']) if args.duration else infos[0]['duration']
				time_trim_command = [f'-ss {start_time} -t {end_time-start_time}']
			#
			# Rescale using scale command
			if rescale_via_vf:
				label = generate_label('rescale')
				commands.append(f'[{outputs[0]}]scale=iw*{args.scale}:-1[{label}]')
				outputs = [f'{label}']
			#
			# Overlay time stamp
			if args.preview or args.timestamp or info['timestamp']:
				label = generate_label('timestamp')
				timestamp_format = 'timestamp: %{pts\:hms}'
				timestamp_cmd = f"[{outputs[0]}]drawtext=text='{timestamp_format}':fontcolor=white:shadowcolor=black:shadowx=2:shadowy=2[{label}]"
				commands.append(timestamp_cmd)
				outputs = [f'{label}']
			#
			# Generate setting command
			config_commands = []
			for key,value in g_configurations.items():
				config_commands.append(f'-{key} {value}')
			#
			if args.preview:
				path = f'-listen 1 -f matroska http://0.0.0.0:{args.port}'
			else:
				path = info['path']
				dir = os.path.dirname(path)
				if dir and not os.path.exists(dir):
					os.makedirs(dir)
			#
			# Build final ffmpeg command
			ffmpeg_program = 'ffmpeg -stats'
			#
			filter_complex_command = [f'-filter_complex "{";".join(commands)}"'] if commands else []
			map_command = [f'-map [{outputs[0]}]'] if commands else []
			if map_command and audio_output:
				map_command += [f'-map [{audio_output}]']
			ffmpeg_command = f'{ffmpeg_program} -y {" ".join(input_commands+filter_complex_command+config_commands+map_command+time_trim_command+[path])}'
			#
			# Print the total second count
			print( '<stream="{}" seconds="{:.2f}" shape="{}x{}" fps="{}">'.format(
				name,infos[0]['duration'],infos[0]['shape'][0],infos[0]['shape'][1],infos[0]['fps'])
			)
			if float('inf') == infos[0]['duration']:
				print( 'Error: time is infinite.' )
				sys.exit()
			#
			# Run it and open it
			if args.complex_filter:
				print( ffmpeg_command )
			else:
				#
				if args.preview:
					print( f'ffplay -loglevel error -autoexit http://127.0.0.1:{args.port}' )
				#
				subprocess.call(ffmpeg_command,shell=True)
		#
		g_current_xml_path.pop()