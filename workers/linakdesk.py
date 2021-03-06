from interruptingcow import timeout

from mqtt import MqttMessage
from workers.base import BaseWorker

REQUIREMENTS = ['git+https://github.com/zewelor/linak_bt_desk.git']

class LinakdeskWorker(BaseWorker):
  def _setup(self):
    from linak_dpg_bt import LinakDesk

    self.desk = LinakDesk(self.mac)

  def status_update(self):
    return [MqttMessage(topic=self.format_topic('height/cm'), payload=self._get_height())]

  def _get_height(self):
    with timeout(20):
      self.desk.read_dpg_data()
      return self.desk.current_height_with_offset.cm

    return -1

