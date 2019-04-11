from serial import Serial


class SerialX(Serial):

    def write(self, data):
        print "cmd", data
        self.flushInput()
        self.flushOutput()
        data = super(SerialX, self).write(data)
        out = ""
        out = self.readline()
        while True:
            out += str(self.read(1))
            if "\n" in out and self.inWaiting() <= 0:
                print  out
                return out
