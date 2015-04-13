# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun  5 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MainWindow
###########################################################################

class MainWindow ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"MyRTA", pos = wx.DefaultPosition, size = wx.Size( 820,564 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		self.m_menubar1 = wx.MenuBar( 0 )
		self.m_menu_file = wx.Menu()
		self.m_menubar1.Append( self.m_menu_file, u"&File" ) 
		
		self.m_menu_help = wx.Menu()
		self.m_menubar1.Append( self.m_menu_help, u"&Help" ) 
		
		self.SetMenuBar( self.m_menubar1 )
		
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		sb_sizer_buttons = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Commands" ), wx.HORIZONTAL )
		
		sb_sizer_buttons.SetMinSize( wx.Size( -1,20 ) ) 
		self.m_button_run = wx.Button( self, wx.ID_ANY, u"Run", wx.DefaultPosition, wx.DefaultSize, 0 )
		sb_sizer_buttons.Add( self.m_button_run, 0, wx.ALL, 5 )
		
		self.m_button_stop = wx.Button( self, wx.ID_ANY, u"Stop", wx.DefaultPosition, wx.DefaultSize, 0 )
		sb_sizer_buttons.Add( self.m_button_stop, 0, wx.ALL, 5 )
		
		self.m_button7 = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0 )
		sb_sizer_buttons.Add( self.m_button7, 0, wx.ALL, 5 )
		
		self.m_button8 = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0 )
		sb_sizer_buttons.Add( self.m_button8, 0, wx.ALL, 5 )
		
		
		bSizer4.Add( sb_sizer_buttons, 1, wx.EXPAND, 5 )
		
		self.m_splitter1 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitter1.SetSashGravity( 0.3 )
		self.m_splitter1.Bind( wx.EVT_IDLE, self.m_splitter1OnIdle )
		
		self.m_panel3 = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel3, wx.ID_ANY, u"label" ), wx.VERTICAL )
		
		
		self.m_panel3.SetSizer( sbSizer2 )
		self.m_panel3.Layout()
		sbSizer2.Fit( self.m_panel3 )
		self.m_panel4 = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_splitter1.SplitVertically( self.m_panel3, self.m_panel4, 0 )
		bSizer4.Add( self.m_splitter1, 5, wx.EXPAND, 5 )
		
		self.m_textCtrl1 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.m_textCtrl1, 4, wx.ALL|wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer4 )
		self.Layout()
		self.m_statusBar1 = self.CreateStatusBar( 3, wx.ST_SIZEGRIP, wx.ID_ANY )
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	
	def m_splitter1OnIdle( self, event ):
		self.m_splitter1.SetSashPosition( 0 )
		self.m_splitter1.Unbind( wx.EVT_IDLE )
	

