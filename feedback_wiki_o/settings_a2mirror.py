"""  __      __    __               ___
    /  \    /  \__|  | _ __        /   \
    \   \/\/   /  |  |/ /  |  __  |  |  |
     \        /|  |    <|  | |__| |  |  |
      \__/\__/ |__|__|__\__|       \___/

A web service for sharing opinions and avoiding arguments

@file       feedback_wiki_o/settings_a2mirror.py
@brief      The private server file for Django
@copyright  GNU Public License, 2018
@authors    Frank Imeson
"""

from .settings_base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['www.feedback.wiki-x.com', 'feedback.wiki-x.com', '162.249.2.136']
