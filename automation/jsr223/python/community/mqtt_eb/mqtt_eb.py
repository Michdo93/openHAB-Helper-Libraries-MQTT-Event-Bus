"""
Copyright July 10, 2020 Richard Koshak

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from core.log import logging, LOG_PREFIX, log_traceback
from community.rules_utils import create_simple_rule, delete_rule, create_rule

init_logger = logging.getLogger("{}.mqtt_eb".format(LOG_PREFIX))


@log_traceback
def check_config(log):
    """Verifies that all the settings exist and are usable."""

    try:
        from configuration import mqtt_eb_name
        log.info("Using event bus name of {}".format(mqtt_eb_name))
    except:
        log.error("mqtt_eb_name is not defined in configuration.py!")
        return False

    broker = None
    try:
        from configuration import mqtt_eb_broker
        broker = mqtt_eb_broker
    except:
        log.error("mqtt_eb_broker is not defined in configuration.py!")
        return False

    if not actions.get("mqtt", broker):
        log.error("{} is not a valid broker Thing ID".format(broker))
        return False

    try:
        from configuration import statePublishTopic
        log.info("Using statePublishTopic {}".format(statePublishTopic))
    except:
        log.error(
            "statePublishTopic should be defined or empty in configuration.py!")

    try:
        from configuration import commandPublishTopic
        log.info("Using commandPublishTopic {}".format(commandPublishTopic))
    except:
        log.error(
            "commandPublishTopic should be defined or empty in configuration.py!")

    try:
        from configuration import stateSubscribeTopic
        log.info("Using stateSubscribeTopic {}".format(stateSubscribeTopic))
    except:
        log.error(
            "stateSubscribeTopic should be defined or empty in configuration.py!")

    try:
        from configuration import commandSubscribeTopic
        log.info("Using commandSubscribeTopic {}".format(commandSubscribeTopic))
    except:
        log.error(
            "commandSubscribeTopic should be defined or empty in configuration.py!")

    return True


@log_traceback
def mqtt_eb_pub(event):
    """Called when a configured Item is updated or commanded and publsihes the
    event to the event bus.
    """

    if not check_config(mqtt_eb_pub.log):
        init_logger.error("Cannot publish event bus event, deleting rule")
        delete_rule(mqtt_eb_pub, init_logger)
        return

    from configuration import mqtt_eb_broker, statePublishTopic, commandPublishTopic

    is_cmd = hasattr(event, 'itemCommand')
    msg = "{}".format(event.itemCommand if is_cmd else event.itemState)

    if is_cmd and commandPublishTopic != '':
        topic = commandPublishTopic.replace("${item}", event.itemName)

    if not is_cmd and statePublishTopic != '':
        topic = statePublishTopic.replace("${item}", event.itemName)

    retained = False if is_cmd else True
    init_logger.info("Publishing {} to  {} on {} with retained {}"
                     .format(msg, topic, mqtt_eb_broker, retained))
    action = actions.get("mqtt", mqtt_eb_broker)
    if action:
        action.publishMQTT(topic, msg, retained)
    else:
        init_logger.error(
            "There is no broker Thing {}!".format(mqtt_eb_broker))


@log_traceback
def load_publisher():

    # Delete the old publisher rule.
    if not delete_rule(mqtt_eb_pub, init_logger):
        init_logger("Failed to delete rule!")
        return False

    # Don't bother to create the rule if we can't use it.
    if not check_config(init_logger):
        init_logger.error("Cannot create MQTT event bus publication rule!")
        return False

    state_publish_topic = ""
    try:
        from configuration import statePublishTopic
        state_publish_topic = statePublishTopic
    except:
        init_logger.warn(
            "No statePublishTopic in configuration.py, statePublishTopic should be defined or empty in configuration.py!")

    command_publish_topic = ""
    try:
        from configuration import commandPublishTopic
        command_publish_topic = commandPublishTopic
    except:
        init_logger.warn(
            "No commandPublishTopic in configuration.py, commandPublishTopic should be defined or empty in configuration.py!")

    triggers = []

    # Create triggers for Items.
    for i in items:
        if state_publish_topic != '':
            triggers.append("Item {} received update".format(i))
        if command_publish_topic != '':
            triggers.append("Item {} received command".format(i))

    # No triggers, no need for the rule.
    if not triggers:
        init_logger.warn("No event bus Items found")
        return False

    # Create the rule to publish the events.
    if not create_rule("MQTT Event Bus", triggers, mqtt_eb_pub,
                       init_logger,
                       description=("Publishes updates and commands on "
                                    "configured Items to the configured "
                                    "event bus topics"),
                       tags=["openhab-rules-tools", "mqtt_eb"]):
        init_logger.error("Failed to create MQTT Event Bus Publisher!")
        return False

    return True


@log_traceback
def mqtt_eb_sub(event):
    """Called when a new message is received on the event bus subscription.
    Splits the topic from the state using "#" and extracts the item and event
    type from the topic.

    Any message for an Item that doesn't exist generates a debug message in the
    log.
    """

    state_subscribe_topic = ""
    try:
        from configuration import stateSubscribeTopic
        state_publish_topic = stateSubscribeTopic
    except:
        mqtt_eb_sub.log.warn(
            "No stateSubscribeTopic in configuration.py, stateSubscribeTopic should be defined or empty in configuration.py!")

    command_subscribe_topic = ""
    try:
        from configuration import commandSubscribeTopic
        command_subscribe_topic = commandSubscribeTopic
    except:
        mqtt_eb_sub.log.warn(
            "No commandSubscribeTopic in configuration.py, commandSubscribeTopic should be defined or empty in configuration.py!")

    topic = event.event.split("#")[0]
    state = event.event.split("#")[1]

    mqtt_eb_sub.log.info("Subscribing {} with state  {}"
                         .format(topic, topic))

    if state_publish_topic != '':
        event_type = 'state'
        itemPosition = state_publish_topic.split("${item}")[0].count("/")

    if command_subscribe_topic != '':
        event_type = 'command'
        itemPosition = command_subscribe_topic.split("${item}")[0].count("/")

    item_name = topic.split("/")[itemPosition]

    mqtt_eb_sub.log.info("Event type {} for item {}"
                         .format(event_type, item_name))

    if item_name not in items:
        mqtt_eb_sub.log.debug("Local openHAB does not have Item {}, ignoring."
                              .format(item_name))
    elif event_type == "command":
        mqtt_eb_sub.log.debug("Received command {} for Item {}"
                              .format(state, item_name))
        events.sendCommand(item_name, state)
    else:
        mqtt_eb_sub.log.debug("Received update {} for Item {}"
                              .format(state, item_name))
        events.postUpdate(item_name, state)


@ log_traceback
def online(event):
    """Publishes ONLINE to mqtt_eb_name/status on System started."""

    init_logger.info("Reporting the event bus as ONLINE")
    from configuration import mqtt_eb_broker, mqtt_eb_name
    actions.get("mqtt", mqtt_eb_broker).publishMQTT("{}/status"
                                                    .format(mqtt_eb_name),
                                                    "ONLINE", True)


@ log_traceback
def load_online():
    """Loads the online status publishing rule."""

    # Delete the old online rule.
    if not delete_rule(online, init_logger):
        init_logger("Failed to delete rule!")
        return False

    triggers = ["System started"]

    if not create_rule("MQTT Event Bus Online", triggers, online, init_logger,
                       description=("Publishes ONLINE to the configured LWT "
                                    "topic."),
                       tags=["openhab-rules-tools", "mqtt_eb"]):
        init_logger.error("Failed to create MQTT Event Bus Online rule!")


@ log_traceback
def load_mqtt_eb(event):
    """Deletes and recreates the MQTT Event Bus publisher and online rules."""

    # Reload to get the latest config parameters.
    import configuration
    reload(configuration)

    if load_publisher():
        load_online()

    """Deletes and recreates the MQTT Event Bus subscription rule."""
    # Delete the old rule
    delete_rule(mqtt_eb_sub, init_logger)

    try:
        from configuration import stateSubscribeTopic
    except:
        load_mqtt_eb.log.warn(
            "No stateSubscribeTopic in configuration.py, stateSubscribeTopic should be defined or empty in configuration.py!")

    try:
        from configuration import commandSubscribeTopic
    except:
        load_mqtt_eb.log.warn(
            "No commandSubscribeTopic in configuration.py, commandSubscribeTopic should be defined or empty in configuration.py!")

    try:
        from configuration import mqtt_eb_in_chan
    except:
        load_mqtt_eb.log.error("mqtt_eb_in_chan is not defined in "
                               "configuration.py")
        return

    # Add the trigger
    triggers = ["Channel {} triggered".format(mqtt_eb_in_chan)]
    if not create_rule("MQTT Event Bus Subscription", triggers, mqtt_eb_sub,
                       load_mqtt_eb.log,
                       description=("Triggers by an MQTT event Channel and updates or "
                                    "commands based on the topic the message came from"),
                       tags=["openhab-rules-tools", "mqtt_eb"]):
        load_mqtt_eb.log.error(
            "Failed to create MQTT Event Bus Subscription!")


@ log_traceback
def scriptLoaded(*args):
    """Creates and then calls the Reload MQTT Event Bus Publisher rule."""

    if create_simple_rule("Reload_MQTT_EB",
                          "Reload MQTT Event Bus",
                          load_mqtt_eb, init_logger,
                          description=("Reload the MQTT Event Bus "
                                       "rule. Run when changing configuration.py"),
                          tags=["openhab-rules-tools", "mqtt_eb"]):
        load_mqtt_eb(None)


@ log_traceback
def scriptUnloaded():
    """Deletes the MQTT Event Bus Publisher and Online rules and the reload rule."""
    delete_rule(load_mqtt_eb, init_logger)
    delete_rule(mqtt_eb, init_logger)
    delete_rule(mqtt_eb_sub, init_logger)
