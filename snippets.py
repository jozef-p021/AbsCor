# -*- coding: utf-8 -*-
import datetime
import json
from collections import OrderedDict
from xml.dom import Node

import numpy as np


def generate_photon_statistics(slitscan, xo=0, mirror=False):
    """
    this generates photon statistics based on slitscan stored in respective file
    """
    if mirror == True:
        sign = -1
    else:
        sign = 1
    data = np.loadtxt(slitscan, usecols=(0, 1), comments='#')
    x = sign * (data[:, 0] - xo)
    y = data[:, 1] - data[0, 1]
    dx = np.mean(np.diff(x))
    cdf = []
    sum = 0
    for i in range(len(x)):
        sum += dx * y[i]
        cdf.append(sum)

    # xo = dx*np.sum(x*y)/sum
    cdf = cdf / sum
    return x, cdf


def beam_path_within_sample(sam, xB, yB, zB, xD, yD, zD):
    """
    """
    ### path_in
    zA = sam.zs - sam.radius * np.sin(np.arccos((yB - sam.ys) / sam.radius))
    path_in = np.abs(zA - zB)
    ### path_out
    path_out = np.sqrt((xD - xB) ** 2 + (yD - yB) ** 2 + (zD - zB) ** 2)
    a = (yD - yB) ** 2 + (zD - zB) ** 2
    b = 2 * ((yB - sam.ys) * (yD - yB) + (zB - sam.zs) * (zD - zB))
    c = (yB - sam.ys) ** 2 + (zB - sam.zs) ** 2 - sam.radius ** 2
    pom = np.sqrt(b ** 2 - 4 * a * c) / (2 * a)
    k1 = -b / (2 * a) + pom
    # k2 = -b/(2*a) - pom
    [path_out] = np.abs(k1) * path_out
    return path_in + path_out

def getScaledTimeHumanReadable(seconds):
    if seconds < 0: return

    d = datetime.datetime(1, 1, 1) + datetime.timedelta(seconds=seconds)

    if seconds < 60:
        msec = int(d.microsecond / 1000)
        if msec > 0:
            humanReadableEstimate = "%d Sec %d MSec" % (d.second, msec)
        else:
            humanReadableEstimate = "%d Sec" % (d.second)
    elif 60 <= seconds < 3600:
        humanReadableEstimate = "%d Min %d Sec" % (d.minute, d.second)
    elif 3600 <= seconds < 24 * 3600:
        humanReadableEstimate = "%d Hour %d Min" % (d.hour, d.minute)
    elif 24 * 3600 <= seconds < 24 * 3600 * 28:
        humanReadableEstimate = "%d Day %d Hour %d Min" % (d.day - 1, d.hour, d.minute)
    elif 24 * 3600 * 28 <= seconds < 24 * 3600 * 28 * 12:
        humanReadableEstimate = "%d Month %d Day %d Hour" % (d.month, d.day - 1, d.hour)
    else:
        humanReadableEstimate = "%d Year %d Month %d Day" % (d.year, d.month, d.day - 1)

    return humanReadableEstimate


from xml.dom.minidom import Node, parse


def parseXMLTags(attributes, out=None, tagFilter=["attribute"], nodePairs=None, getAttributesInfo=False):
    if out is None: out = OrderedDict()
    for attribute in attributes:
        if attribute.nodeType == Node.COMMENT_NODE: continue
        tagName = attribute.tagName
        if tagName not in tagFilter: continue
        attributeName = attribute.getAttribute("name")
        attributeType = attribute.getAttribute("type").lower()
        attributeValue = attribute.firstChild
        if nodePairs is not None: nodePairs[attributeName] = attribute.firstChild

        if attributeValue is None:
            nodeType = None
        else:
            nodeType = attributeValue.nodeType

        if nodeType == Node.TEXT_NODE:
            attributeValue = attributeValue.nodeValue
            if attributeValue == "None":
                attributeValue = None
            elif attributeType in ("int", "integer"):
                attributeValue = int(attributeValue)
            elif attributeType in ("float", "decimal"):
                attributeValue = float(attributeValue)
            elif attributeType in ("bool", "boolean"):
                if attributeValue in ("False", 0):
                    attributeValue = False
                else:
                    attributeValue = True
            elif attributeType == "json":
                attributeValue = json.loads(attributeValue)
            else:
                if attributeValue == "None":
                    attributeValue = None
                else:
                    attributeValue = unicode(attributeValue)


            out[attributeName] = attributeValue
        elif nodeType == Node.ELEMENT_NODE:
            out[attributeName] = parseXMLTags(attribute.childNodes, tagFilter=tagFilter,
                                              getAttributesInfo=getAttributesInfo)
        elif nodeType is None:
            out[attributeName] = None
    return out

def removeXMLBlanks(node):
    for x in node.childNodes:
        if x.nodeType == Node.TEXT_NODE:
            if x.nodeValue:
                x.nodeValue = x.nodeValue.strip()
        elif x.nodeType == Node.ELEMENT_NODE:
            removeXMLBlanks(x)

def parseXMLFile(filePath):
    parsedXML = parse(filePath)
    removeXMLBlanks(parsedXML)
    parsedXML.normalize()
    return parsedXML