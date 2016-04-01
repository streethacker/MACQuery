#!/usr/bin/env python
#-*- coding:utf-8 -*-

import unittest
import MACQuery
from MACQuery import MACQueryHandler

handler = MACQueryHandler("./data.xml")


class FancyInputMAC(unittest.TestCase):
    FancyMacAddress = {
        "00-00-00": "XEROX CORPORATION",
                    "58-8D-09": "CISCO SYSTEMS, INC.",
                    "20-59-A0": "Paragon Technologies Inc.",
                    "9C-06-6E": "Hytera Communications Corporation Limited",
                    "9C-3A-AF": "Samsung Electronics Co.,Ltd",
                    "9C-D3-6D": "NETGEAR INC.,",
                    "E4-2A-D3": "Magneti Marelli S.p.A. Powertrain",
                    "E4-40-E2": "Samsung Electronics Co.,Ltd",
                    "FC-FB-FB": "CISCO SYSTEMS, INC.",
                    "90-2B-34": "GIGA-BYTE TECHNOLOGY CO.,LTD.",
                    "38-F5-97": "home2net GmbH",
                    "EC-89-F5": "Lenovo Mobile Communication Technology Ltd.",
                    "80-f5-93": "IRCO Sistemas de Telecomunicación S.A.",
                    "C4-ee-F5": "Oclaro, Inc.",
                    "f0-F5-ae": "Adaptrum Inc.",
                    "f4-f5-a5": "Nokia corporation",
                    "EC-89-F5-2B": "Lenovo Mobile Communication Technology Ltd.",
                    "DC-2B-66-E2": "InfoBLOCK S.A. de C.V.",
                    "00-07-F5-3D-7C": "Bridgeco Co AG",
                    "04-2B-BB-22-1F": "PicoCELA, Inc.",
                    "90-2B-34-63-E7-0D": "GIGA-BYTE TECHNOLOGY CO.,LTD.",
                    "78-2B-CB-64-D0-33": "Dell Inc",
                    "DC:2B:61": "Apple",
                    "DC:2B:66:2B:E7:00": "InfoBLOCK S.A. de C.V.",
                    "A8-2B:D6-45:22:F5": "Shina System Co., Ltd",
                    "A0-2B-B8:6D": "Hewlett Packard",
    }

    def testFancyMAC(self):
        for addr, org in self.FancyMacAddress.items():
            result = handler.query(addr)
            self.assertEqual(org, result["org"])


class BadInputMAC(unittest.TestCase):

    def testBadMAC(self):
        for addr in (
                "FC-F6",
                "E8-9A-8F-FC-78-C9-A0",
                "20-59-Z0",
                "20-59-A0-",
                "9C-06-6K",
                "*9-06-7E",
                "5$-22-33",
                "9C.3A.AF",
                "E4&2A&D3"):
            self.assertRaises(MACQuery.BadFormatError, handler.query, addr)

    def testUnknownMAC(self):
        for addr in (
                "88-99-10",
                "AA-BB-CC",
                "FF-AE-00",
                "cb-09-9d",
                "2b-ce-40",
                "7A-22-F5",
                "F1-F5-5B",
                "E1-F5-CA",
                "D8-B8-F5"):
            self.assertRaises(MACQuery.BadRequestError, handler.query, addr)

if __name__ == "__main__":
    unittest.main()
