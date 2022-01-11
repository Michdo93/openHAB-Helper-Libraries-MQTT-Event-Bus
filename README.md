# openHAB-Helper-Libraries-MQTT-Event-Bus
A MQTT Event Bus for openHAB 2.x and 3.x using the [Helper Libraries for openHAB Scripted Automation](https://openhab-scripters.github.io/openhab-helper-libraries/index.html). Tested with openHAB 2.x and openHAB 3.x. This should work equivalent like the [Event bus binding](https://v2.openhab.org/addons/bindings/mqtt1/#event-bus-binding-configuration) from the old [MQTT 1.x binding](https://v2.openhab.org/addons/bindings/mqtt1/).

Description:
Publish/receive all states/commmands directly on the openHAB eventbus.

Usage:
Perfect for integrating multiple openHAB instances or broadcasting all events.

## Preparation

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
