import config
import string


class SerialConfig(config.Config):

     def afterLoad(self):
         self.values["baudrate"] = int(self.values["baudrate"])
         self.values["readTimeout"] = int(self.values["readTimeout"])

