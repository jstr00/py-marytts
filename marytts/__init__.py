#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2017 Guenter Bartsch
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#
# A simple MARY TTS client in Python
#
# based on Code from Hugh Sasse (maryclient-http.py)
#

import httplib, urllib

import sys
import re 
import traceback
import logging

import xml.etree.ElementTree as ET

def _compress_ws (s):

    vc = True

    res = ''

    for c in s:

        if c == ' ':
            vc = False
        else:
            if vc:
                res = res + c
            else:
                res = res + ' ' + c
            vc = True

    return res 


class MaryTTS(object):

    def __init__(self, 
                 host   = "127.0.0.1",
                 port   = 59125,
                 locale = "en_US",
                 voice  = "cmu-rms-hsmm"):

        self.input_type   = "TEXT"
        self.output_type  = "AUDIO"
        self.audio        = "WAVE_FILE"

        self._host        = host
        self._port        = port
        self._locale      = locale
        self._voice       = voice

    def _generate(self, message):
        """Given a message in message,
           return a response in the appropriate
           format."""
        raw_params = {"INPUT_TEXT"  : message.encode('UTF8'),
                      "INPUT_TYPE"  : self.input_type,
                      "OUTPUT_TYPE" : self.output_type,
                      "LOCALE"      : self._locale,
                      "AUDIO"       : self.audio,
                      "VOICE"       : self._voice,
                      }
        params = urllib.urlencode(raw_params)
        headers = {}

        logging.debug('maryclient: generate, raw_params=%s' % repr(raw_params))

        # Open connection to self._host, self._port.
        conn = httplib.HTTPConnection(self._host, self._port)

        #conn.set_debuglevel(5)
        
        conn.request("POST", "/process", params, headers)
        response = conn.getresponse()
        if response.status != 200:
            logging.error(response.getheaders())
            raise Exception ("{0}: {1}".format(response.status, response.reason))
        return response.read()

    def _mary_gather_ph (self, parent):

        res = ""

        for child in parent:
            r = self._mary_gather_ph (child)
            if len(r) > 0:
                res += r + " "

        if 'ph' in parent.attrib:
            res += parent.attrib['ph'] + " "

        return _compress_ws(res)

    def g2p(self, word):

        self.input_type  = "TEXT"
        self.output_type = "PHONEMES"

        xmls = self._generate(word.lower())

        #print "Got: For %s %s" % (graph.encode('utf-8'), xmls)

        root = ET.fromstring(xmls)

        #print "ROOT: %s" % repr(root)

        mph = self._mary_gather_ph (root)

        return re.sub(u"^ \?", "", re.sub(u"^ ' \?", "'", mph))

    def synth_wav(self, txt, fmt='txt'):

        if fmt == 'txt':
            phonemes = self.g2p(txt)
        elif fmt == 'xs':
            phonemes = txt
        else:
            raise Exception ('unknown format: %s' % fmt)

        wav = None

        try:
            s = '<maryxml xmlns="http://mary.dfki.de/2002/MaryXML" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="0.5" xml:lang="%s"><p><s><t g2p_method="lexicon" ph="%s" pos="NE"></t></s></p></maryxml>' % (self.locale[:2], phonemes)

            self.input_type  = "PHONEMES"
            self.output_type = "AUDIO"
            wav = self._generate(s)

        except:
            logging.error("*** ERROR: unexpected error: %s " % sys.exc_info()[0])
            traceback.print_exc()

        return wav

    @property
    def voices(self):

        raw_params = { }
        params = urllib.urlencode(raw_params)
        headers = {}

        logging.debug('maryclient: voices, raw_params=%s' % repr(raw_params))

        # Open connection to self._host, self._port.
        conn = httplib.HTTPConnection(self._host, self._port)

        #conn.set_debuglevel(5)
        
        conn.request("GET", "/voices", params, headers)
        response = conn.getresponse()
        if response.status != 200:
            logging.error(response.getheaders())
            raise Exception ("{0}: {1}".format(response.status, response.reason))
        res = response.read()

        voices = []
        for line in res.split('\n'):
            voices.append(line.split(' '))

        logging.debug('maryclient: voices=%s' % repr(voices))

        return voices

    @property
    def host(self):
        return self._host
    @host.setter
    def host(self, v):
        self._host = v

    @property
    def port(self):
        return self._port  
    @port.setter
    def port(self, v):
        self._port   = v

    @property
    def locale(self):
        return self._locale
    @locale.setter
    def locale(self, v):
        self._locale    = v

    @property
    def voice(self):
        return self._voice
    @voice.setter
    def voice(self, v):
        self._voice    = v
