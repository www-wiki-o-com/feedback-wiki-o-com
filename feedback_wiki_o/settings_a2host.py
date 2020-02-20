"""  __      __    __               ___
    /  \    /  \__|  | _ __        /   \
    \   \/\/   /  |  |/ /  |  __  |  |  |
     \        /|  |    <|  | |__| |  |  |
      \__/\__/ |__|__|__\__|       \___/

A web service for sharing opinions and avoiding arguments

@file       feedback_wiki_o/settings_a2host.py
@brief      The private server file for Django
@copyright  GNU Public License, 2018
@authors    Frank Imeson
"""

from .settings_base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['www.feedback.wiki-o.com', 'feedback.wiki-o.com', '75.98.169.10']
