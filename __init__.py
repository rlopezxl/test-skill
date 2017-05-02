# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.


# Visit https://docs.mycroft.ai/skill.creation for more detailed information
# on the structure of this skill and its containing folder, as well as
# instructions for designing your own skill based on this template.


# Import statements: the list of outside modules you'll be using in your
# skills, whether from other files in mycroft-core or from external libraries
from os.path import dirname

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

import requests

__author__ = 'rlopezxl'

# Logger: used for debug lines, like "LOGGER.debug(xyz)". These
# statements will show up in the command line when running Mycroft.
LOGGER = getLogger(__name__)

# The logic of each skill is contained within its own class, which inherits
# base methods from the MycroftSkill class with the syntax you can see below:
# "class ____Skill(MycroftSkill)"
class TestyTestSkill(MycroftSkill):

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(TestyTestSkill, self).__init__(name="TestyTestSkill")
        self.gender = "male"
        self.name = "ruben"
        self.agi = "400,000"
        self.monthly = "3,500"

    # This method loads the files needed for the skill's functioning, and
    # creates and registers each intent that the skill uses
    def initialize(self):
        self.load_data_files(dirname(__file__))

        myself_intent = IntentBuilder("MyselfIntent").\
            require("Myself").build()
        self.register_intent(myself_intent, self.handle_myself_intent)

        service_call_intent = IntentBuilder("ServiceCallIntent").\
            require("ServiceCall").build()
        self.register_intent(service_call_intent, self.handle_service_call_intent)

        expense_intent = IntentBuilder("ExpenseIntent").\
            require("MonthlyExpense").optionally("Monthly").build()
        self.register_intent(expense_intent, self.handle_expense_intent)


    # The "handle_xxxx_intent" functions define Mycroft's behavior when
    # each of the skill's intents is triggered: in this case, he simply
    # speaks a response. Note that the "speak_dialog" method doesn't
    # actually speak the text it's passed--instead, that text is the filename
    # of a file in the dialog folder, and Mycroft speaks its contents when
    # the method is called.
    def handle_myself_intent(self, message):
        self.speak_dialog("myself")
        self.speak("Your name is " + self.name)
        self.speak("You make " + self.agi + " dollars a year.")
        self.speak("Your current monthly expenses are " + self.monthly)

    def handle_service_call_intent(self, message):
        self.speak_dialog("service.call")
        ip = requests.get("http://www.xldevelopment.net/ip.php")
        self.speak("Your I.P. is " + ip.text)

    def handle_expense_intent(self, message):
        amount = message.data.get("Amount")
        try:
            expense = int(amount)
            monthly = int(self.monthly)
            self.speak_dialog("expense", data={'amount': amount})
            self.speak("Your new monthly expense is " + str(monthly + expense))
        except Exception as e:
            self.speak_dialog("error", data={'amount': amount})
            LOGGER.error("Error: {0}".format(e))


    # The "stop" method defines what Mycroft does when told to stop during
    # the skill's execution. In this case, since the skill's functionality
    # is extremely simple, the method just contains the keyword "pass", which
    # does nothing.
    def stop(self):
        pass

# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return TestyTestSkill()
