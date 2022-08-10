import os
import sys
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
from main import Wifi


_exe_path_ = os.path.join(*[os.environ['VIRTUAL_ENV'], 'Scripts', 'pythonservice.exe'])


class AppServerSvc (win32serviceutil.ServiceFramework):
    _svc_name_ = "WifiReachabilityService"
    _svc_display_name_ = "Wifi"

    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        win32serviceutil.ServiceFramework.__exe_path__ = os.path.join(*[os.environ['VIRTUAL_ENV'], 'Scripts', 'pythonservice.exe'])
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_,''))
        self.main()

    def main(self):
        if os.name == 'nt':
            os.system('chcp 65001 >nul 2>&1')
        if sys.stdout.encoding != 'utf8':
            sys.stdout.reconfigure(encoding='utf8')
        if sys.stderr.encoding != 'utf8':
            sys.stderr.reconfigure(encoding='utf8')
        wifi = Wifi()
        wifi.main()

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(AppServerSvc)