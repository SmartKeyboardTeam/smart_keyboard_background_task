from threading import Thread
import subprocess
import serial.tools.list_ports
import globals


class KeyboardExecutor:
    def __init__(self):
        self.listening_ports = set()

    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(KeyboardExecutor, self).__new__(self)
        return self.instance

    def run(self):
        daemon = Thread(target=self.__listen_to_ports,
                        daemon=True, name='PortsListening')
        daemon.start()

    def __execute_script(self, pin):
        script = next(
            (element for element in globals.scripts if element['pin'] == pin), None)
        if script:
            try:
                subprocess.Popen(["powershell", script['command']], stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, shell=True, creationflags=0x08000000)
            except Exception as e:
                print(e)

    def __listen_to_serial(self, port):
        try:
            ser = serial.Serial(port, baudrate=9600, timeout=1)
            print(f"Listening to {port}")

            while True:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    self.__execute_script(int(line))

        except serial.SerialException:
            print(f"{port} disconnected. Stopping listening.")

    def __listen_to_ports(self):
        while True:
            connected_ports = [
                port.device for port in serial.tools.list_ports.comports()]

            # Check for newly connected ports
            for port in connected_ports:
                if port not in self.listening_ports:
                    daemon = Thread(target=self.__listen_to_serial, args=(port,),
                                    daemon=True, name='PortsListening')
                    daemon.start()
                    self.listening_ports.add(port)

            # Check for disconnected ports
            disconnected_ports = self.listening_ports - set(connected_ports)
            for port in disconnected_ports:
                self.listening_ports.remove(port)
