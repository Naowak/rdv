from kivy.garden.mapview import MapView, MapMarker
from kivy.app import App
from kivy.clock import Clock, mainthread
from kivy.utils import platform
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from plyer import gps
from android.permissions import request_permissions, Permission

import traceback



class MapViewApp(App):
    
    def build(self):
        self.current_lat = 0
        self.current_lon = 0

        self.init_gps()
        self.start_gps()
        
        self.mapview = MapView(zoom=24, lat=self.current_lat, lon=self.current_lon)
        self.label = Label(text='Locations are supposed to be printed here.')

        self.layout = GridLayout(rows=2)
        self.layout.add_widget(self.mapview)
        self.layout.add_widget(self.label)


        return self.layout

    def request_android_permissions(self):
        
        def callback(permissions, results):
            if all([res for res in results]):
                print("callback. All permissions granted.")
            else:
                print("callback. Some permissions refused.")

        request_permissions([Permission.INTERNET,
                            Permission.ACCESS_COARSE_LOCATION,
                            Permission.ACCESS_FINE_LOCATION], callback)

    def init_gps(self):
        try :
            gps.configure(on_location=self.on_location,
                          on_status=self.on_status)
        except NotImplementedError:
            traceback.print_exc()
            self.gps_status = 'GPS is not implemented for your platform'
        
        if platform == "android":
            print("gps.py: Android detected. Requesting permissions")
            self.request_android_permissions()

    def start_gps(self):
        gps.start(1000, 1)

    def stop_gps(self):
        gps.stop()

    @mainthread
    def on_location(self, **kwargs):
        self.current_lat = kwargs['lat']
        self.current_lon = kwargs['lon']

        self.mapview.center_on(self.current_lat, self.current_lon)
        marker = MapMarker(lat=self.current_lat, lon=self.current_lon)
        self.mapview.add_marker(marker)
        
        self.label.text = '\n'.join([f'{k} : {v}' for k,v in kwargs.items()])
        print(self.current_lat, self.current_lon)

    @mainthread
    def on_status(self, stype, status):
        pass


MapViewApp().run()