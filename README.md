# openHAB-Helper-Libraries-MQTT-Event-Bus
A MQTT Event Bus for openHAB 2.x and 3.x using the [Helper Libraries for openHAB Scripted Automation](https://openhab-scripters.github.io/openhab-helper-libraries/index.html). Tested with openHAB 2.x and openHAB 3.x. This should work equivalent like the [Event bus binding](https://v2.openhab.org/addons/bindings/mqtt1/#event-bus-binding-configuration) from the old [MQTT 1.x binding](https://v2.openhab.org/addons/bindings/mqtt1/).

Description:
Publish/receive all states/commmands directly on the openHAB eventbus.

Usage:
Perfect for integrating multiple openHAB instances or broadcasting all events.

## Preparation

### Install the mosquitto MQTT broker

The next step is to install the mosquitto MQTT broker on the master with

```
sudo apt install mosquitto mosquitto-clients
```

The slaves only need `mosquitto-clients` because all slaves will later be connected to the master.

Then you have to edit the mosquitto.conf file:

```
# Place your local configuration in /etc/mosquitto/conf.d/
#
# A full description of the configuration file is at
# /usr/share/doc/mosquitto/examples/mosquitto.conf.example

listener 1883 0.0.0.0

pid_file /run/mosquitto/mosquitto.pid

persistence true
persistence_location /var/lib/mosquitto/

log_dest file /var/log/mosquitto/mosquitto.log

include_dir /etc/mosquitto/conf.d

allow_anonymous true
```

Of course you can use a password which mean you should not have to use `allow_anonymous true`. The more important thing is that you have to use `listener 1883 0.0.0.0`. This means that the mosquitto broker will be public accessible for all slaves (maybe if you want with a password).

### Install Jython on openHAB 2.x

#### Install the openHAB Helper Libraries

At first go to `PaperUI` and install the `Next-Generation Rule Engine`:

`OpenHAB --> PaperUI --> Addons --> Misc --> Next-Generation Rule Engine --> Install`

Then you have to stop openHAB with

```
sudo systemctl stop openhab2.service
```

After that we download the openHAB Helper Libraries and unzip them:

```
cd ~
wget https://github.com/openhab-scripters/openhab-helper-libraries/archive/master.zip
unzip master.zip
sudo mv openhab-helper-libraries-master/ openhab-helper-libraries
```

In the next step we will move the Helper Libraries to openHAB 2:

```
sudo cp -R ~/openhab-helper-libraries/Core/* /etc/openhab2/
sudo chmod -R 777 /etc/openhab2/automation
sudo chown -R openhab:openhab /etc/openhab2/automation
```

#### Install Jython

We have to rename following two files to use Jython:

```
sudo mv /etc/openhab2/automation/lib/python/configuration.py.example /etc/openhab2/automation/lib/python/configuration.py
sudo mv /etc/openhab2/automation/lib/python/personal/__init__.py.example /etc/openhab2/automation/lib/python/personal/__init__.py
```

Then you have to change the `EXTRA_JAVA_OPTS` with `sudo nano /etc/default/openhab2` that it has following parameters:

```
EXTRA_JAVA_OPTS="-Xbootclasspath/a:/etc/openhab2/automation/jython/jython-standalone-2.7.0.jar -Dpython.home=/etc/openhab2/automation/jython -Dpython.path=/etc/openhab2/automation/lib/python"
```

Please make sure that if you need other parameters that they are also used! If you use as example `Java 11` you have to use `Jython 2.7.2` instead of `Jython 2.7.0`.

In the next step we will download Jython and move it to the path given in the parameters above:

```
sudo mkdir -p /etc/openhab2/automation/jython
wget https://repo1.maven.org/maven2/org/python/jython-standalone/2.7.0/jython-standalone-2.7.0.jar
sudo mv ~/jython-standalone-2.7.0.jar /etc/openhab2/automation/jython/jython-standalone-2.7.0.jar
sudo chmod -R 777 /etc/openhab2/automation/jython/
sudo chown -R openhab:openhab /etc/openhab2/automation/jython/
```

If you use `Jython 2.7.2` you have to do following:

```
sudo mkdir -p /etc/openhab2/automation/jython
wget https://repo1.maven.org/maven2/org/python/jython-standalone/2.7.2/jython-standalone-2.7.2.jar
sudo mv ~/jython-standalone-2.7.2.jar /etc/openhab2/automation/jython/jython-standalone-2.7.2.jar
sudo chmod -R 777 /etc/openhab2/automation/jython/
sudo chown -R openhab:openhab /etc/openhab2/automation/jython/
```

As example you can test if Jython works by using the `Hello World example`:

```
sudo cp -R ~/openhab-helper-libraries/Script\ Examples/Python/hello_world.py /etc/openhab2/automation/jsr223/python/personal/hello_world.py
sudo chmod +x /etc/openhab2/automation/jsr223/python/personal/hello_world.py
sudo chown -R openhab:openhab /etc/openhab2/automation/jsr223/python/personal/hello_world.py
```

### Install Jython on openHAB 3.x


#### Install the openHAB Helper Libraries

You have to stop openHAB with

```
sudo systemctl stop openhab.service
```

After that we clone the openHAB Helper Libraries:

```
cd ~
git clone https://github.com/CrazyIvan359/openhab-helper-libraries.git
```

In the next step we will move the Helper Libraries to openHAB 3:

```
sudo cp -R ~/openhab-helper-libraries/Core/* /etc/openhab/
sudo chmod -R 777 /etc/openhab/automation
sudo chown -R openhab:openhab /etc/openhab/automation
```

#### Install Jython

We have to rename following two files to use Jython:

```
sudo mv /etc/openhab/automation/lib/python/configuration.py.example /etc/openhab/automation/lib/python/configuration.py
sudo mv /etc/openhab/automation/lib/python/personal/__init__.py.example /etc/openhab/automation/lib/python/personal/__init__.py
```

For openHAB 3.x we don't have to set the `EXTRA_JAVA_OPTS` parameters. Also we don't have to download and install Jython externally.

You have to start openHAB again with:

```
sudo systemctl start openhab.service
```

At first go to `Settings` and install `Jython`:

`OpenHAB --> Settings --> Automation --> + --> Jython Scripting --> Install`

As example you can test if Jython works by using the `Hello World example`:

```
sudo cp -R ~/openhab-helper-libraries/Script\ Examples/Python/hello_world.py /etc/openhab/automation/jsr223/python/personal/hello_world.py
sudo chmod +x /etc/openhab/automation/jsr223/python/personal/hello_world.py
sudo chown -R openhab:openhab /etc/openhab/automation/jsr223/python/personal/hello_world.py
```

## Install the MQTT Event Bus

### Install the MQTT Event Bus on openHAB 2.x

The script is adapted from Rich Koshak's [Marketplace MQTT Event Bus Script](https://community.openhab.org/t/marketplace-mqtt-event-bus/76938) from his [openHAB Rules Tools](https://github.com/rkoshak/openhab-rules-tools). We adopt a part of it.

```
cd ~
git clone https://github.com/rkoshak/openhab-rules-tools.git
cp -r ~/openhab-rules-tools/rules_utils/automation /etc/openhab2
git clone https://github.com/Michdo93/openHAB-Helper-Libraries-MQTT-Event-Bus.git
cp -r ~/openHAB-Helper-Libraries-MQTT-Event-Bus/mqtt_eb/automation /etc/openhab
sudo chmod -R 777 /etc/openhab2/automation
sudo chown -R openhab:openhab /etc/openhab2/automation
```

Please copy the configuration from `/etc/openhab2/automation/lib/python/configuration.py.mqtt_eb-example` to `/etc/openhab2/automation/lib/python/configuration.py` and adjust it accordingly.

You can have a look on the master/slave example!

Also you have to install the MQTT 2.x Binding. Go to `PaperUI --> Add-ons --> Bindings --> MQTT Binding --> Install`. After that you have to create a connection to the installed Mosquitto Broker with a `MQTT Broker Thing`. Go to `Things --> + --> MQTT Binding --> Add manually --> MQTT Broker`. At least this thing should contain a `Triggering Channel`. The master should have a `Triggering Channel` which should be triggered if the slave send out `commands` and the slave(s) should have a `Triggering Channel` which should be triggered if the master send out `states`.

Please make sure that the configuration.py uses the `Thing Identifier` as parameter for `mqtt_eb_broker` and the `Channel Identifier` as parameter for `mqtt_eb_in_chan`!

For a better understanding have a look at the configuration for openHAB 3!

### Install the MQTT Event Bus on openHAB 3.x

The script is adapted from Rich Koshak's [Marketplace MQTT Event Bus Script](https://community.openhab.org/t/marketplace-mqtt-event-bus/76938) from his [openHAB Rules Tools](https://github.com/rkoshak/openhab-rules-tools). We adopt a part of it.

```
cd ~
git clone https://github.com/rkoshak/openhab-rules-tools.git
cp -r ~/openhab-rules-tools/rules_utils/automation /etc/openhab
git clone https://github.com/Michdo93/openHAB-Helper-Libraries-MQTT-Event-Bus.git
cp -r ~/openHAB-Helper-Libraries-MQTT-Event-Bus/mqtt_eb/automation /etc/openhab
sudo chmod -R 777 /etc/openhab/automation
sudo chown -R openhab:openhab /etc/openhab/automation
```

Please copy the configuration from `/etc/openhab/automation/lib/python/configuration.py.mqtt_eb-example` to `/etc/openhab/automation/lib/python/configuration.py` and adjust it accordingly.

You can have a look on the master/slave example!

Also you have to install the MQTT 3.x Binding. Go to `Settings --> Bindings --> + --> MQTT Binding --> Install`. After that you have to create a connection to the installed Mosquitto Broker with a `MQTT Broker Thing`. Go to `Things --> + --> MQTT Binding --> MQTT Broker`.

On the master you can set a configuration like the following:

![master_broker_config](https://raw.githubusercontent.com/Michdo93/openHAB-Helper-Libraries-MQTT-Event-Bus/main/master_broker_config.JPG)
![master_broker_config](https://raw.githubusercontent.com/Michdo93/openHAB-Helper-Libraries-MQTT-Event-Bus/main/master_broker_config2.JPG)
![master_broker_config](https://raw.githubusercontent.com/Michdo93/openHAB-Helper-Libraries-MQTT-Event-Bus/main/master_broker_config3.JPG)

On the slave you can set a configuration like this:

![slave_broker_config](https://raw.githubusercontent.com/Michdo93/openHAB-Helper-Libraries-MQTT-Event-Bus/main/slave_broker_config.JPG)
![slave_broker_config](https://raw.githubusercontent.com/Michdo93/openHAB-Helper-Libraries-MQTT-Event-Bus/main/slave_broker_config2.JPG)
![slave_broker_config](https://raw.githubusercontent.com/Michdo93/openHAB-Helper-Libraries-MQTT-Event-Bus/main/slave_broker_config3.JPG)

You have to make sure that the slave(s) uses the Hostname or IP from the master. In the given example you can see the IP address `192.168.0.74` for this.

At least this thing should contain a `Triggering Channel`. The master should have a `Triggering Channel` which should be triggered if the slave send out `commands` and the slave(s) should have a `Triggering Channel` which should be triggered if the master send out `states`.

In the next step you go to `Things` and click on the created thing from the steps above. There you have to go to the tab `Channels` and click on `Add Channel` to create a `Triggering Channel`.

On the master it could look like this:

![master_trigger_channel](https://raw.githubusercontent.com/Michdo93/openHAB-Helper-Libraries-MQTT-Event-Bus/main/master_trigger_channel.JPG)

On the slave it could look like this:

![slave_trigger_channel](https://raw.githubusercontent.com/Michdo93/openHAB-Helper-Libraries-MQTT-Event-Bus/main/slave_trigger_channel.JPG)

Please make sure that the configuration.py uses the `Thing Identifier` as parameter for `mqtt_eb_broker` and the `Channel Identifier` as parameter for `mqtt_eb_in_chan`!

### Restart openHAB

#### Restart openHAB 2.x

To make the changes usable, the openHAB system must be restarted.

```
sudo systemctl stop openhab2
sudo rm -r /var/lib/openhab2/cache/*
sudo rm -r /var/lib/openhab2/tmp/*
sudo systemctl start openhab2
```

#### Restart openHAB 3.x

To make the changes usable, the openHAB system must be restarted.

```
sudo systemctl stop openhab
sudo rm -r /var/lib/openhab/cache/*
sudo rm -r /var/lib/openhab/tmp/*
sudo systemctl start openhab
```

### Set the Debug Level for the Scripting automation

Please make sure that you connect to the karaf console with `ssh -p 8101 openhab@localhost`. The standard password should be `habopen`.

You have to enter following two commands inside the karaf console:

```
log:set DEBUG org.openhab.core.automation
log:set DEBUG jsr223
```

If you run `log:tail` you should see all DEBUG informations from the Scripted Automation. If you have installed the `Jython Hello World example` you should also see this in the logging.







## Master / Slave example

Please make sure that the slave(s) will be connected to the master's mosquitto broker!

### Usage

You have to make sure that the item names on the master and on the slave(s) are equal. The master should contain all items from all slaves. But not all slaves should contain all items from the master. This means that the slaves can have different items with different names. Also the slaves could have only a few items from the master. This can be thought of as a restricted user who only has access to a few items. For example, that a slave is in the bathroom and the openHAB instance in the bathroom then only allows the items in the bathroom to be operated. The master/slave principle can only subscribe where the corresponding item is present. Otherwise it will be published, but a slave or even none of the slaves will access this topic. Conversely, the master should be able to subscribe to everything that the slaves publish.

### Configuration example 1

On the master you can create a configuration like this:

```
# The name to use for this instance of openHAB, forms the root of the MQTT topic
# hierarchy.
mqtt_eb_name = "Master"

# Thing ID for the MQTT broker Thing.
mqtt_eb_broker = "mqtt:broker:mqttbroker"

# The Channel ID of the MQTT Event Bus subscription channel
mqtt_eb_in_chan = "mqtt:broker:mqttbroker:commandUpdates"

statePublishTopic = "/messages/states/${item}"
commandPublishTopic = ""
stateSubscribeTopic = ""
commandSubscribeTopic = "/messages/commands/${item}"
```

and on the slave like this:

```
# The name to use for this instance of openHAB, forms the root of the MQTT topic
# hierarchy.
mqtt_eb_name = "Slave"

# Thing ID for the MQTT broker Thing.
mqtt_eb_broker = "mqtt:broker:mqttbroker"

# The Channel ID of the MQTT Event Bus subscription channel
mqtt_eb_in_chan = "mqtt:broker:mqttbroker:stateUpdates"

statePublishTopic = ""
commandPublishTopic = "/messages/commands/${item}"
stateSubscribeTopic = "/messages/states/${item}"
commandSubscribeTopic = ""
```

Or you can copy it from the `configuration.py.mqtt_eb-master1` or from the `configuration.py.mqtt_eb-slave1` to the `configuration.py` file.

### Configuration example 2

On the master you can create a configuration like this:

```
# The name to use for this instance of openHAB, forms the root of the MQTT topic
# hierarchy.
mqtt_eb_name = "Master"

# Thing ID for the MQTT broker Thing.
mqtt_eb_broker = "mqtt:broker:mqttbroker"

# The Channel ID of the MQTT Event Bus subscription channel
mqtt_eb_in_chan = "mqtt:broker:mqttbroker:commandUpdates"

statePublishTopic = "openHAB/in/${item}/state"
commandPublishTopic = ""
stateSubscribeTopic = ""
commandSubscribeTopic = "openHAB/out/${item}/command"
```

and on the slave like this:

```
# The name to use for this instance of openHAB, forms the root of the MQTT topic
# hierarchy.
mqtt_eb_name = "Slave"

# Thing ID for the MQTT broker Thing.
mqtt_eb_broker = "mqtt:broker:mqttbroker"

# The Channel ID of the MQTT Event Bus subscription channel
mqtt_eb_in_chan = "mqtt:broker:mqttbroker:stateUpdates"

statePublishTopic = ""
commandPublishTopic = "openHAB/out/${item}/command"
stateSubscribeTopic = "openHAB/in/${item}/state"
commandSubscribeTopic = ""
```

Or you can copy it from the `configuration.py.mqtt_eb-master2` or from the `configuration.py.mqtt_eb-slave2` to the `configuration.py` file.

### Proof of concept

#### Check the master logging

The logs on the master could look like this:

```
11:04:30.935 [DEBUG] [re.automation.internal.RuleEngineImpl] - The rule '1b0b9317-db90-4f06-b9c7-6b00c255b72d' is executed.
11:04:40.427 [INFO ] [openhab.event.ItemCommandEvent       ] - Item 'testSwitch' received command ON
11:04:40.436 [DEBUG] [re.automation.internal.RuleEngineImpl] - The trigger 'Item-testSwitch-received-update_f7cbf540722811ec8814b827eba9d5bf_f7cc435e722811ecbbc4b827eba9d5bf' of rule 'aca0842d-2567-4835-b02c-3aa02f14b96a' is triggered.
11:04:40.441 [INFO ] [jsr223.jython.MQTT Event Bus         ] - Using event bus name of Master
11:04:40.443 [INFO ] [openhab.event.ItemStateChangedEvent  ] - Item 'testSwitch' changed from OFF to ON
11:04:40.458 [INFO ] [jsr223.jython.MQTT Event Bus         ] - Using statePublishTopic /messages/states/${item}
11:04:40.463 [INFO ] [jsr223.jython.MQTT Event Bus         ] - Using commandPublishTopic
11:04:40.468 [INFO ] [jsr223.jython.MQTT Event Bus         ] - Using stateSubscribeTopic
11:04:40.473 [INFO ] [jsr223.jython.MQTT Event Bus         ] - Using commandSubscribeTopic /messages/commands/${item}
11:04:40.478 [INFO ] [jsr223.jython.mqtt_eb                ] - Publishing ON to  /messages/states/testSwitch on mqtt:broker:mqttbroker with retained 1
11:04:40.484 [DEBUG] [re.automation.internal.RuleEngineImpl] - The rule 'aca0842d-2567-4835-b02c-3aa02f14b96a' is executed.
11:04:40.927 [DEBUG] [re.automation.internal.RuleEngineImpl] - The trigger 'Time_cron_0_10_99df2880722811ec951cb827eba9d5bf_9a85a1b0722811ec9252b827eba9d5bf' of rule '1b0b9317-db90-4f06-b9c7-6b00c255b72d' is triggered.
11:04:40.932 [INFO ] [.Jython Hello World (cron decorators)] - Hello World!
11:04:40.937 [DEBUG] [re.automation.internal.RuleEngineImpl] - The rule '1b0b9317-db90-4f06-b9c7-6b00c255b72d' is executed.
11:04:44.282 [INFO ] [openhab.event.ChannelTriggeredEvent  ] - mqtt:broker:mqttbroker:commandUpdates triggered /messages/commands/testSwitch#OFF
11:04:44.286 [DEBUG] [re.automation.internal.RuleEngineImpl] - The trigger 'Channel_mqtt_broker_mqttbroker_commandUpdates_triggered_f851ee1e722811eca8a8b827eba9d5bf_f852634f722811ec8b81b827eba9d5bf' of rule '34ec96f1-c16b-4b1e-8c51-11be573a252c' is triggered.
11:04:44.294 [INFO ] [23.jython.MQTT Event Bus Subscription] - Subscribing /messages/commands/testSwitch with state  /messages/commands/testSwitch
11:04:44.300 [INFO ] [23.jython.MQTT Event Bus Subscription] - Event type command for item testSwitch
11:04:44.308 [DEBUG] [23.jython.MQTT Event Bus Subscription] - Received command OFF for Item testSwitch
11:04:44.312 [DEBUG] [re.automation.internal.RuleEngineImpl] - The rule '34ec96f1-c16b-4b1e-8c51-11be573a252c' is executed.
11:04:44.313 [INFO ] [openhab.event.ItemCommandEvent       ] - Item 'testSwitch' received command OFF
11:04:44.318 [DEBUG] [re.automation.internal.RuleEngineImpl] - The trigger 'Item-testSwitch-received-update_f7cbf540722811ec8814b827eba9d5bf_f7cc435e722811ecbbc4b827eba9d5bf' of rule 'aca0842d-2567-4835-b02c-3aa02f14b96a' is triggered.
11:04:44.323 [INFO ] [openhab.event.ItemStateChangedEvent  ] - Item 'testSwitch' changed from ON to OFF
11:04:44.324 [INFO ] [jsr223.jython.MQTT Event Bus         ] - Using event bus name of Master
11:04:44.329 [INFO ] [jsr223.jython.MQTT Event Bus         ] - Using statePublishTopic /messages/states/${item}
11:04:44.335 [INFO ] [jsr223.jython.MQTT Event Bus         ] - Using commandPublishTopic
11:04:44.340 [INFO ] [jsr223.jython.MQTT Event Bus         ] - Using stateSubscribeTopic
11:04:44.345 [INFO ] [jsr223.jython.MQTT Event Bus         ] - Using commandSubscribeTopic /messages/commands/${item}
11:04:44.351 [INFO ] [jsr223.jython.mqtt_eb                ] - Publishing OFF to  /messages/states/testSwitch on mqtt:broker:mqttbroker with retained 1
11:04:44.355 [DEBUG] [re.automation.internal.RuleEngineImpl] - The rule 'aca0842d-2567-4835-b02c-3aa02f14b96a' is executed.
11:04:48.556 [INFO ] [openhab.event.ChannelTriggeredEvent  ] - mqtt:broker:mqttbroker:commandUpdates triggered /messages/commands/testSwitch#ON
11:04:48.561 [DEBUG] [re.automation.internal.RuleEngineImpl] - The trigger 'Channel_mqtt_broker_mqttbroker_commandUpdates_triggered_f851ee1e722811eca8a8b827eba9d5bf_f852634f722811ec8b81b827eba9d5bf' of rule '34ec96f1-c16b-4b1e-8c51-11be573a252c' is triggered.
11:04:48.567 [INFO ] [23.jython.MQTT Event Bus Subscription] - Subscribing /messages/commands/testSwitch with state  /messages/commands/testSwitch
11:04:48.575 [INFO ] [23.jython.MQTT Event Bus Subscription] - Event type command for item testSwitch
11:04:48.581 [DEBUG] [23.jython.MQTT Event Bus Subscription] - Received command ON for Item testSwitch
11:04:48.585 [DEBUG] [re.automation.internal.RuleEngineImpl] - The rule '34ec96f1-c16b-4b1e-8c51-11be573a252c' is executed.
11:04:48.586 [INFO ] [openhab.event.ItemCommandEvent       ] - Item 'testSwitch' received command ON
11:04:48.591 [DEBUG] [re.automation.internal.RuleEngineImpl] - The trigger 'Item-testSwitch-received-update_f7cbf540722811ec8814b827eba9d5bf_f7cc435e722811ecbbc4b827eba9d5bf' of rule 'aca0842d-2567-4835-b02c-3aa02f14b96a' is triggered.
11:04:48.596 [INFO ] [openhab.event.ItemStateChangedEvent  ] - Item 'testSwitch' changed from OFF to ON
11:04:48.596 [INFO ] [jsr223.jython.MQTT Event Bus         ] - Using event bus name of Master
11:04:48.603 [INFO ] [jsr223.jython.MQTT Event Bus         ] - Using statePublishTopic /messages/states/${item}
11:04:48.608 [INFO ] [jsr223.jython.MQTT Event Bus         ] - Using commandPublishTopic
11:04:48.613 [INFO ] [jsr223.jython.MQTT Event Bus         ] - Using stateSubscribeTopic
11:04:48.618 [INFO ] [jsr223.jython.MQTT Event Bus         ] - Using commandSubscribeTopic /messages/commands/${item}
11:04:48.623 [INFO ] [jsr223.jython.mqtt_eb                ] - Publishing ON to  /messages/states/testSwitch on mqtt:broker:mqttbroker with retained 1
11:04:48.627 [DEBUG] [re.automation.internal.RuleEngineImpl] - The rule 'aca0842d-2567-4835-b02c-3aa02f14b96a' is executed.
11:04:50.928 [DEBUG] [re.automation.internal.RuleEngineImpl] - The trigger 'Time_cron_0_10_99df2880722811ec951cb827eba9d5bf_9a85a1b0722811ec9252b827eba9d5bf' of rule '1b0b9317-db90-4f06-b9c7-6b00c255b72d' is triggered.
11:04:50.932 [INFO ] [.Jython Hello World (cron decorators)] - Hello World!
11:04:50.937 [DEBUG] [re.automation.internal.RuleEngineImpl] - The rule '1b0b9317-db90-4f06-b9c7-6b00c255b72d' is executed.
11:04:53.014 [INFO ] [openhab.event.ItemCommandEvent       ] - Item 'testSwitch' received command OFF
11:04:53.019 [DEBUG] [re.automation.internal.RuleEngineImpl] - The trigger 'Item-testSwitch-received-update_f7cbf540722811ec8814b827eba9d5bf_f7cc435e722811ecbbc4b827eba9d5bf' of rule 'aca0842d-2567-4835-b02c-3aa02f14b96a' is triggered.
11:04:53.024 [INFO ] [jsr223.jython.MQTT Event Bus         ] - Using event bus name of Master
11:04:53.024 [INFO ] [openhab.event.ItemStateChangedEvent  ] - Item 'testSwitch' changed from ON to OFF
11:04:53.031 [INFO ] [jsr223.jython.MQTT Event Bus         ] - Using statePublishTopic /messages/states/${item}
11:04:53.036 [INFO ] [jsr223.jython.MQTT Event Bus         ] - Using commandPublishTopic
11:04:53.041 [INFO ] [jsr223.jython.MQTT Event Bus         ] - Using stateSubscribeTopic
11:04:53.046 [INFO ] [jsr223.jython.MQTT Event Bus         ] - Using commandSubscribeTopic /messages/commands/${item}
11:04:53.051 [INFO ] [jsr223.jython.mqtt_eb                ] - Publishing OFF to  /messages/states/testSwitch on mqtt:broker:mqttbroker with retained 1
11:04:53.055 [DEBUG] [re.automation.internal.RuleEngineImpl] - The rule 'aca0842d-2567-4835-b02c-3aa02f14b96a' is executed.
```

#### Check the slave logging

The logs on the slave(s) could look like this:

```
11:02:40.429 [DEBUG] [re.automation.internal.RuleEngineImpl] - The rule '18334321-f767-4c9b-8846-80068e92e8f1' is executed.
11:02:48.271 [DEBUG] [re.automation.internal.RuleEngineImpl] - The trigger 'Channel_mqtt_broker_mqttbroker_stateUpdates_triggered_e572469e722911ecaa62b827eb8adac3_e5a1e21e722911ecb94eb827eb8adac3' of rule '3221aaa7-9b2c-481e-ba9b-d8f4c012d716' is triggered.
11:02:48.277 [INFO ] [openhab.event.ChannelTriggeredEvent  ] - mqtt:broker:mqttbroker:stateUpdates triggered /messages/states/testSwitch#ON
11:02:48.278 [INFO ] [23.jython.MQTT Event Bus Subscription] - Subscribing /messages/states/testSwitch with state  /messages/states/testSwitch
11:02:48.289 [INFO ] [23.jython.MQTT Event Bus Subscription] - Event type state for item  testSwitch
11:02:48.294 [DEBUG] [23.jython.MQTT Event Bus Subscription] - Received update ON for Item testSwitch
11:02:48.298 [DEBUG] [re.automation.internal.RuleEngineImpl] - The rule '3221aaa7-9b2c-481e-ba9b-d8f4c012d716' is executed.
11:02:48.303 [INFO ] [openhab.event.ItemStateChangedEvent  ] - Item 'testSwitch' changed from OFF to ON
11:02:50.418 [DEBUG] [re.automation.internal.RuleEngineImpl] - The trigger 'Time_cron_0_10_de6eed40722911ecb871b827eb8adac3_df0b7b5e722911ecbc6eb827eb8adac3' of rule '18334321-f767-4c9b-8846-80068e92e8f1' is triggered.
11:02:50.423 [INFO ] [.Jython Hello World (cron decorators)] - Hello World!
11:02:50.428 [DEBUG] [re.automation.internal.RuleEngineImpl] - The rule '18334321-f767-4c9b-8846-80068e92e8f1' is executed.
11:02:52.013 [INFO ] [openhab.event.ItemCommandEvent       ] - Item 'testSwitch' received command OFF
11:02:52.017 [DEBUG] [re.automation.internal.RuleEngineImpl] - The trigger 'Item-testSwitch-received-command_e49db88f722911ecb48fb827eb8adac3_e49e06ae722911ecb01eb827eb8adac3' of rule 'afacc4e6-80aa-4bd1-b757-23d8ae243e77' is triggered.
11:02:52.023 [INFO ] [jsr223.jython.MQTT Event Bus         ] - Using event bus name of Slave
11:02:52.029 [INFO ] [openhab.event.ItemStateChangedEvent  ] - Item 'testSwitch' changed from ON to OFF
11:02:52.034 [INFO ] [jsr223.jython.MQTT Event Bus         ] - Using statePublishTopic
11:02:52.039 [INFO ] [jsr223.jython.MQTT Event Bus         ] - Using commandPublishTopic /messages/commands/${item}
11:02:52.044 [INFO ] [jsr223.jython.MQTT Event Bus         ] - Using stateSubscribeTopic /messages/states/${item}
11:02:52.050 [INFO ] [jsr223.jython.MQTT Event Bus         ] - Using commandSubscribeTopic
11:02:52.055 [INFO ] [jsr223.jython.mqtt_eb                ] - Publishing OFF to  /messages/commands/testSwitch on mqtt:broker:mqttbroker with retained 0
11:02:52.060 [DEBUG] [re.automation.internal.RuleEngineImpl] - The rule 'afacc4e6-80aa-4bd1-b757-23d8ae243e77' is executed.
11:02:52.144 [DEBUG] [re.automation.internal.RuleEngineImpl] - The trigger 'Channel_mqtt_broker_mqttbroker_stateUpdates_triggered_e572469e722911ecaa62b827eb8adac3_e5a1e21e722911ecb94eb827eb8adac3' of rule '3221aaa7-9b2c-481e-ba9b-d8f4c012d716' is triggered.
11:02:52.150 [INFO ] [openhab.event.ChannelTriggeredEvent  ] - mqtt:broker:mqttbroker:stateUpdates triggered /messages/states/testSwitch#OFF
11:02:52.150 [INFO ] [23.jython.MQTT Event Bus Subscription] - Subscribing /messages/states/testSwitch with state  /messages/states/testSwitch
11:02:52.163 [INFO ] [23.jython.MQTT Event Bus Subscription] - Event type state for item  testSwitch
11:02:52.170 [DEBUG] [23.jython.MQTT Event Bus Subscription] - Received update OFF for Item testSwitch
11:02:52.173 [DEBUG] [re.automation.internal.RuleEngineImpl] - The rule '3221aaa7-9b2c-481e-ba9b-d8f4c012d716' is executed.
11:02:56.290 [INFO ] [openhab.event.ItemCommandEvent       ] - Item 'testSwitch' received command ON
11:02:56.296 [DEBUG] [re.automation.internal.RuleEngineImpl] - The trigger 'Item-testSwitch-received-command_e49db88f722911ecb48fb827eb8adac3_e49e06ae722911ecb01eb827eb8adac3' of rule 'afacc4e6-80aa-4bd1-b757-23d8ae243e77' is triggered.
11:02:56.299 [INFO ] [jsr223.jython.MQTT Event Bus         ] - Using event bus name of Slave
11:02:56.306 [INFO ] [openhab.event.ItemStateChangedEvent  ] - Item 'testSwitch' changed from OFF to ON
11:02:56.307 [INFO ] [jsr223.jython.MQTT Event Bus         ] - Using statePublishTopic
11:02:56.314 [INFO ] [jsr223.jython.MQTT Event Bus         ] - Using commandPublishTopic /messages/commands/${item}
11:02:56.320 [INFO ] [jsr223.jython.MQTT Event Bus         ] - Using stateSubscribeTopic /messages/states/${item}
11:02:56.325 [INFO ] [jsr223.jython.MQTT Event Bus         ] - Using commandSubscribeTopic
11:02:56.330 [INFO ] [jsr223.jython.mqtt_eb                ] - Publishing ON to  /messages/commands/testSwitch on mqtt:broker:mqttbroker with retained 0
11:02:56.334 [DEBUG] [re.automation.internal.RuleEngineImpl] - The rule 'afacc4e6-80aa-4bd1-b757-23d8ae243e77' is executed.
11:02:56.414 [DEBUG] [re.automation.internal.RuleEngineImpl] - The trigger 'Channel_mqtt_broker_mqttbroker_stateUpdates_triggered_e572469e722911ecaa62b827eb8adac3_e5a1e21e722911ecb94eb827eb8adac3' of rule '3221aaa7-9b2c-481e-ba9b-d8f4c012d716' is triggered.
11:02:56.419 [INFO ] [openhab.event.ChannelTriggeredEvent  ] - mqtt:broker:mqttbroker:stateUpdates triggered /messages/states/testSwitch#ON
11:02:56.420 [INFO ] [23.jython.MQTT Event Bus Subscription] - Subscribing /messages/states/testSwitch with state  /messages/states/testSwitch
11:02:56.430 [INFO ] [23.jython.MQTT Event Bus Subscription] - Event type state for item  testSwitch
11:02:56.438 [DEBUG] [23.jython.MQTT Event Bus Subscription] - Received update ON for Item testSwitch
11:02:56.441 [DEBUG] [re.automation.internal.RuleEngineImpl] - The rule '3221aaa7-9b2c-481e-ba9b-d8f4c012d716' is executed.
11:03:00.418 [DEBUG] [re.automation.internal.RuleEngineImpl] - The trigger 'Time_cron_0_10_de6eed40722911ecb871b827eb8adac3_df0b7b5e722911ecbc6eb827eb8adac3' of rule '18334321-f767-4c9b-8846-80068e92e8f1' is triggered.
11:03:00.423 [INFO ] [.Jython Hello World (cron decorators)] - Hello World!
11:03:00.428 [DEBUG] [re.automation.internal.RuleEngineImpl] - The rule '18334321-f767-4c9b-8846-80068e92e8f1' is executed.
11:03:00.843 [DEBUG] [re.automation.internal.RuleEngineImpl] - The trigger 'Channel_mqtt_broker_mqttbroker_stateUpdates_triggered_e572469e722911ecaa62b827eb8adac3_e5a1e21e722911ecb94eb827eb8adac3' of rule '3221aaa7-9b2c-481e-ba9b-d8f4c012d716' is triggered.
11:03:00.848 [INFO ] [openhab.event.ChannelTriggeredEvent  ] - mqtt:broker:mqttbroker:stateUpdates triggered /messages/states/testSwitch#OFF
11:03:00.850 [INFO ] [23.jython.MQTT Event Bus Subscription] - Subscribing /messages/states/testSwitch with state  /messages/states/testSwitch
11:03:00.857 [INFO ] [23.jython.MQTT Event Bus Subscription] - Event type state for item  testSwitch
11:03:00.863 [DEBUG] [23.jython.MQTT Event Bus Subscription] - Received update OFF for Item testSwitch
11:03:00.867 [DEBUG] [re.automation.internal.RuleEngineImpl] - The rule '3221aaa7-9b2c-481e-ba9b-d8f4c012d716' is executed.
11:03:00.873 [INFO ] [openhab.event.ItemStateChangedEvent  ] - Item 'testSwitch' changed from ON to OFF
```
