from serial import Serial


class SerialX(Serial):
    def write(self, data):
        self.flushInput()
        self.flushOutput()
        data = super().write(data)
        out = ""
        while True:
            out += str(self.read(1))
            if "\n" in out and self.inWaiting() <= 0:
                return out
