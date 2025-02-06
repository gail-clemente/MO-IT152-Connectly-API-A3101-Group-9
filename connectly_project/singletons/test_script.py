from config_manager import ConfigManager

config1 = ConfigManager()
config2 = ConfigManager()

assert config1 is config2  # Both instances should be the same
#print("Initial DEFAULT_PAGE_SIZE:", config1.get_setting("DEFAULT_PAGE_SIZE"))
config1.set_setting("DEFAULT_PAGE_SIZE", 50)

print("Config1 DEFAULT_PAGE_SIZE:", config1.get_setting("DEFAULT_PAGE_SIZE"))
print("Config2 DEFAULT_PAGE_SIZE:", config2.get_setting("DEFAULT_PAGE_SIZE"))

assert config2.get_setting("DEFAULT_PAGE_SIZE") == 50

print("Singleton is working correctly!")

