from typing import List

class BreathAnalysisService:
    def analyze_breath(self, durations: List[float], attempt_count: int) -> dict:
        """
        Calculates breath metrics based on multiple attempt durations.
        """
        if not durations:
            return {
                "average_duration": 0.0,
                "lung_capacity_score": 0.0,
                "breath_stability_score": 0.0,
                "breath_strength_index": 0.0
            }

        avg_duration = sum(durations) / len(durations)
        
        # Simulated scoring logic
        # Max capacity approx 60 seconds
        lung_capacity_score = min((avg_duration / 60.0) * 100, 100.0)
        
        # Stability: 100 - (variance relative to average)
        if len(durations) > 1:
            variance = sum((d - avg_duration) ** 2 for d in durations) / len(durations)
            stability = max(100.0 - (variance * 2), 0.0)
        else:
            stability = 100.0 if attempt_count == 1 else 0.0
            
        strength_index = (lung_capacity_score * 0.7) + (stability * 0.3)
        
        return {
            "average_duration": round(avg_duration, 2),
            "lung_capacity_score": round(lung_capacity_score, 2),
            "breath_stability_score": round(stability, 2),
            "breath_strength_index": round(strength_index, 2)
        }

breath_analysis_service = BreathAnalysisService()
