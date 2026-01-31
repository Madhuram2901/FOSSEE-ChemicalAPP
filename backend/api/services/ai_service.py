import os
import google.generativeai as genai
from django.conf import settings

def generate_chemical_insights(summary_data):
    """
    Generate professional chemical engineering insights using Gemini
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "AI Insights are currently unavailable. Please configure the GEMINI_API_KEY in the backend environment."

    try:
        genai.configure(api_key=api_key)
        
        # Determine available models
        available_models = []
        try:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    available_models.append(m.name)
        except:
            pass
            
        # Preference: 1.5-flash, then 1.5-pro, then any available
        selected_model = 'gemini-1.5-flash' # Default fallback
        if available_models:
            flash_models = [m for m in available_models if '1.5-flash' in m]
            pro_models = [m for m in available_models if '1.5-pro' in m]
            
            if flash_models:
                selected_model = flash_models[0]
            elif pro_models:
                selected_model = pro_models[0]
            else:
                selected_model = available_models[0]

        # Ensure we use the short name for GenerativeModel if it starts with models/
        model_name = selected_model.replace('models/', '')
        model = genai.GenerativeModel(model_name)

        prompt = f"""
        As a professional chemical process engineer, analyze the following chemical equipment dataset summary and provide 3 very concise, actionable bullet points. 
        Focus on operational efficiency and immediate maintenance priorities.

        Dataset Summary:
        - Total Equipment: {summary_data['total_equipment']}
        - Average Flowrate: {summary_data['averages']['flowrate']} m3/h
        - Average Pressure: {summary_data['averages']['pressure']} bar
        - Average Temperature: {summary_data['averages']['temperature']} °C
        - Equipment Type Distribution: {summary_data['type_distribution']}

        Format your response as a simple list of 3 bullet points, each max 15 words. 
        Example:
        • High pressure in Compressors suggests seal inspection.
        • Temperature variance of 15% requires sensor calibration.
        """

        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Optimization Insight: The plant is operating with {summary_data['total_equipment']} units. Focus on balancing Pressure/Temperature ratios for long-term stability. (AI Service Error: {str(e)})"
