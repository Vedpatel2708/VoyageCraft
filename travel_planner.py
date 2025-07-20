import logging
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from models import TripPreferences, TravelPlanResult

logger = logging.getLogger(__name__)

class TravelPlanner:
    def __init__(self, groq_api_key: str):
        self.llm = ChatGroq(
            temperature=0.1,
            api_key=groq_api_key,
            model_name="llama-3.3-70b-versatile"
        )
        self.setup_prompts()
    
    def setup_prompts(self):
        """Setup all the prompt templates with Indian Rupees and better formatting"""
        self.itinerary_prompt = ChatPromptTemplate.from_messages([
            ("system", """Create a detailed {duration} itinerary for {destination}. 
            Budget: {budget} | Style: {travel_style} | Group: {group_size} people | Interests: {interests}
            
            REQUIREMENTS:
            - Use Indian Rupees (₹) for all pricing
            - Format as clear bullet points with HTML structure
            - Use <h3>Day X</h3> for each day
            - Use <ul><li> for activities with time badges
            - Include <div class="time-badge">Time</div> for each activity
            - Add brief cost estimates in ₹ where relevant
            - Include 5-7 activities per day maximum
            - Make each point clear and actionable
            
            Example format:
            <h3>Day 1</h3>
            <ul>
            <li><div class="time-badge">9:00 AM</div><strong>Activity Name</strong> - Description with cost estimate (₹500-800)</li>
            </ul>"""),
            ("human", "Create a detailed itinerary with clear bullet points."),
        ])
        
        self.budget_prompt = ChatPromptTemplate.from_messages([
            ("system", """Create a detailed budget breakdown for {destination} ({duration}, {budget} level, {group_size} people).
            
            REQUIREMENTS:
            - ALL AMOUNTS IN INDIAN RUPEES (₹) ONLY
            - Format as clear bullet points using HTML <ul><li>
            - Organize into main categories with subcategories
            - Show daily averages and total estimates
            - Include specific price ranges, not vague estimates
            - Add money-saving tips as separate bullet points
            - Use <h3> for main categories
            - Be comprehensive but organized
            
            Categories to cover:
            <h3>🏨 Accommodation</h3>
            <ul>
            <li>Hotel/hostel costs per night (₹X-Y)</li>
            <li>Total accommodation cost (₹Z)</li>
            </ul>
            
            <h3>🍽️ Food & Dining</h3>
            <ul>
            <li>Breakfast: ₹X per day</li>
            <li>Lunch: ₹Y per day</li>
            <li>Dinner: ₹Z per day</li>
            </ul>
            
            And similar for Transport, Activities, Shopping, etc."""),
            ("human", "Provide a detailed budget breakdown with clear bullet points in Indian Rupees."),
        ])
        
        self.tips_prompt = ChatPromptTemplate.from_messages([
            ("system", """Provide essential travel tips for {destination}. 
            
            REQUIREMENTS:
            - Format as clear bullet points using HTML <ul><li>
            - Include relevant costs in Indian Rupees (₹)
            - Use emojis for visual appeal
            - Organize into categories
            - Include practical, actionable advice
            - Cover cultural, safety, transport, and money tips
            
            Example format:
            <h3>💰 Money & Payments</h3>
            <ul>
            <li>💳 Most places accept cards, but carry ₹2000-3000 cash</li>
            <li>🏧 ATM withdrawal fee is around ₹200-300 per transaction</li>
            </ul>"""),
            ("human", "Give me essential local tips with clear bullet points."),
        ])

        self.transportation_prompt = ChatPromptTemplate.from_messages([
            ("system", """Provide comprehensive transportation information for {destination} ({budget} budget, {group_size} people).
            
            REQUIREMENTS:
            - ALL COSTS IN INDIAN RUPEES (₹) ONLY
            - Format as clear bullet points using HTML <ul><li>
            - Organize by transportation type
            - Include specific cost ranges
            - Add booking tips and recommendations
            - Cover airport transfers, local transport, intercity travel
            
            Example format:
            <h3>✈️ Airport Transfer</h3>
            <ul>
            <li>🚕 Taxi: ₹800-1200 to city center (45 mins)</li>
            <li>🚌 Airport bus: ₹150-250 per person</li>
            </ul>"""),
            ("human", "Explain transportation options with detailed bullet points in Indian Rupees."),
        ])

        self.accommodation_prompt = ChatPromptTemplate.from_messages([
            ("system", """Recommend accommodations for {destination} ({duration}, {budget} budget, {group_size} people, {travel_style} style).
            
            REQUIREMENTS:
            - ALL PRICES IN INDIAN RUPEES (₹) ONLY
            - Format as clear bullet points using HTML <ul><li>
            - Organize by area/neighborhood
            - Include specific price ranges per night
            - Mention accommodation types and amenities
            - Add booking tips and best areas for different budgets
            
            Example format:
            <h3>🏙️ City Center Area</h3>
            <ul>
            <li>🏨 Hotels: ₹3000-6000 per night</li>
            <li>🏠 Airbnb: ₹2000-4000 per night</li>
            <li>✅ Best for: First-time visitors, close to attractions</li>
            </ul>"""),
            ("human", "Suggest accommodations with detailed bullet points in Indian Rupees."),
        ])

    def create_itinerary(self, preferences: TripPreferences) -> str:
        """Generate detailed itinerary with bullet points"""
        try:
            response = self.llm.invoke(
                self.itinerary_prompt.format_messages(
                    destination=preferences.destination,
                    duration=preferences.duration,
                    budget=preferences.budget,
                    travel_style=preferences.travel_style,
                    interests=", ".join(preferences.interests) if preferences.interests else "general sightseeing",
                    group_size=preferences.group_size,
                    special_requests=preferences.special_requests or "None"
                )
            )
            logger.info(f"✅ Created detailed itinerary for {preferences.destination}")
            return response.content
        except Exception as e:
            logger.error(f"❌ Itinerary creation failed: {e}")
            raise Exception(f"Failed to create itinerary: {str(e)}")

    def calculate_budget(self, preferences: TripPreferences) -> str:
        """Generate detailed budget breakdown with bullet points"""
        try:
            response = self.llm.invoke(
                self.budget_prompt.format_messages(
                    destination=preferences.destination,
                    duration=preferences.duration,
                    budget=preferences.budget,
                    group_size=preferences.group_size
                )
            )
            logger.info(f"💰 Created detailed budget breakdown for {preferences.destination}")
            return response.content
        except Exception as e:
            logger.error(f"❌ Budget calculation failed: {e}")
            raise Exception(f"Failed to calculate budget: {str(e)}")

    def get_local_tips(self, preferences: TripPreferences) -> str:
        """Generate detailed local tips with bullet points"""
        try:
            response = self.llm.invoke(
                self.tips_prompt.format_messages(
                    destination=preferences.destination
                )
            )
            logger.info(f"💡 Generated detailed tips for {preferences.destination}")
            return response.content
        except Exception as e:
            logger.error(f"❌ Tips generation failed: {e}")
            raise Exception(f"Failed to generate tips: {str(e)}")

    def get_transportation_info(self, preferences: TripPreferences) -> str:
        """Generate detailed transportation information with bullet points"""
        try:
            response = self.llm.invoke(
                self.transportation_prompt.format_messages(
                    destination=preferences.destination,
                    budget=preferences.budget,
                    group_size=preferences.group_size
                )
            )
            logger.info(f"🚗 Generated detailed transportation info for {preferences.destination}")
            return response.content
        except Exception as e:
            logger.error(f"❌ Transportation info failed: {e}")
            raise Exception(f"Failed to get transportation info: {str(e)}")

    def get_accommodation_info(self, preferences: TripPreferences) -> str:
        """Generate detailed accommodation suggestions with bullet points"""
        try:
            response = self.llm.invoke(
                self.accommodation_prompt.format_messages(
                    destination=preferences.destination,
                    duration=preferences.duration,
                    budget=preferences.budget,
                    group_size=preferences.group_size,
                    travel_style=preferences.travel_style
                )
            )
            logger.info(f"🏨 Generated detailed accommodation info for {preferences.destination}")
            return response.content
        except Exception as e:
            logger.error(f"❌ Accommodation info failed: {e}")
            raise Exception(f"Failed to get accommodation info: {str(e)}")

    def plan_trip(self, preferences: TripPreferences) -> dict:
        """Main method to plan a trip with detailed bullet-point formatting"""
        try:
            logger.info(f"🌍 Starting detailed trip planning for {preferences.destination}")
            
            # Generate all components with better formatting
            itinerary = self.create_itinerary(preferences)
            budget = self.calculate_budget(preferences)
            tips = self.get_local_tips(preferences)
            transportation = self.get_transportation_info(preferences)
            accommodation = self.get_accommodation_info(preferences)
            
            logger.info(f"✅ Detailed trip planning completed for {preferences.destination}")
            
            return {
                "success": True,
                "itinerary": itinerary,
                "budget": budget,
                "tips": tips,
                "transportation": transportation,
                "accommodation": accommodation
            }
            
        except Exception as e:
            logger.error(f"❌ Trip planning failed: {e}")
            return {"error": f"Failed to plan trip: {str(e)}"}

    def validate_preferences(self, preferences: TripPreferences) -> bool:
        """Validate trip preferences"""
        if not preferences.destination.strip():
            raise ValueError("Destination is required")
        if not preferences.duration.strip():
            raise ValueError("Duration is required")
        if preferences.group_size < 1:
            raise ValueError("Group size must be at least 1")
        return True