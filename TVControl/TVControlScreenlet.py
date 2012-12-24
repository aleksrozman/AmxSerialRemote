#!/usr/bin/env python

# This application is released under the GNU General Public License 
# v3 (or, at your option, any later version). You can find the full 
# text of the license under http://www.gnu.org/licenses/gpl.txt. 
# By using, editing and/or distributing this software you agree to 
# the terms and conditions of this license. 
# Thank you for using free software!


import screenlets
from screenlets.options import StringOption , BoolOption , IntOption , FileOption , DirectoryOption , ListOption , AccountOption , TimeOption , FontOption, ColorOption , ImageOption
from screenlets.options import create_option_from_node
from screenlets import DefaultMenuItem
import pango
import gobject
import gtk
import os

class TVControlScreenlet (screenlets.Screenlet):
	"""An AMX Serial Control Remote"""
	
	# default meta-info for Screenlets (should be removed and put into metainfo)
	__name__	= 'TVControlScreenlet'
	__version__	= '0.3'
	__author__	= 'Aleks'
	__desc__	= __doc__	# set description to docstring of class
	
	# editable options (options that are editable through the UI)

	volume_b = (255 / 255.0, 255 / 255.0, 255 / 255.0,.8)
	volume_fill = (0 / 255.0, 0 / 255.0, 151 / 255.0,.8)
	chinput_b = (1,1,1,1)
	main_border = (.5,.6,.8,1)
	main_b = (0,0,0,1)
	buttons_b = (1,1,1,1)
	channel_text = (0,0,0,1)
	main_text = (1,1,1,1)
	buttons_shadow = (204 / 255.0, 204 / 255.0, 204 / 255.0,.9)
	
	# User needs to fill this location out for the absolute path to the executable
	# directory that contains the compiled C files
	# Make sure it ends with a slash (/)
	path_to_exec = "./"
	channels = [['my_tv.png',3],['cbs.png',4],['abc.png',8],['nbc.png',10],['fox.png',11],['cw.png',12],['tbs.png',17],['comedy.png',27],['tnt.png',29],['abc_family.png',32],['history.png',37],['discovery.png',38],['cartoon_network.png',55],['fx.png',59],['fox_news.png',60],['science_channel.png',80],['sci_fi.png',93],['prev.png',0]]
	cols = 3
	font_example = "Sans Medium 5"

	bsize = 50
	buttoncenter = 5
	bspacing = 20

	v_padding = 50
	h_padding = 20

	power_b_width = 50
	power_spacing = 50
	power_width = power_b_width*2+power_spacing
	power_height = 50
	power_top = v_padding
	power_bottom = power_top + power_height

	power_channel_spacing = 50
	buttonsize = bsize + 2 * buttoncenter
	buttonspacing = buttonsize + bspacing
	channel_top = power_channel_spacing + power_bottom
	channel_bottom = (len(channels)-1)//cols * buttonspacing + channel_top + buttonsize
	channel_left = h_padding
	channel_right = buttonspacing * cols + channel_left
	
	channel_volume_spacing = 20
	volume_height = channel_bottom - channel_top
	volume_width = 50
	volume_top = channel_top
	volume_bottom = volume_height + channel_top
	volume_left = channel_right + channel_volume_spacing
	volume_right = volume_left + volume_width
	

	clickvolume = int(.75 * volume_height)
	prevchannel = 0
	currentchannel = 0

	volume_mute = 0
	prev_clickvolume = clickvolume

	channel_chinput_spacing = 20
	chinput_width = volume_right - channel_left
	chinput_height = 30
	chinput_left = channel_left
	chinput_right = chinput_left + chinput_width
	chinput_top  = channel_bottom+channel_chinput_spacing
	chinput_bottom = chinput_top + chinput_height
	chinput = ""

	remote_width = volume_right + h_padding
	remote_height = chinput_bottom  + v_padding

	power_left = remote_width//2 - power_width//2
	power_right = power_left+power_width

	# constructor
	def __init__ (self, **keyword_args):
		#call super (width/height MUST match the size of graphics in the theme)
		screenlets.Screenlet.__init__(self, width=self.remote_width, height=self.remote_height,uses_theme=True, **keyword_args)
		# set theme
		self.theme_name = "logos"
		# add option group

		self.add_options_group('Sizes', 'Adjust Sizes')
		self.add_option(IntOption('Sizes','bspacing', 
			self.bspacing, 'Button Spacing', 
			'Example options group using integer', 
			min=0, max=200))
		self.add_option(IntOption('Sizes','buttoncenter', 
			self.buttoncenter, 'Button Center', 
			'Example options group using integer', 
			min=0, max=200))
		self.add_option(IntOption('Sizes','v_padding', 
			self.v_padding, 'Vertical Padding', 
			'Example options group using integer', 
			min=0, max=200))
		self.add_option(IntOption('Sizes','h_padding', 
			self.h_padding, 'Horizontal Padding', 
			'Example options group using integer', 
			min=0, max=200))
		self.add_option(IntOption('Sizes','power_spacing', 
			self.power_spacing, 'Power Spacing', 
			'Example options group using integer', 
			min=0, max=200))
		self.add_option(IntOption('Sizes','power_channel_spacing', 
			self.power_channel_spacing, 'Power Channel Spacing', 
			'Example options group using integer', 
			min=0, max=200))
		self.add_option(IntOption('Sizes','channel_volume_spacing', 
			self.channel_volume_spacing, 'Channel Volume Spacing', 
			'Example options group using integer', 
			min=0, max=200))
		self.add_option(IntOption('Sizes','channel_chinput_spacing', 
			self.channel_chinput_spacing, 'Channel Input Spacing', 
			'Example options group using integer', 
			min=0, max=200))
		self.add_option(IntOption('Sizes','chinput_height', 
			self.chinput_height, 'Channel Input Height', 
			'Example options group using integer', 
			min=0, max=200))
		self.add_option(IntOption('Sizes','volume_width', 
			self.volume_width, 'Volume Width', 
			'Example options group using integer', 
			min=0, max=200))
		self.add_option(FontOption('Sizes','font_example', 
			self.font_example, 'Main Font', 
			'Example options group using font'))

		self.add_options_group('Colors', 'Adjust Colors')
		self.add_option(ColorOption('Colors','volume_b', 
			self.volume_b, 'Volume Background', 
			'Example options group using color'))
		self.add_option(ColorOption('Colors','volume_fill', 
			self.volume_fill, 'Volume Fill', 
			'Example options group using color'))
		self.add_option(ColorOption('Colors','buttons_shadow', 
			self.buttons_shadow, 'Button Shadow', 
			'Example options group using color'))
		self.add_option(ColorOption('Colors','buttons_b', 
			self.buttons_b, 'Buttons Background', 
			'Example options group using color'))
		self.add_option(ColorOption('Colors','chinput_b', 
			self.chinput_b, 'Input Background', 
			'Example options group using color'))
		self.add_option(ColorOption('Colors','main_border', 
			self.main_border, 'Main Border', 
			'Example options group using color'))
		self.add_option(ColorOption('Colors','main_b', 
			self.main_b, 'Main Background', 
			'Example options group using color'))
		self.add_option(ColorOption('Colors','channel_text', 
			self.channel_text, 'Current Channel Text Color', 
			'Example options group using color'))
		self.add_option(ColorOption('Colors','main_text', 
			self.main_text, 'Main Text Color', 
			'Example options group using color'))

	
	
		# ADD a 1 second (1000) TIMER
		self.timer = gobject.timeout_add( 1000, self.update)

		#Also add options from xml file for example porpuse
		#self.init_options_from_metadata() 

	def update (self):
		self.redraw_canvas()
		return True # keep running this event	
	
	# ONLY FOR TESTING!!!!!!!!!
	def init_options_from_metadata (self):
		"""Try to load metadata-file with options. The file has to be named
		like the Screenlet, with the extension ".xml" and needs to be placed
		in the Screenlet's personal directory. 
		NOTE: This function always uses the metadata-file relative to the 
			  Screenlet's location, not the ones in SCREENLETS_PATH!!!"""
		print __file__
		p = __file__.rfind('/')
		mypath = __file__[:p]
		print mypath
		self.add_options_from_file( mypath + '/' + \
			self.__class__.__name__ + '.xml')	


	def on_after_set_atribute(self,name, value):
		"""Called after setting screenlet atributes"""
		pass

	def on_before_set_atribute(self,name, value):
		"""Called before setting screenlet atributes"""
		pass


	def on_create_drag_icon (self):
		"""Called when the screenlet's drag-icon is created. You can supply
		your own icon and mask by returning them as a 2-tuple."""
		return (None, None)

	def on_composite_changed(self):
		"""Called when composite state has changed"""
		pass

	def on_drag_begin (self, drag_context):
		"""Called when the Screenlet gets dragged."""
		pass
	
	def on_drag_enter (self, drag_context, x, y, timestamp):
		"""Called when something gets dragged into the Screenlets area."""
		pass
	
	def on_drag_leave (self, drag_context, timestamp):
		"""Called when something gets dragged out of the Screenlets area."""
		pass

	def on_drop (self, x, y, sel_data, timestamp):
		"""Called when a selection is dropped on this Screenlet."""
		return False
		
	def on_focus (self, event):
		"""Called when the Screenlet's window receives focus."""
		pass
	
	def on_hide (self):
		"""Called when the Screenlet gets hidden."""
		pass
	
	def on_init (self):
		"""Called when the Screenlet's options have been applied and the 
		screenlet finished its initialization. If you want to have your
		Screenlet do things on startup you should use this handler."""
		# add default menu items
		self.add_default_menuitems()

	def toggle_mute(self):
		if self.volume_mute == 0:
			self.prev_clickvolume = self.clickvolume
			self.clickvolume = 0
			volume = 0
			self.volume_mute = 1
		else:
			self.clickvolume = self.prev_clickvolume
			self.volume_mute = 0
			volume = self.clickvolume / self.volume_height
			volume = 100 * volume
			volume = int(volume)
		os.system(path_to_exec + "volume_control "+str(volume))
		return False

	def ch_change (self,channel):
		self.prevchannel = self.currentchannel
		os.system(path_to_exec + "channel_changer "+channel)
		self.currentchannel = int(channel)
		self.chinput = ""
		return False

	def on_key_down(self, keycode, keyvalue, event):
		"""Called when a keypress-event occured in Screenlet's window."""
		key = gtk.gdk.keyval_name(event.keyval)
		if key == "Return" or key == "KP_Enter":
			self.ch_change(self.chinput)
		elif key == "BackSpace":
			self.chinput = ""
		elif key == "space":
			self.toggle_mute()
		else:
			temp = key[len(key)-1]
			try:
				int(temp)
			except:
				print "wrong key"
				return False
			self.chinput = self.chinput + key[(len(key)-1)]
			if len(self.chinput) == 2:
				self.ch_change(self.chinput)
		return True
		
	def on_load_theme (self):
		"""Called when the theme is reloaded (after loading, before redraw)."""
		pass
	
	def on_menuitem_select (self, id):
		"""Called when a menuitem is selected."""
		pass
	
	def on_mouse_down (self, event):
		"""Called when a buttonpress-event occured in Screenlet's window. 
		Returning True causes the event to be not further propagated."""
		5555
		if self.mousex < self.channel_right and self.mousex > self.channel_left and self.mousey < self.channel_bottom and self.mousey > self.channel_top:
			scaledx = (self.mousex-self.channel_left)
			scaledy = (self.mousey-self.channel_top)
			horizontal = (scaledx % self.buttonspacing)
			vertical = (scaledy % self.buttonspacing)
			if horizontal < self.buttonsize and vertical < self.buttonsize:
				choice = (scaledx // self.buttonspacing) + self.cols*(scaledy // self.buttonspacing)
			else:
				choice = len(self.channels)
			ichoice = int(choice)
			if ichoice < len(self.channels):
				if ichoice == len(self.channels) - 1:
					ch = self.prevchannel
				else:
					ch = self.channels[ichoice][1]
		    		self.ch_change(str(ch))
			    	return True
			else:
				return False
		if self.mousex < self.volume_right and self.mousex > self.volume_left and self.mousey < self.volume_bottom and self.mousey > self.volume_top:
			self.clickvolume = self.volume_height-(self.mousey-self.volume_top)
			volume = self.clickvolume / self.volume_height
			volume = 100 * volume
			volume = int(volume)
	    		os.system(path_to_exec + "volume_control "+str(volume))
			return True
		if self.mousex < self.power_right and self.mousex > self.power_left and self.mousey < self.power_bottom and self.mousey > self.power_top:
			if self.mousex < (self.power_left +self.power_b_width):
		    		os.system(path_to_exec + "power 1")
				return True
			if self.mousex > (self.power_left + self.power_b_width + self.power_spacing):
		    		os.system(path_to_exec + "power 0")
				return True
#		if self.mousex < self.chinput_right and self.mousex > self.chinput_left and self.mousey < self.chinput_bottom and self.mousey > self.chinput_top:
#			return True
		return False
	
	def on_mouse_enter (self, event):
		"""Called when the mouse enters the Screenlet's window."""
		pass
		
	def on_mouse_leave (self, event):
		"""Called when the mouse leaves the Screenlet's window."""
		pass
	def on_mouse_move(self, event):
		"""Called when the mouse moves in the Screenlet's window."""
#		self.redraw_canvas()
		pass

	def on_mouse_up (self, event):
		"""Called when a buttonrelease-event occured in Screenlet's window. 
		Returning True causes the event to be not further propagated."""
#		return False
		pass
			
	def on_quit (self):
		"""Callback for handling destroy-event. Perform your cleanup here!"""
		return True
		
	def on_realize (self):
		""""Callback for handling the realize-event."""
	
	def on_scale (self):
		"""Called when Screenlet.scale is changed."""
		pass
	
	def on_scroll_up (self):
		"""Called when mousewheel is scrolled up (button4)."""
		pass

	def on_scroll_down (self):
		"""Called when mousewheel is scrolled down (button5)."""
		pass
	
	def on_show (self):
		"""Called when the Screenlet gets shown after being hidden."""
		pass
	
	def on_switch_widget_state (self, state):
		"""Called when the Screenlet enters/leaves "Widget"-state."""
		pass
	
	def on_unfocus (self, event):
		"""Called when the Screenlet's window loses focus."""
		pass
	
	def on_draw (self, ctx):
		# if theme is loaded
		if self.theme:
			# set scale rel. to scale-attribute
			ctx.scale(self.scale, self.scale)
			ctx.set_source_rgba(self.main_border[0],self.main_border[1],self.main_border[2],self.main_border[3])
			self.theme.draw_rounded_rectangle(ctx,0,0,20,self.width,self.height)
			ctx.set_source_rgba(self.main_b[0],self.main_b[1],self.main_b[2],self.main_b[3])
			self.theme.draw_rounded_rectangle(ctx,5,5,20,self.width-10,self.height-10)
			y = self.channel_top
			x = self.channel_left
			for i in range(0,len(self.channels)):
				ctx.set_source_rgba(self.buttons_shadow[0],self.buttons_shadow[1],self.buttons_shadow[2],self.buttons_shadow[3])
				self.theme.draw_rounded_rectangle(ctx,x,y,10,self.buttonsize,self.buttonsize)
				ctx.set_source_rgba(self.buttons_b[0],self.buttons_b[1],self.buttons_b[2],self.buttons_b[3])
				self.theme.draw_rounded_rectangle(ctx,x+self.buttoncenter//2,y+self.buttoncenter//2,10,self.buttonsize-self.buttoncenter//2,self.buttonsize-self.buttoncenter//2)
				dimage = self.channels[i][0]
				ctx.save()
				ctx.translate(x+self.buttoncenter,y+self.buttoncenter)
				ctx.set_source_surface(self.theme[dimage], 0,0)
				ctx.paint()
				x = x + (self.buttonspacing)
				if x >= self.channel_right:
					y = y + (self.buttonspacing)
					x = self.channel_left
				ctx.restore()
			ctx.set_source_rgba(self.volume_b[0],self.volume_b[1],self.volume_b[2],self.volume_b[3])
			self.theme.draw_rectangle(ctx,self.volume_left,self.volume_top,self.volume_width,self.volume_height)
			ctx.set_source_rgba(self.volume_fill[0],self.volume_fill[1],self.volume_fill[2],self.volume_fill[3])
			self.theme.draw_rectangle(ctx,self.volume_left,self.volume_top+(self.volume_height - self.clickvolume),self.volume_width,self.clickvolume)

			ctx.save()
			ctx.translate(self.power_left,self.power_top)
			ctx.set_source_surface(self.theme['power.png'], 0,0)
			ctx.paint()
			ctx.restore()
			ctx.save()
			ctx.translate(self.power_left+self.power_b_width+self.power_spacing,self.power_top)
			ctx.set_source_surface(self.theme['poweroff.png'], 0,0)
			ctx.paint()
			ctx.restore()
			ctx.set_source_rgba(self.main_text[0],self.main_text[1],self.main_text[2],self.main_text[3])
			self.theme.draw_text(ctx, "AMX REMOTE", 0, 5, self.font_example, 20,self.width,pango.ALIGN_CENTER)
			self.theme.draw_text(ctx, "POWER", self.power_left,self.power_top, self.font_example, 10,self.power_width,pango.ALIGN_CENTER)
			self.theme.draw_text(ctx, "PRESETS", self.channel_left,self.channel_top-30, self.font_example, 10,self.channel_right-self.channel_left,pango.ALIGN_CENTER)
			self.theme.draw_line(ctx,self.channel_left,self.channel_top-15,self.channel_right-self.channel_left-self.bspacing,0,1)
			self.theme.draw_text(ctx, "VOLUME", self.volume_left,self.volume_top-30, self.font_example, 10,self.volume_width,pango.ALIGN_CENTER)

			ctx.set_source_rgba(153 / 255.0, 204 / 255.0, 225 / 255.0,1)
			self.theme.draw_rounded_rectangle(ctx,self.chinput_left-2,self.chinput_top-2,5,self.chinput_width,self.chinput_height)
			ctx.set_source_rgba(self.chinput_b[0],self.chinput_b[1],self.chinput_b[2],self.chinput_b[3])
			self.theme.draw_rounded_rectangle(ctx,self.chinput_left,self.chinput_top,5,self.chinput_width,self.chinput_height)
			
			ctx.set_source_rgba(self.channel_text[0],self.channel_text[1],self.channel_text[2],self.channel_text[3])
			printstring = ""
			if len(self.chinput) != 0:
				printstring = self.chinput
			elif self.currentchannel != 0:
				printstring = str(self.currentchannel)

			self.theme.draw_text(ctx, printstring, self.chinput_left,self.chinput_top, self.font_example, 20,self.chinput_width,pango.ALIGN_CENTER)
			# TEST: render example-bg into context (either PNG or SVG)
			# render svg-file
			#self.theme['example-bg.svg'].render_cairo(ctx)
			# render png-file
	
	def on_draw_shape (self, ctx):
		self.on_draw(ctx)
	
# If the program is run directly or passed as an argument to the python
# interpreter then create a Screenlet instance and show it
if __name__ == "__main__":
	# create new session
	import screenlets.session
	screenlets.session.create_session(TVControlScreenlet)

