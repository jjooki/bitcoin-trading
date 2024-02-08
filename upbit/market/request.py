from dataclasses import dataclass

@dataclass
class MarketRequest:
    isDetails: bool = True
    
    def to_dict(self):
        return {
            "isDetails": self.isDetails
        }