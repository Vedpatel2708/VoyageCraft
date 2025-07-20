from dataclasses import dataclass
from typing import List, Optional

@dataclass
class TripPreferences:
    destination: str
    duration: str
    budget: str
    travel_style: str
    interests: List[str]
    special_requests: str = ""
    group_size: int = 1

    def to_dict(self):
        return {
            'destination': self.destination,
            'duration': self.duration,
            'budget': self.budget,
            'travel_style': self.travel_style,
            'interests': self.interests,
            'special_requests': self.special_requests,
            'group_size': self.group_size
        }

@dataclass
class TravelPlanResult:
    success: bool
    itinerary: Optional[str] = None
    budget: Optional[str] = None
    tips: Optional[str] = None
    transportation: Optional[str] = None
    accommodation: Optional[str] = None
    error: Optional[str] = None