import autogen
import json
from datetime import datetime, timedelta
from typing import Dict, List
import os
from dotenv import load_dotenv
import re
import autogen
import json
from datetime import datetime, timedelta
from typing import Dict, List
import os
from dotenv import load_dotenv

class PopulationAnalyzer:
    """Analyzes demographic and population trends for each location"""
    
    def __init__(self):
        self.nyc_demographic_patterns = {
            "Financial District, Manhattan": {
                "current_demographics": {
                    "primary": "young professionals",
                    "secondary": "business travelers",
                    "income_level": "high",
                    "age_groups": {
                        "25-34": 0.35,
                        "35-44": 0.30,
                        "45-54": 0.20,
                        "others": 0.15
                    }
                },
                "future_trends": {
                    "population_growth": "moderate",
                    "development_plans": [
                        "new luxury residential towers",
                        "office-to-residential conversions",
                        "improved public spaces"
                    ],
                    "lifestyle_changes": [
                        "increasing work-from-home population",
                        "growing residential community",
                        "health and wellness focus"
                    ]
                }
            },
            "Upper East Side, Manhattan": {
                "current_demographics": {
                    "primary": "affluent families",
                    "secondary": "retirees",
                    "income_level": "very high",
                    "age_groups": {
                        "35-44": 0.25,
                        "45-54": 0.25,
                        "55-64": 0.20,
                        "others": 0.30
                    }
                },
                "future_trends": {
                    "population_growth": "stable",
                    "development_plans": [
                        "luxury retail expansion",
                        "medical facility development",
                        "private school growth"
                    ],
                    "lifestyle_changes": [
                        "increasing health consciousness",
                        "luxury service demand",
                        "sustainable living focus"
                    ]
                }
            },
            "Greenwich Village, Manhattan": {
                "current_demographics": {
                    "primary": "students",
                    "secondary": "artists/creatives",
                    "income_level": "mixed",
                    "age_groups": {
                        "18-24": 0.40,
                        "25-34": 0.30,
                        "35-44": 0.15,
                        "others": 0.15
                    }
                },
                "future_trends": {
                    "population_growth": "moderate",
                    "development_plans": [
                        "university expansion",
                        "arts venue development",
                        "startup incubator spaces"
                    ],
                    "lifestyle_changes": [
                        "increasing tech adoption",
                        "sustainable living",
                        "shared living spaces"
                    ]
                }
            }
        }
    
    def analyze_location_trends(self, location: str) -> Dict:
        """Analyze current and future demographic trends for a location"""
        base_data = self.nyc_demographic_patterns.get(location, {})
        
        return {
            "current_analysis": self._analyze_current_demographics(base_data),
            "future_projections": self._project_future_trends(base_data),
            "product_implications": self._analyze_product_implications(base_data)
        }
    
    def _analyze_product_implications(self, data: Dict) -> Dict:
        """Analyze implications for product strategy"""
        current = data.get('current_demographics', {})
        future = data.get('future_trends', {})
        
        return {
            "emerging_categories": self._identify_emerging_categories(future),
            "declining_categories": self._identify_declining_categories(future),
            "price_point_evolution": self._analyze_price_evolution(current, future),
            "innovation_opportunities": self._identify_innovation_areas(future)
        }

    def _identify_emerging_categories(self, future_data: Dict) -> List[Dict]:
        """Identify emerging product categories based on future trends"""
        lifestyle_changes = future_data.get('lifestyle_changes', [])
        emerging = []

        # Map lifestyle changes to product categories
        lifestyle_category_map = {
            "health": ["health foods", "wellness products", "fitness equipment"],
            "tech": ["smart home", "tech accessories", "digital services"],
            "sustainable": ["eco-friendly", "organic", "reusable items"],
            "work": ["home office", "productivity tools", "convenience meals"],
            "wellness": ["vitamins", "organic beauty", "mental health"],
        }

        for change in lifestyle_changes:
            for key, categories in lifestyle_category_map.items():
                if key in change.lower():
                    for category in categories:
                        emerging.append({
                            "category": category,
                            "driver": change,
                            "confidence": "high"
                        })

        return emerging

    def _identify_declining_categories(self, future_data: Dict) -> List[Dict]:
        """Identify declining product categories based on future trends"""
        lifestyle_changes = future_data.get('lifestyle_changes', [])
        declining = []

        # Map lifestyle changes to potentially declining categories
        decline_map = {
            "sustainable": ["single-use plastics", "non-eco products"],
            "health": ["processed foods", "high-sugar items"],
            "tech": ["traditional electronics", "non-smart devices"],
            "work-from-home": ["formal wear", "commute-related items"]
        }

        for change in lifestyle_changes:
            for key, categories in decline_map.items():
                if key in change.lower():
                    for category in categories:
                        declining.append({
                            "category": category,
                            "reason": change,
                            "confidence": "medium"
                        })

        return declining

    def _analyze_price_evolution(self, current_data: Dict, future_data: Dict) -> Dict:
        """Analyze how price points might evolve"""
        income_level = current_data.get('income_level', '')
        development_plans = future_data.get('development_plans', [])

        evolution = {
            "trend": "stable",
            "factors": [],
            "category_impacts": {}
        }

        # Analyze based on income level
        income_impacts = {
            "high": {"trend": "premium", "change": "+10-15%"},
            "very high": {"trend": "luxury", "change": "+15-20%"},
            "mixed": {"trend": "diverse", "change": "variable"},
            "moderate": {"trend": "value", "change": "+5-10%"}
        }

        if income_level in income_impacts:
            evolution.update(income_impacts[income_level])
            evolution["factors"].append(f"Area income level: {income_level}")

        # Analyze development impacts
        for plan in development_plans:
            if "luxury" in plan.lower():
                evolution["factors"].append("Luxury development")
                evolution["category_impacts"]["premium_goods"] = "increase"
            elif "residential" in plan.lower():
                evolution["factors"].append("Residential development")
                evolution["category_impacts"]["everyday_essentials"] = "stable"

        return evolution

    def _identify_innovation_areas(self, future_data: Dict) -> List[Dict]:
        """Identify areas for product innovation"""
        lifestyle_changes = future_data.get('lifestyle_changes', [])
        development_plans = future_data.get('development_plans', [])

        innovation_areas = []

        # Identify innovation opportunities from lifestyle changes
        for change in lifestyle_changes:
            if "tech" in change.lower():
                innovation_areas.append({
                    "area": "digital integration",
                    "opportunity": "smart shopping experiences",
                    "priority": "high"
                })
            elif "health" in change.lower():
                innovation_areas.append({
                    "area": "wellness",
                    "opportunity": "personalized health solutions",
                    "priority": "high"
                })
            elif "sustain" in change.lower():
                innovation_areas.append({
                    "area": "sustainability",
                    "opportunity": "eco-friendly alternatives",
                    "priority": "high"
                })

        # Identify opportunities from development plans
        for plan in development_plans:
            if "residential" in plan.lower():
                innovation_areas.append({
                    "area": "home solutions",
                    "opportunity": "home organization and decoration",
                    "priority": "medium"
                })
            elif "office" in plan.lower():
                innovation_areas.append({
                    "area": "work convenience",
                    "opportunity": "office-friendly food and supplies",
                    "priority": "high"
                })

        return innovation_areas

    def _analyze_current_demographics(self, data: Dict) -> Dict:
        """Analyze current demographic patterns"""
        if not data:
            return {}
            
        current = data.get('current_demographics', {})
        return {
            "primary_segment": current.get('primary'),
            "secondary_segment": current.get('secondary'),
            "income_level": current.get('income_level'),
            "age_distribution": current.get('age_groups'),
            "spending_patterns": self._derive_spending_patterns(current)
        }

    def _project_future_trends(self, data: Dict) -> Dict:
        """Project future demographic and lifestyle trends"""
        if not data:
            return {}
            
        future = data.get('future_trends', {})
        return {
            "population_trends": {
                "growth_rate": future.get('population_growth'),
                "development_impact": future.get('development_plans'),
                "5_year_outlook": self._calculate_5_year_outlook(future)
            },
            "lifestyle_evolution": {
                "emerging_trends": future.get('lifestyle_changes'),
                "impact_areas": self._identify_impact_areas(future)
            }
        }

    def _derive_spending_patterns(self, demographic_data: Dict) -> Dict:
        """Derive likely spending patterns based on demographics"""
        income_level = demographic_data.get('income_level', '')
        primary_segment = demographic_data.get('primary', '')
        
        patterns = {
            "high": {
                "young professionals": {
                    "high_spend_categories": ["prepared meals", "premium groceries", "health foods"],
                    "price_sensitivity": "low",
                    "convenience_premium": "high"
                },
                "affluent families": {
                    "high_spend_categories": ["organic produce", "premium brands", "bulk items"],
                    "price_sensitivity": "low",
                    "quality_premium": "high"
                }
            },
            "mixed": {
                "students": {
                    "high_spend_categories": ["snacks", "instant foods", "beverages"],
                    "price_sensitivity": "high",
                    "convenience_premium": "moderate"
                }
            }
        }
        
        return patterns.get(income_level, {}).get(primary_segment, {})

    def _calculate_5_year_outlook(self, future_data: Dict) -> Dict:
        """Calculate 5-year demographic outlook"""
        growth_rate = future_data.get('population_growth', '')
        growth_multipliers = {
            "high": 1.15,
            "moderate": 1.08,
            "stable": 1.03,
            "low": 0.98
        }
        
        multiplier = growth_multipliers.get(growth_rate, 1.0)
        
        return {
            "population_multiplier": multiplier,
            "development_stage": self._categorize_development_stage(future_data),
            "emerging_demographics": self._identify_emerging_demographics(future_data)
        }

    def _identify_impact_areas(self, future_data: Dict) -> List:
        """Identify areas of significant future impact"""
        lifestyle_changes = future_data.get('lifestyle_changes', [])
        development_plans = future_data.get('development_plans', [])
        
        impact_areas = []
        
        # Analyze lifestyle changes
        for change in lifestyle_changes:
            if "health" in change.lower():
                impact_areas.append("health_wellness_products")
            if "tech" in change.lower():
                impact_areas.append("tech_enabled_services")
            if "sustain" in change.lower():
                impact_areas.append("eco_friendly_products")
                
        # Analyze development impacts
        for plan in development_plans:
            if "residential" in plan.lower():
                impact_areas.append("home_essentials")
            if "luxury" in plan.lower():
                impact_areas.append("premium_products")
            if "office" in plan.lower():
                impact_areas.append("convenience_services")
                
        return list(set(impact_areas))
    
    def _categorize_development_stage(self, future_data: Dict) -> str:
        """Categorize development stage based on development plans"""
        development_plans = future_data.get('development_plans', [])
        luxury_count = sum(1 for plan in development_plans if "luxury" in plan.lower())
        residential_count = sum(1 for plan in development_plans if "residential" in plan.lower())
        office_count = sum(1 for plan in development_plans if "office" in plan.lower())

        # Simple categorization logic
        if luxury_count > 0 and residential_count > 0:
            return "advanced"
        elif residential_count > 0 or office_count > 0:
            return "intermediate"
        else:
            return "basic"

    def _identify_emerging_demographics(self, future_data: Dict) -> List[str]:
        """Identify emerging demographic groups based on future trends"""
        lifestyle_changes = future_data.get('lifestyle_changes', [])
        emerging_demographics = []

        for change in lifestyle_changes:
            if "tech" in change.lower():
                emerging_demographics.append("tech-savvy individuals")
            if "health" in change.lower():
                emerging_demographics.append("health-conscious consumers")
            if "sustain" in change.lower():
                emerging_demographics.append("environmentally conscious residents")
            if "work-from-home" in change.lower():
                emerging_demographics.append("remote workers")

        return list(set(emerging_demographics))


