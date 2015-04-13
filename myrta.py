import wx
import myrta_window

if __name__ == "__main__":
    app = wx.App()
    mw = myrta_window.MainWindow(None)
    mw.Show()
    app.MainLoop()