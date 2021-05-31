import sublime 
import sublime_plugin

# This plugin expects the first line to contain field label of picklist field
class FileRewriteCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		# Content for new tab written to this var
		output_content = []

		row_number = 0
		prev_line = ''

		# Create new window
		new_tab = self.view.window().new_file()

		# Get handle to contents of window
		content = self.view.substr(sublime.Region(0, len(self.view)))
		
		# Traverse contents of window
		for line in content.split('\n'):
			row_number += 1
			
			prev_line = line
			if row_number == 1:
				# Add header to output
				output_content.append(self.create_header(line, prev_line))
			else:
				if line.lower().find('keep') > 0:
					output_content.append(self.create_picklist_entry(line))

		# Add the footer part
		output_content.append(self.create_footer())

		# With content completely built, inject into new tab		
		new_tab.run_command('append', {"characters" : '\n'.join(output_content)})


	# Responsible for creating the header
	def create_header(self, p_line, p_prev_line):

		# Extract label
		label = p_prev_line.strip()
		# Extract the API name by splitting the string and plucking the first string from array
		full_name = p_line.split()[0].strip()

		header = '<?xml version="1.0" encoding="UTF-8"?>\n'
		header += '<CustomField xmlns="http://soap.sforce.com/2006/04/metadata">\n'
		header += '    <fullName>' + full_name + '</fullName>\n'
		header += '    <externalId>false</externalId>\n'
		header += '    <label>' + label +'</label>\n'
		#header += '    <required>false</required>\n'
		#header += '    <trackFeedHistory>false</trackFeedHistory>\n'
		#header += '    <trackHistory>false</trackHistory>\n'
		#header += '    <trackTrending>false</trackTrending>\n'
		header += '    <type>Picklist</type>\n'
		header += '    <valueSet>\n'
		header += '        <valueSetDefinition>\n'
		header += '            <sorted>true</sorted>'

		return header		

	# Responsible for creating a picklist entry
	def create_picklist_entry(self, p_line):
		# substring from start to position of 'keep' - then strips leading and trailing whitespace
		label = (p_line[:p_line.lower().find('keep')]).strip()

		picklist_entry = '            <value>\n'
		picklist_entry += '                <fullName>' + label + '</fullName>\n'
		picklist_entry += '                <default>false</default>\n'
		picklist_entry += '                <label>' + label + '</label>\n'
		picklist_entry += '            </value>'

		return picklist_entry

	# Responsible for creating the footer (i.e. closing the open tags)
	def create_footer(self):
		footer = '        </valueSetDefinition>\n'
		footer += '    </valueSet>\n'
		footer += '</CustomField>'

		return footer