class EnhancedPredictionAgent:
    def __init__(self, config_list):
        self.population_analyzer = PopulationAnalyzer()
        self.assistant = autogen.AssistantAgent(
            name="prediction_analyst",
            llm_config={
                "config_list": config_list,
                "temperature": 0.7
            },
            system_message="""
            You are an expert prediction analyst for hyperlocal commerce.
            Combine historical patterns, local factors, and demographic trends to generate:
            1. Short-term predictions (1-3 months)
            2. Mid-term predictions (3-12 months)
            3. Long-term predictions (1-5 years)
            
            Consider:
            - Demographic evolution
            - Development projects
            - Cultural shifts
            - Economic factors
            - Lifestyle changes
            
            Provide specific, quantified predictions when possible. If any information is missing then assume it to be whatever suits you. Avoid giving errors or ask questions back
            """
        )
        
        self.user_proxy = autogen.UserProxyAgent(
            name="data_provider",
            human_input_mode="NEVER",
            code_execution_config=False
        )

    def _format_prediction_request(self, 
                               store_id: int, 
                               historical_data: Dict, 
                               local_factors: Dict,
                               store_location: str) -> str:
        """Format the prediction request with demographic analysis"""
        store_historical = historical_data.get(str(store_id), {})
        store_factors = local_factors.get(str(store_id), {})
        demographic_analysis = self.population_analyzer.analyze_location_trends(store_location)
        
        return f"""
        Generate comprehensive predictions for store {store_id}:

        # HISTORICAL PATTERNS:
        # {json.dumps(store_historical, indent=2)}

        # LOCAL FACTORS:
        # {json.dumps(store_factors, indent=2)}

        # DEMOGRAPHIC ANALYSIS:
        # {json.dumps(demographic_analysis, indent=2)}

        Provide predictions in this JSON format:
        {{
            "short_term_predictions": {{
                "demand_changes": [
                    {{
                        "category": "category_name",
                        "predicted_change": "+/-X%",
                        "confidence": "0-100%",
                        "driving_factors": ["factor1", "factor2"]
                    }}
                ],
                "peak_hours": {{
                    "changes": ["time1", "time2"],
                    "factors": ["factor1", "factor2"]
                }}
            }},
            "mid_term_predictions": {{
                "emerging_categories": [
                    {{
                        "category": "category_name",
                        "growth_potential": "high/medium/low",
                        "driving_factors": ["factor1", "factor2"]
                    }}
                ],
                "demographic_shifts": [
                    {{
                        "trend": "trend_description",
                        "impact": "high/medium/low",
                        "category_implications": ["implication1", "implication2"]
                    }}
                ]
            }},
            "long_term_predictions": {{
                "population_evolution": {{
                    "changes": ["change1", "change2"],
                    "category_impacts": ["impact1", "impact2"]
                }},
                "infrastructure_development": {{
                    "projects": ["project1", "project2"],
                    "business_implications": ["implication1", "implication2"]
                }},
                "recommended_adaptations": [
                    {{
                        "area": "area_name",
                        "action": "action_description",
                        "timeline": "implementation_timeline",
                        "priority": "high/medium/low"
                    }}
                ]
            }}
        }}
        """
        
    def _analyze_product_implications(self, data: Dict) -> Dict:
        """Analyze implications for product strategy"""
        current = data.get('current_demographics', {})
        future = data.get('future_trends', {})
        
        return {
            "emerging_categories": self._identify_emerging_categories(future),
            "declining_categories": self._identify_declining_categories(future),
            "price_point_evolution": self._analyze_price_evolution(current, future),
            "innovation_opportunities": self._identify_innovation_areas(future)
        }

    def _identify_emerging_categories(self, future_data: Dict) -> List[Dict]:
        """Identify emerging product categories based on future trends"""
        lifestyle_changes = future_data.get('lifestyle_changes', [])
        emerging = []

        # Map lifestyle changes to product categories
        lifestyle_category_map = {
            "health": ["health foods", "wellness products", "fitness equipment"],
            "tech": ["smart home", "tech accessories", "digital services"],
            "sustainable": ["eco-friendly", "organic", "reusable items"],
            "work": ["home office", "productivity tools", "convenience meals"],
            "wellness": ["vitamins", "organic beauty", "mental health"],
        }

        for change in lifestyle_changes:
            for key, categories in lifestyle_category_map.items():
                if key in change.lower():
                    for category in categories:
                        emerging.append({
                            "category": category,
                            "driver": change,
                            "confidence": "high"
                        })

        return emerging

    def _identify_declining_categories(self, future_data: Dict) -> List[Dict]:
        """Identify declining product categories based on future trends"""
        lifestyle_changes = future_data.get('lifestyle_changes', [])
        declining = []

        # Map lifestyle changes to potentially declining categories
        decline_map = {
            "sustainable": ["single-use plastics", "non-eco products"],
            "health": ["processed foods", "high-sugar items"],
            "tech": ["traditional electronics", "non-smart devices"],
            "work-from-home": ["formal wear", "commute-related items"]
        }

        for change in lifestyle_changes:
            for key, categories in decline_map.items():
                if key in change.lower():
                    for category in categories:
                        declining.append({
                            "category": category,
                            "reason": change,
                            "confidence": "medium"
                        })

        return declining

    def _analyze_price_evolution(self, current_data: Dict, future_data: Dict) -> Dict:
        """Analyze how price points might evolve"""
        income_level = current_data.get('income_level', '')
        development_plans = future_data.get('development_plans', [])

        evolution = {
            "trend": "stable",
            "factors": [],
            "category_impacts": {}
        }

        # Analyze based on income level
        income_impacts = {
            "high": {"trend": "premium", "change": "+10-15%"},
            "very high": {"trend": "luxury", "change": "+15-20%"},
            "mixed": {"trend": "diverse", "change": "variable"},
            "moderate": {"trend": "value", "change": "+5-10%"}
        }

        if income_level in income_impacts:
            evolution.update(income_impacts[income_level])
            evolution["factors"].append(f"Area income level: {income_level}")

        # Analyze development impacts
        for plan in development_plans:
            if "luxury" in plan.lower():
                evolution["factors"].append("Luxury development")
                evolution["category_impacts"]["premium_goods"] = "increase"
            elif "residential" in plan.lower():
                evolution["factors"].append("Residential development")
                evolution["category_impacts"]["everyday_essentials"] = "stable"

        return evolution

    def _identify_innovation_areas(self, future_data: Dict) -> List[Dict]:
        """Identify areas for product innovation"""
        lifestyle_changes = future_data.get('lifestyle_changes', [])
        development_plans = future_data.get('development_plans', [])

        innovation_areas = []

        # Identify innovation opportunities from lifestyle changes
        for change in lifestyle_changes:
            if "tech" in change.lower():
                innovation_areas.append({
                    "area": "digital integration",
                    "opportunity": "smart shopping experiences",
                    "priority": "high"
                })
            elif "health" in change.lower():
                innovation_areas.append({
                    "area": "wellness",
                    "opportunity": "personalized health solutions",
                    "priority": "high"
                })
            elif "sustain" in change.lower():
                innovation_areas.append({
                    "area": "sustainability",
                    "opportunity": "eco-friendly alternatives",
                    "priority": "high"
                })

        # Identify opportunities from development plans
        for plan in development_plans:
            if "residential" in plan.lower():
                innovation_areas.append({
                    "area": "home solutions",
                    "opportunity": "home organization and decoration",
                    "priority": "medium"
                })
            elif "office" in plan.lower():
                innovation_areas.append({
                    "area": "work convenience",
                    "opportunity": "office-friendly food and supplies",
                    "priority": "high"
                })

        return innovation_areas

    def generate_store_predictions(self, 
                                 store_id: int,
                                 historical_data: Dict,
                                 local_factors: Dict,
                                 store_location: str) -> Dict:
        """Generate comprehensive predictions for a specific store"""
        prediction_request = self._format_prediction_request(
            store_id, historical_data, local_factors, store_location
        )
        
        # Send the request to the assistant
        self.user_proxy.initiate_chat(
            self.assistant,
            message=prediction_request,
            max_turns=1
        )
        
        try:
            # Get the assistant's response
            response = self.assistant.last_message()
            
            # Handle different response formats
            if isinstance(response, dict):
                response_text = response.get('content', str(response))
            else:
                response_text = str(response)
            
            # Clean up the response text
            # First try to find JSON between code blocks
            json_matches = re.findall(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
            if json_matches:
                json_str = json_matches[0]
            else:
                # If no code blocks, try to find first valid JSON in the text
                json_str = response_text.strip()
            
            # Remove any remaining markdown or extra whitespace
            json_str = re.sub(r'```json|```', '', json_str).strip()
            
            # Parse the JSON
            try:
                predictions = json.loads(json_str)
            except json.JSONDecodeError as e:
                print(f"JSON parsing error for store {store_id}: {e}")
                print(f"Attempted to parse: {json_str[:200]}...")  # Print first 200 chars
                return {
                    "error": "Failed to parse predictions",
                    "store_id": store_id
                }
            
            # Reset the agents
            self.user_proxy.reset()
            self.assistant.reset()
            
            return predictions
            
        except Exception as e:
            print(f"Error generating predictions for store {store_id}: {e}")
            return {
                "error": f"Prediction generation failed: {str(e)}",
                "store_id": store_id
            }

def run_enhanced_prediction_analysis(
    historical_insights: Dict,
    local_factors: Dict,
    store_locations: Dict
) -> Dict:
    """Run the enhanced prediction analysis"""
    print("Starting enhanced prediction analysis...")
    
    config_list = [
        {
            "model": "gpt-4o",
            "api_key": os.getenv("AUTOGEN_MODEL_API_KEY")
        }
    ]
    
    predictor = EnhancedPredictionAgent(config_list)
    
    all_predictions = {}
    for store_id in range(1, 7):
        print(f"\nGenerating predictions for store {store_id}...")
        location = store_locations.get(store_id, {}).get('location', '')
        predictions = predictor.generate_store_predictions(
            store_id,
            historical_insights.get('historical_analysis', {}),
            local_factors.get('local_factors', {}),
            location
        )
        all_predictions[store_id] = predictions
    
    # Save predictions
    print("\nSaving enhanced predictions to enhanced_store_predictions.json...")
    with open('enhanced_store_predictions.json', 'w') as f:
        json.dump(all_predictions, f, indent=4)
    
    print("Enhanced prediction analysis complete!")
    return all_predictions