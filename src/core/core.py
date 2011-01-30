#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os, sys, smtplib
from datetime import date
from email.MIMEText import MIMEText

# Loggers de alto nivel
logger = logging.getLogger("BackupDar")