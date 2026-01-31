import os
import google.generativeai as genai
from django.conf import settings

def generate_chemical_insights(summary_data, insight_type="general"):
    """
    Generate professional chemical engineering insights using Gemini.
    insight_type can be: "general", "analytics", or "trends"
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "AI Insights are currently unavailable. Please configure the GEMINI_API_KEY."

    try:
        genai.configure(api_key=api_key)
        # Determine available models (re-using logic to find flash/pro)
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        selected_model = 'gemini-1.5-flash'
        if available_models:
            flash = [m for m in available_models if '1.5-flash' in m]
            pro = [m for m in available_models if '1.5-pro' in m]
            selected_model = flash[0] if flash else (pro[0] if pro else available_models[0])

        model = genai.GenerativeModel(selected_model.replace('models/', ''))

        if insight_type == "analytics":
            prompt = f"""
            As a chemical process engineer, analyze the Pressure-Temperature correlation for this dataset:
            - Mean Pressure: {summary_data['averages']['pressure']} bar
            - Mean Temperature: {summary_data['averages']['temperature']} °C
            - Correlation Strength: {summary_data.get('correlation_label', 'calculated in real-time')}
            
            Provide a 1-sentence analytical observation about the relationship between P and T in this specific system.
            Example: "A strong positive correlation suggests that thermal expansion is the primary driver of pressure variance in this reactor loop."
            """
        elif insight_type == "trends":
            prompt = f"""
            As a chemical process engineer, analyze these stability metrics across the last 5 operational runs:
            - Dataset Overview: {summary_data.get('history_summary', 'Historical logs active')}
            
            Provide a short (max 25 words) summary of the plant's recent performance stability.
            Example: "Your plant maintains high pressure stability across recent runs. Flowrates show slight seasonal variance but remain within strict operational limits."
            """
        else:
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
            """

        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Operational observation: System is running within calculated parameters. (AI Error: {str(e)})"
