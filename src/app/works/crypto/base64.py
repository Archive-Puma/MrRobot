from app.works.base     import Base
from app.core.exception import Elliot

import base64

class Work(Base):
    
    # Data
    name = "base64"
    category = "crypto"

    def run(self):
        param, msg = self.get_one("encode","decode")
        try:
            if param == "encode":
                # Encode
                result = base64.b64encode(bytes(msg, encoding="utf-8"))
            else:
                # Align the b64 message
                msg += "=" * ((4 - len(msg) % 4) % 4)
                # Decode
                result = base64.b64decode(bytes(msg, encoding="utf-8"))
        except binascii.Error:
            raise Elliot(f"Cannot {param} base64: {msg}")
        # Return the message in a utf8 format
        return result.decode("utf-8")
        