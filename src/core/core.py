#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os, sys, smtplib
from datetime import date
from email.MIMEText import MIMEText
from email.Encoders import encode_base64