from appium import webdriver

DESIRED_CAPS = {}
DESIRED_CAPS["app"] = r"C:\\Users\\Stefan Stankovic\\Documents\\BSci\\flow_modulation\\Bsci.FlowModulation\\bin\\Debug\\net48\\Bsci.FlowModulation"
DESIRED_CAPS["platformName"] = "Windows"
DESIRED_CAPS["deviceName"] = "DESKTOP-B1O1ABM"
driver = webdriver.Remote(
command_executor="http://127.0.0.1:4723",
desired_capabilities=DESIRED_CAPS)