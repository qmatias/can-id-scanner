"""Barcode reading and parsing."""

from typing import Optional

import zxingcpp
from pydantic import BaseModel

from can_id_scanner.pdf417dict import fields as pdf417_fields


class Identity(BaseModel):
    """A person's identity."""

    nickname: str
    full_name: str


def read_identity(image) -> Optional[Identity]:
    """Reads a name from a barcode on an image."""
    results = zxingcpp.read_barcodes(image, formats=zxingcpp.BarcodeFormat.PDF417)
    for result in results:
        data = parse_data(result.text)
        first_name = data["First Name"].split()[0]
        nickname = first_name.title()
        full_name = (first_name + " " + data["Last Name"]).title()
        return Identity(nickname=nickname, full_name=full_name)
    return None


def parse_data(data: str) -> dict[str, str]:
    """Reads PDF417 data into a human-readable dict."""
    parsed = {}
    for line in data.split("<LF>"):
        if len(line) < 3:  # all pdf417 lines have 3char code
            continue
        code, value = line[:3], line[3:]
        code_name = pdf417_fields.get(code, code)
        parsed[code_name] = value

    return parsed
