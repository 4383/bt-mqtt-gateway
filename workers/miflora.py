from interruptingcow import timeout
from mqtt import MqttMessage
from workers.base import BaseWorker

REQUIREMENTS = ['miflora']

monitoredAttrs = ["temperature", "moisture", "light", "conductivity", "battery"]

class MifloraWorker(BaseWorker):
  def _setup(self):

    for name, mac in self.devices.items():
      self.devices[name] = mac

  def status_update(self):
    ret = []
    for name, mac in self.devices.items():
      try:
        ret += self.update_device_state(name, mac)
      except RuntimeError:
        pass

    return ret

  @timeout(8.0)
  def update_device_state(self, name, mac):
    from miflora.miflora_poller import MiFloraPoller
    from btlewrap.bluepy import BluepyBackend

    poller = MiFloraPoller(mac, BluepyBackend)

    ret = []
    for attr in monitoredAttrs:

      ret.append(MqttMessage(topic=self.format_topic(name, attr), payload=poller.parameter_value(attr)))

    return ret
