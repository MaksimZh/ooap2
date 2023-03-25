# Иерархия источников питания

class PowerSource:
    pass

class BatteryPowerSource(PowerSource):
    pass

class WirePowerSource(PowerSource):
    pass


# Иерархия интерфейсов подключения

class Connection:
    pass

class UsbConnection(Connection):
    pass

class BluetoothConnection(Connection):
    pass


# Иерархия пользовательского интерфейса

class UserInterface:
    pass

class KeyboardInterface:
    pass

class MouseInterface:
    pass


# Python позволяет множественное наследование

# Bluetooth-мышь с питанием от батареи
class BluetoothMouse(BatteryPowerSource, BluetoothConnection, MouseInterface):
    pass

# Проводная клавиатура с подключением по USB и питанием по этому же проводу
class UsbKeyboard(WirePowerSource, UsbConnection, MouseInterface):
    pass
