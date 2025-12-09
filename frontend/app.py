# import streamlit as st
# import requests
# import json
# from PIL import Image
# from datetime import datetime
# import base64

# # Page configuration
# st.set_page_config(
#     page_title="Plant Disease Classifier",
#     page_icon="🌱",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Custom CSS
# st.markdown("""
# <style>
# .main-header {
#     font-size: 2.5rem;
#     color: #2E8B57;
#     text-align: center;
#     margin-bottom: 1rem;
# }
# .sub-header {
#     font-size: 1.2rem;
#     color: #228B22;
#     margin-bottom: 2rem;
#     text-align: center;
# }
# .metric-box {
#     background-color: #f8f9fa;
#     border: 2px solid #e9ecef;
#     border-radius: 10px;
#     padding: 15px;
#     text-align: center;
# }
# .success-box {
#     background-color: #d4edda;
#     border: 1px solid #c3e6cb;
#     border-radius: 5px;
#     padding: 20px;
#     margin: 10px 0;
# }
# .warning-box {
#     background-color: #fff3cd;
#     border: 1px solid #ffeaa7;
#     border-radius: 5px;
#     padding: 20px;
#     margin: 10px 0;
# }
# .info-box {
#     background-color: #d1ecf1;
#     border: 1px solid #bee5eb;
#     border-radius: 5px;
#     padding: 20px;
#     margin: 10px 0;
# }
# .stButton > button {
#     background-color: #28a745;
#     color: white;
#     font-weight: bold;
# }
# .stButton > button:hover {
#     background-color: #218838;
# }
# .treatment-card {
#     background-color: #f8f9fa;
#     border-left: 4px solid #28a745;
#     border-radius: 5px;
#     padding: 15px;
#     margin: 10px 0;
# }
# </style>
# """, unsafe_allow_html=True)

# # Initialize session state
# if 'predictions' not in st.session_state:
#     st.session_state.predictions = []
# if 'backend_url' not in st.session_state:
#     st.session_state.backend_url = "http://localhost:8000"

# def check_backend_health(url):
#     """Check if backend is available"""
#     try:
#         response = requests.get(f"{url}/health", timeout=5)
#         if response.status_code == 200:
#             return response.json()
#         return None
#     except:
#         return None

# def display_results(result):
#     """Display analysis results properly"""
#     # Extract data correctly
#     mode = result.get('mode', 'unknown')
    
#     if mode == 'online' and 'analysis' in result:
#         # Online mode with analysis
#         analysis = result['analysis']
#         plant_type = analysis.get('plant_type', 'Unknown')
#         disease = analysis.get('disease', 'Unknown')
#         is_healthy = analysis.get('is_healthy', False)
#         plant_confidence = analysis.get('plant_confidence', 0.0)
#         disease_confidence = analysis.get('disease_confidence', 0.0)
#         message = analysis.get('message', '')
#         treatment = analysis.get('treatment', {})
#         audio_url = result.get('audio_url')
#     else:
#         # Offline mode or direct response
#         plant_type = result.get('plant_type', 'Unknown')
#         disease = result.get('disease', 'Unknown')
#         is_healthy = result.get('is_healthy', False)
#         plant_confidence = result.get('plant_confidence', 0.0)
#         disease_confidence = result.get('disease_confidence', 0.0)
#         message = result.get('message', '')
#         treatment = result.get('treatment', {})
#         audio_url = result.get('audio_url')
    
#     # Display success message
#     st.markdown('<div class="success-box">', unsafe_allow_html=True)
#     st.write("✅ **Analysis Complete!**")
#     if message:
#         st.write(f"**Finding:** {message}")
#     st.markdown('</div>', unsafe_allow_html=True)
    
#     # Create columns for metrics
#     col1, col2, col3, col4 = st.columns(4)
    
#     with col1:
#         # Capitalize plant type for better display
#         display_plant = plant_type.capitalize() if plant_type != 'Unknown' else 'Unknown'
#         confidence_text = f"{plant_confidence*100:.0f}%" if plant_confidence > 0 else ""
#         st.metric("🌿 Plant Type", display_plant, confidence_text)
    
#     with col2:
#         # Format disease name
#         display_disease = disease.replace('_', ' ').title() if disease != 'Unknown' else 'Unknown'
#         confidence_text = f"{disease_confidence*100:.0f}%" if disease_confidence > 0 else ""
#         st.metric("🔬 Disease/Condition", display_disease, confidence_text)
    
#     with col3:
#         status = "✅ Healthy" if is_healthy else "⚠️ Diseased"
#         status_icon = "🟢" if is_healthy else "🔴"
#         st.metric("📊 Health Status", f"{status_icon} {status}")
    
#     with col4:
#         mode_display = "🌐 Online" if mode == 'online' else "📡 Offline"
#         st.metric("⚙️ Mode", mode_display)
    
#     # Health status details
#     if not is_healthy:
#         st.markdown('<div class="warning-box">', unsafe_allow_html=True)
#         st.write(f"⚠️ **Attention needed:** Your {display_plant} plant shows signs of **{display_disease}**.")
#         st.markdown('</div>', unsafe_allow_html=True)
#     else:
#         st.markdown('<div class="success-box">', unsafe_allow_html=True)
#         st.write(f"🎉 **Good news!** Your {display_plant} plant appears to be **healthy**.")
#         st.markdown('</div>', unsafe_allow_html=True)
    
#     # Display treatment recommendations
#     if treatment and isinstance(treatment, dict) and any(treatment.values()):
#         st.subheader("💊 Treatment Recommendations")
        
#         # Create tabs for different treatment types
#         tab1, tab2, tab3 = st.tabs(["🌱 Cultural Control", "🧪 Chemical Control", "🛡️ Preventive Measures"])
        
#         with tab1:
#             cultural = treatment.get('cultural', '')
#             if cultural:
#                 if isinstance(cultural, list):
#                     for i, item in enumerate(cultural, 1):
#                         st.write(f"{i}. {item}")
#                 else:
#                     st.write(cultural)
#             else:
#                 st.info("No cultural control recommendations available.")
        
#         with tab2:
#             chemical = treatment.get('chemical', '')
#             if chemical:
#                 if isinstance(chemical, list):
#                     for i, item in enumerate(chemical, 1):
#                         st.write(f"{i}. {item}")
#                 else:
#                     st.write(chemical)
#             else:
#                 st.info("No chemical control recommendations available.")
        
#         with tab3:
#             preventive = treatment.get('preventive', '')
#             if preventive:
#                 if isinstance(preventive, list):
#                     for i, item in enumerate(preventive, 1):
#                         st.write(f"{i}. {item}")
#                 else:
#                     st.write(preventive)
#             else:
#                 st.info("No preventive measures available.")
    
#     # Audio output
#     if audio_url:
#         st.subheader("🎵 Audio Summary")
#         st.audio(audio_url, format="audio/mp3")
#         st.caption("AI-generated voice summary of the analysis")
    
#     # Display plant information based on type
#     display_plant_info(display_plant)
    
#     # Download options
#     st.subheader("📥 Export Results")
    
#     # Create JSON for download
#     result_json = json.dumps(result, indent=2, ensure_ascii=False)
    
#     # Create text summary
#     text_summary = f"""PLANT DISEASE ANALYSIS REPORT
# {'=' * 40}
# Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# Plant Type: {display_plant}
# Disease/Condition: {display_disease}
# Health Status: {'Healthy' if is_healthy else 'Diseased'}
# Confidence: {plant_confidence*100:.1f}%
# Analysis Mode: {mode}

# FINDINGS:
# {message}

# TREATMENT RECOMMENDATIONS:
# """
    
#     if treatment:
#         for key, value in treatment.items():
#             if value:
#                 text_summary += f"\n{key.upper()}:\n"
#                 if isinstance(value, list):
#                     for item in value:
#                         text_summary += f"  • {item}\n"
#                 else:
#                     text_summary += f"  {value}\n"
    
#     col1, col2 = st.columns(2)
    
#     with col1:
#         st.download_button(
#             label="📄 Download JSON Report",
#             data=result_json,
#             file_name=f"plant_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
#             mime="application/json",
#             use_container_width=True
#         )
    
#     with col2:
#         st.download_button(
#             label="📝 Download Text Summary",
#             data=text_summary,
#             file_name=f"plant_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
#             mime="text/plain",
#             use_container_width=True
#         )

# def display_plant_info(plant_type):
#     """Display information about the detected plant"""
#     plant_info = {
#         "Tomato": {
#             "description": "Tomato (Solanum lycopersicum) is a warm-season fruiting plant.",
#             "common_varieties": ["Cherry", "Beefsteak", "Roma", "Heirloom"],
#             "growing_season": "Spring to Fall",
#             "ideal_temp": "21-27°C (70-80°F)",
#             "watering": "Regular, deep watering (2-3 times per week)",
#             "sunlight": "Full sun (6-8 hours daily)"
#         },
#         "Potato": {
#             "description": "Potato (Solanum tuberosum) is a root vegetable that grows underground.",
#             "common_varieties": ["Russet", "Yukon Gold", "Red", "Fingerling"],
#             "growing_season": "Cool season crop",
#             "ideal_temp": "15-20°C (60-68°F)",
#             "watering": "Consistent moisture, avoid waterlogging",
#             "sunlight": "Full sun"
#         },
#         "Corn": {
#             "description": "Corn (Zea mays) is a tall cereal grass that produces kernels on ears.",
#             "common_varieties": ["Sweet corn", "Field corn", "Popcorn"],
#             "growing_season": "Warm season",
#             "ideal_temp": "21-30°C (70-86°F)",
#             "watering": "Regular watering, especially during tasseling",
#             "sunlight": "Full sun"
#         },
#         "Rice": {
#             "description": "Rice (Oryza sativa) is a staple cereal grain that grows in flooded fields.",
#             "common_varieties": ["Jasmine", "Basmati", "Arborio", "Brown"],
#             "growing_season": "Wet season",
#             "ideal_temp": "20-35°C (68-95°F)",
#             "watering": "Flooded fields required",
#             "sunlight": "Full sun"
#         }
#     }
    
#     if plant_type.lower() in ['tomato', 'potato', 'corn', 'rice']:
#         info = plant_info.get(plant_type.capitalize(), {})
#         if info:
#             with st.expander(f"🌱 About {plant_type.capitalize()} Plants"):
#                 st.write(f"**Description**: {info['description']}")
                
#                 st.write("**Common Varieties**:")
#                 for variety in info['common_varieties']:
#                     st.write(f"- {variety}")
                
#                 st.write(f"**Growing Season**: {info['growing_season']}")
#                 st.write(f"**Ideal Temperature**: {info['ideal_temp']}")
#                 st.write(f"**Watering Needs**: {info['watering']}")
#                 st.write(f"**Sunlight Requirements**: {info['sunlight']}")

# def main():
#     # Header
#     st.markdown('<h1 class="main-header">🌱 Plant Disease Classifier</h1>', unsafe_allow_html=True)
#     st.markdown('<h3 class="sub-header">AI-powered plant health analysis system</h3>', unsafe_allow_html=True)
    
#     # Sidebar
#     with st.sidebar:
#         st.title("⚙️ Configuration")
        
#         # Backend URL input
#         backend_url = st.text_input(
#             "Backend API URL",
#             value=st.session_state.backend_url,
#             help="Enter the URL where your FastAPI backend is running"
#         )
#         st.session_state.backend_url = backend_url
        
#         # Connection test
#         if st.button("🔗 Test Connection", use_container_width=True):
#             with st.spinner("Checking..."):
#                 health = check_backend_health(backend_url)
#                 if health:
#                     st.success("✅ Connected!")
#                     st.write(f"**Models**: {'Loaded' if health.get('models_loaded') else 'Not loaded'}")
#                     st.write(f"**Modes**: {', '.join(health.get('available_modes', []))}")
#                 else:
#                     st.error("❌ Cannot connect")
        
#         st.divider()
        
#         # Mode selection
#         st.subheader("Analysis Mode")
#         mode = st.radio(
#             "Select analysis mode:",
#             ["Auto", "Online", "Offline"],
#             index=0,
#             help="Auto: Uses online if available, falls back to offline"
#         )
        
#         st.divider()
        
#         # History
#         st.subheader("📋 Recent Analysis")
#         if st.session_state.predictions:
#             for pred in reversed(st.session_state.predictions[-3:]):
#                 # Extract plant type properly
#                 plant = "Unknown"
#                 if pred.get('mode') == 'online' and 'analysis' in pred:
#                     plant = pred['analysis'].get('plant_type', 'Unknown')
#                 else:
#                     plant = pred.get('plant_type', 'Unknown')
                
#                 # Extract disease
#                 disease = "Unknown"
#                 if pred.get('mode') == 'online' and 'analysis' in pred:
#                     disease = pred['analysis'].get('disease', 'Unknown')
#                 else:
#                     disease = pred.get('disease', 'Unknown')
                
#                 status = "🟢" if pred.get('is_healthy', False) else "🔴"
#                 st.write(f"{status} {plant.capitalize()} - {disease}")
#         else:
#             st.write("No analysis history")
        
#         if st.session_state.predictions and st.button("🗑️ Clear History", use_container_width=True):
#             st.session_state.predictions = []
#             st.rerun()
    
#     # Main content area
#     col1, col2 = st.columns([1, 1])
    
#     with col1:
#         st.header("📤 Upload Image")
        
#         # File uploader
#         uploaded_file = st.file_uploader(
#             "Choose a plant leaf image",
#             type=['jpg', 'jpeg', 'png'],
#             help="Upload a clear image of plant leaves"
#         )
        
#         if uploaded_file is not None:
#             # Display image
#             image = Image.open(uploaded_file)
#             st.image(image, caption="Uploaded Image", use_column_width=True)
            
#             # Image details
#             with st.expander("📷 Image Details"):
#                 st.write(f"**File**: {uploaded_file.name}")
#                 st.write(f"**Size**: {uploaded_file.size / 1024:.1f} KB")
#                 st.write(f"**Dimensions**: {image.size[0]} × {image.size[1]} pixels")
#                 st.write(f"**Format**: {image.format}")
    
#     with col2:
#         st.header("🔍 Analysis Results")
        
#         if uploaded_file is not None:
#             # Analyze button
#             if st.button("🔬 Analyze Plant Health", type="primary", use_container_width=True):
#                 with st.spinner("Analyzing image. This may take 10-30 seconds..."):
#                     try:
#                         # Prepare file for upload
#                         files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                        
#                         # Send request to backend
#                         response = requests.post(
#                             f"{backend_url}/predict",
#                             files=files,
#                             timeout=60
#                         )
                        
#                         if response.status_code == 200:
#                             result = response.json()
                            
#                             # Store in history
#                             result['timestamp'] = datetime.now().isoformat()
#                             st.session_state.predictions.append(result)
                            
#                             # Display results
#                             display_results(result)
                            
#                         elif response.status_code == 503:
#                             st.error("Service Unavailable")
#                             st.info("""
#                             Possible reasons:
#                             1. Backend server not running
#                             2. No internet connection (for online mode)
#                             3. Models not loaded (for offline mode)
#                             """)
#                         else:
#                             st.error(f"Error {response.status_code}")
#                             st.write(f"Details: {response.text}")
                            
#                     except requests.exceptions.ConnectionError:
#                         st.error("Connection Error")
#                         st.info(f"""
#                         Cannot connect to backend at:
#                         **{backend_url}**
                        
#                         Make sure:
#                         1. Backend server is running
#                         2. URL is correct
#                         3. No firewall blocking
#                         """)
                        
#                     except requests.exceptions.Timeout:
#                         st.error("Request Timeout")
#                         st.write("The analysis is taking too long. Try:")
#                         st.write("- Smaller image")
#                         st.write("- Better internet connection")
                        
#                     except Exception as e:
#                         st.error(f"Unexpected Error: {str(e)}")
        
#         else:
#             # Welcome/instructions
#             st.markdown('<div class="info-box">', unsafe_allow_html=True)
#             st.write("""
#             ## 📋 Instructions
            
#             1. **Upload** a plant leaf image on the left
#             2. **Configure** backend URL if needed
#             3. **Click Analyze** to start detection
#             4. **Review** results and recommendations
            
#             ### 💡 Tips for Best Results:
#             - Use clear, well-lit images
#             - Focus on affected leaves
#             - Include scale if possible
#             - Avoid blurry photos
#             """)
#             st.markdown('</div>', unsafe_allow_html=True)
            
#             # Quick stats
#             if st.session_state.predictions:
#                 total = len(st.session_state.predictions)
#                 healthy = sum(1 for p in st.session_state.predictions 
#                             if p.get('is_healthy') or 
#                             ('analysis' in p and p['analysis'].get('is_healthy')))
#                 diseased = total - healthy
                
#                 st.metric("📊 Total Analyses", total)
#                 st.metric("✅ Healthy Plants", healthy)
#                 st.metric("⚠️ Diseased Plants", diseased)
    
#     # Footer
#     st.divider()
#     footer_cols = st.columns(4)
#     with footer_cols[0]:
#         st.write("**Version**: 1.0.0")
#     with footer_cols[1]:
#         st.write("**Backend**: FastAPI")
#     with footer_cols[2]:
#         st.write("**AI Model**: GPT-4 + Custom CNN")
#     with footer_cols[3]:
#         st.write("**Status**: " + ("✅ Connected" if check_backend_health(backend_url) else "❌ Disconnected"))

# if __name__ == "__main__":
#     main()




import streamlit as st
import requests
import json
from PIL import Image
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="Plant Disease Classifier",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    color: #2E8B57;
    text-align: center;
    margin-bottom: 1rem;
}
.sub-header {
    font-size: 1.2rem;
    color: #228B22;
    margin-bottom: 2rem;
    text-align: center;
}
.metric-box {
    background-color: #f8f9fa;
    border: 2px solid #e9ecef;
    border-radius: 10px;
    padding: 15px;
    text-align: center;
}
.success-box {
    background-color: #d4edda;
    border: 1px solid #c3e6cb;
    border-radius: 5px;
    padding: 20px;
    margin: 10px 0;
}
.warning-box {
    background-color: #fff3cd;
    border: 1px solid #ffeaa7;
    border-radius: 5px;
    padding: 20px;
    margin: 10px 0;
}
.info-box {
    background-color: #d1ecf1;
    border: 1px solid #bee5eb;
    border-radius: 5px;
    padding: 20px;
    margin: 10px 0;
}
.stButton > button {
    background-color: #28a745;
    color: white;
    font-weight: bold;
}
.stButton > button:hover {
    background-color: #218838;
}
.upload-box {
    border: 2px dashed #4CAF50;
    border-radius: 10px;
    padding: 30px;
    text-align: center;
    margin: 20px 0;
}
.treatment-tab {
    background-color: #f8f9fa;
    border-radius: 5px;
    padding: 15px;
    margin: 5px 0;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'predictions' not in st.session_state:
    st.session_state.predictions = []
if 'backend_url' not in st.session_state:
    st.session_state.backend_url = "https://plant-disease-classifier-7.onrender.com"
if 'last_analysis' not in st.session_state:
    st.session_state.last_analysis = None

def check_backend_health(url):
    """Check if backend is available"""
    try:
        response = requests.get(f"{url}/health", timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        return None

def display_results(result):
    """Display analysis results properly"""
    # Extract data correctly
    mode = result.get('mode', 'unknown')
    
    # Store for later use
    st.session_state.last_analysis = result
    
    if mode == 'online' and 'analysis' in result:
        # Online mode with analysis
        analysis = result['analysis']
        plant_type = analysis.get('plant_type', 'Unknown')
        disease = analysis.get('disease', 'Unknown')
        is_healthy = analysis.get('is_healthy', False)
        plant_confidence = analysis.get('plant_confidence', 0.0)
        disease_confidence = analysis.get('disease_confidence', 0.0)
        message = analysis.get('message', '')
        treatment = analysis.get('treatment', {})
    else:
        # Offline mode or direct response
        plant_type = result.get('plant_type', 'Unknown')
        disease = result.get('disease', 'Unknown')
        is_healthy = result.get('is_healthy', False)
        plant_confidence = result.get('plant_confidence', 0.0)
        disease_confidence = result.get('disease_confidence', 0.0)
        message = result.get('message', '')
        treatment = result.get('treatment', {})
    
    # Display success message
    st.markdown('<div class="success-box">', unsafe_allow_html=True)
    st.write("✅ **Analysis Complete!**")
    if message:
        st.write(f"**Finding:** {message}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Create columns for metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Capitalize plant type for better display
        display_plant = str(plant_type).capitalize() if plant_type != 'Unknown' else 'Unknown'
        confidence_text = f"{plant_confidence*100:.0f}%" if plant_confidence > 0 else ""
        st.metric("🌿 Plant Type", display_plant, confidence_text)
    
    with col2:
        # Format disease name
        display_disease = str(disease).replace('_', ' ').title() if disease != 'Unknown' else 'Unknown'
        confidence_text = f"{disease_confidence*100:.0f}%" if disease_confidence > 0 else ""
        st.metric("🔬 Disease/Condition", display_disease, confidence_text)
    
    with col3:
        status = "✅ Healthy" if is_healthy else "⚠️ Diseased"
        status_icon = "🟢" if is_healthy else "🔴"
        st.metric("📊 Health Status", f"{status_icon} {status}")
    
    with col4:
        mode_display = "🌐 Online" if mode == 'online' else "📡 Offline"
        st.metric("⚙️ Mode", mode_display)
    
    # Health status details
    if not is_healthy:
        st.markdown('<div class="warning-box">', unsafe_allow_html=True)
        st.write(f"⚠️ **Attention needed:** Your {display_plant} plant shows signs of **{display_disease}**.")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.write(f"🎉 **Good news!** Your {display_plant} plant appears to be **healthy**.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Display treatment recommendations
    if treatment and isinstance(treatment, dict) and any(treatment.values()):
        st.subheader("💊 Treatment Recommendations")
        
        # Create tabs for different treatment types
        tab1, tab2, tab3 = st.tabs(["🌱 Cultural Control", "🧪 Chemical Control", "🛡️ Preventive Measures"])
        
        with tab1:
            cultural = treatment.get('cultural', '')
            if cultural:
                if isinstance(cultural, list):
                    for i, item in enumerate(cultural, 1):
                        st.markdown(f'<div class="treatment-tab">{i}. {item}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="treatment-tab">{cultural}</div>', unsafe_allow_html=True)
            else:
                st.info("No cultural control recommendations available.")
        
        with tab2:
            chemical = treatment.get('chemical', '')
            if chemical:
                if isinstance(chemical, list):
                    for i, item in enumerate(chemical, 1):
                        st.markdown(f'<div class="treatment-tab">{i}. {item}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="treatment-tab">{chemical}</div>', unsafe_allow_html=True)
            else:
                st.info("No chemical control recommendations available.")
        
        with tab3:
            preventive = treatment.get('preventive', '')
            if preventive:
                if isinstance(preventive, list):
                    for i, item in enumerate(preventive, 1):
                        st.markdown(f'<div class="treatment-tab">{i}. {item}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="treatment-tab">{preventive}</div>', unsafe_allow_html=True)
            else:
                st.info("No preventive measures available.")
    
    # Display plant information based on type
    display_plant_info(display_plant)
    
    # Download options
    st.subheader("📥 Export Results")
    
    # Create JSON for download
    result_json = json.dumps(result, indent=2, ensure_ascii=False)
    
    # Create text summary
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    text_summary = f"""PLANT DISEASE ANALYSIS REPORT
{'=' * 40}
Date: {current_time}
Plant Type: {display_plant}
Disease/Condition: {display_disease}
Health Status: {'Healthy' if is_healthy else 'Diseased'}
Confidence: {plant_confidence*100:.1f}%
Analysis Mode: {mode}

FINDINGS:
{message}

TREATMENT RECOMMENDATIONS:
"""
    
    if treatment:
        for key, value in treatment.items():
            if value:
                text_summary += f"\n{key.upper()}:\n"
                if isinstance(value, list):
                    for item in value:
                        text_summary += f"  • {item}\n"
                else:
                    text_summary += f"  {value}\n"
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button(
            label="📄 Download JSON Report",
            data=result_json,
            file_name=f"plant_analysis_{current_time.replace(':', '-').replace(' ', '_')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col2:
        st.download_button(
            label="📝 Download Text Summary",
            data=text_summary,
            file_name=f"plant_summary_{current_time.replace(':', '-').replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True
        )

def display_plant_info(plant_type):
    """Display information about the detected plant"""
    plant_info = {
        "Tomato": {
            "description": "Tomato (Solanum lycopersicum) is a warm-season fruiting plant.",
            "common_varieties": ["Cherry", "Beefsteak", "Roma", "Heirloom"],
            "growing_season": "Spring to Fall",
            "ideal_temp": "21-27°C (70-80°F)",
            "watering": "Regular, deep watering (2-3 times per week)",
            "sunlight": "Full sun (6-8 hours daily)"
        },
        "Potato": {
            "description": "Potato (Solanum tuberosum) is a root vegetable that grows underground.",
            "common_varieties": ["Russet", "Yukon Gold", "Red", "Fingerling"],
            "growing_season": "Cool season crop",
            "ideal_temp": "15-20°C (60-68°F)",
            "watering": "Consistent moisture, avoid waterlogging",
            "sunlight": "Full sun"
        },
        "Corn": {
            "description": "Corn (Zea mays) is a tall cereal grass that produces kernels on ears.",
            "common_varieties": ["Sweet corn", "Field corn", "Popcorn"],
            "growing_season": "Warm season",
            "ideal_temp": "21-30°C (70-86°F)",
            "watering": "Regular watering, especially during tasseling",
            "sunlight": "Full sun"
        }
    }
    
    # Normalize plant type for comparison
    plant_lower = str(plant_type).lower()
    plant_key = None
    
    for key in plant_info.keys():
        if key.lower() == plant_lower:
            plant_key = key
            break
    
    if plant_key:
        info = plant_info[plant_key]
        with st.expander(f"🌱 About {plant_key} Plants"):
            st.write(f"**Description**: {info['description']}")
            
            st.write("**Common Varieties**:")
            for variety in info['common_varieties']:
                st.write(f"- {variety}")
            
            st.write(f"**Growing Season**: {info['growing_season']}")
            st.write(f"**Ideal Temperature**: {info['ideal_temp']}")
            st.write(f"**Watering Needs**: {info['watering']}")
            st.write(f"**Sunlight Requirements**: {info['sunlight']}")
    elif plant_type.lower() not in ['unknown', '']:
        with st.expander(f"🌱 About {plant_type.capitalize()} Plants"):
            st.write(f"**Description**: {plant_type.capitalize()} is a common agricultural plant.")
            st.write("**General Care Tips**:")
            st.write("- Ensure 6-8 hours of sunlight daily")
            st.write("- Water regularly based on soil moisture")
            st.write("- Monitor for pests and diseases")
            st.write("- Use appropriate fertilizers")
            st.write("- Maintain proper spacing for air circulation")

def main():
    # Header
    st.markdown('<h1 class="main-header">🌱 Plant Disease Classifier</h1>', unsafe_allow_html=True)
    st.markdown('<h3 class="sub-header">AI-powered plant health analysis system</h3>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.title("⚙️ Configuration")
        
        # Backend URL input
        backend_url = st.text_input(
            "Backend API URL",
            value=st.session_state.backend_url,
            help="Enter the URL where your FastAPI backend is running"
        )
        st.session_state.backend_url = backend_url
        
        # Connection test
        if st.button("🔗 Test Connection", use_container_width=True):
            with st.spinner("Checking connection..."):
                health = check_backend_health(backend_url)
                if health:
                    st.success("✅ Connected to backend!")
                    st.write(f"**Models Loaded**: {'Yes' if health.get('models_loaded') else 'No'}")
                    st.write(f"**TF Version**: {health.get('tensorflow_version', 'N/A')}")
                else:
                    st.error("❌ Cannot connect to backend")
                    st.info(f"Make sure backend is running at:\n`{backend_url}`")
        
        st.divider()
        
        # Mode selection
        st.subheader("Analysis Mode")
        analysis_mode = st.radio(
            "Select analysis mode:",
            ["Auto", "Online", "Offline"],
            index=0,
            help="Auto: Uses online if available, falls back to offline"
        )
        
        st.divider()
        
        # History
        st.subheader("📋 Recent Analysis")
        if st.session_state.predictions:
            for pred in reversed(st.session_state.predictions[-3:]):
                # Extract plant type properly
                plant = "Unknown"
                if pred.get('mode') == 'online' and 'analysis' in pred:
                    plant = pred['analysis'].get('plant_type', 'Unknown')
                else:
                    plant = pred.get('plant_type', 'Unknown')
                
                # Extract disease
                disease = "Unknown"
                if pred.get('mode') == 'online' and 'analysis' in pred:
                    disease = pred['analysis'].get('disease', 'Unknown')
                else:
                    disease = pred.get('disease', 'Unknown')
                
                status = "🟢" if pred.get('is_healthy', False) else "🔴"
                st.write(f"{status} {str(plant).capitalize()} - {str(disease).title()}")
        else:
            st.write("No analysis history yet")
        
        if st.session_state.predictions and st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.predictions = []
            st.rerun()
        
        st.divider()
        
        # Quick tips
        with st.expander("💡 Tips"):
            st.write("""
            - Use clear, well-lit images
            - Focus on affected leaves
            - Include scale reference if possible
            - Multiple angles help
            - Avoid blurry photos
            """)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📤 Upload Image")
        
        # File uploader with better styling
        st.markdown('<div class="upload-box">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Drag and drop or click to upload",
            type=['jpg', 'jpeg', 'png'],
            label_visibility="collapsed",
            help="Upload a clear image of plant leaves"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        if uploaded_file is not None:
            # Display image
            try:
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Image", use_column_width=True)
                
                # Image details
                with st.expander("📷 Image Details"):
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.write(f"**File Name**: {uploaded_file.name}")
                        st.write(f"**File Size**: {uploaded_file.size / 1024:.1f} KB")
                    with col_b:
                        st.write(f"**Dimensions**: {image.size[0]} × {image.size[1]} pixels")
                        st.write(f"**Format**: {image.format}")
            except Exception as e:
                st.error(f"Error loading image: {str(e)}")
                st.info("Please try uploading a different image file.")
    
    with col2:
        st.header("🔍 Analysis Results")
        
        if uploaded_file is not None:
            # Analyze button
            if st.button("🔬 Analyze Plant Health", type="primary", use_container_width=True):
                with st.spinner("Analyzing image. Please wait..."):
                    try:
                        # Prepare file for upload
                        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                        
                        # Send request to backend
                        response = requests.post(
                            f"{st.session_state.backend_url}/predict",
                            files=files,
                            timeout=45
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            
                            # Store in history
                            result['timestamp'] = datetime.now().isoformat()
                            st.session_state.predictions.append(result)
                            
                            # Display results
                            display_results(result)
                            
                        elif response.status_code == 503:
                            st.error("⚠️ Service Unavailable")
                            st.info("""
                            **Possible issues:**
                            1. Backend server is not running
                            2. No internet connection (for online mode)
                            3. Models failed to load (for offline mode)
                            
                            **Check:**
                            - Is the backend running?
                            - Do you have internet access?
                            - Check backend logs for errors
                            """)
                        else:
                            st.error(f"❌ Error {response.status_code}")
                            st.write(f"**Details**: {response.text[:200]}...")
                            
                    except requests.exceptions.ConnectionError as e:
                        st.error("🔌 Connection Error")
                        st.info(f"""
                        **Cannot connect to backend server at:**
                        ```
                        {st.session_state.backend_url}
                        ```
                        
                        **To start the backend:**
                        1. Open a new terminal
                        2. Navigate to your backend directory
                        3. Run:
                        ```bash
                        python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
                        ```
                        
                        **Or if using a different port:**
                        ```bash
                        python -m uvicorn app:app --reload --port 8001
                        ```
                        Then update the URL in the sidebar.
                        """)
                        
                    except requests.exceptions.Timeout:
                        st.error("⏱️ Request Timeout")
                        st.write("""
                        The analysis is taking too long. Try:
                        
                        1. **Use a smaller image** (under 1MB recommended)
                        2. **Check your internet connection** (for online mode)
                        3. **Try offline mode** if available
                        4. **Wait and try again** - server might be busy
                        """)
                        
                    except Exception as e:
                        st.error(f"💥 Unexpected Error")
                        st.write(f"**Error details**: {str(e)}")
                        st.write("""
                        **Troubleshooting steps:**
                        1. Check if backend is running
                        2. Verify the backend URL is correct
                        3. Try uploading a different image
                        4. Restart both frontend and backend
                        """)
        
        else:
            # Welcome/instructions
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.write("""
            ## 🚀 Welcome to Plant Disease Classifier
            
            **How to use:**
            1. **Upload** a plant leaf image on the left
            2. **Configure** backend URL if needed
            3. **Click Analyze** to start detection
            4. **Review** results and recommendations
            
            **Features:**
            - 🌐 **Online mode**: AI-powered analysis with treatment recommendations
            - 📡 **Offline mode**: Local model-based analysis
            - 💊 **Treatment plans**: Cultural, chemical, and preventive measures
            - 📥 **Export results**: Download JSON or text reports
            """)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Quick stats if available
            if st.session_state.predictions:
                total = len(st.session_state.predictions)
                healthy_count = 0
                
                for pred in st.session_state.predictions:
                    if pred.get('mode') == 'online' and 'analysis' in pred:
                        if pred['analysis'].get('is_healthy', False):
                            healthy_count += 1
                    elif pred.get('is_healthy', False):
                        healthy_count += 1
                
                diseased_count = total - healthy_count
                
                col_stats1, col_stats2, col_stats3 = st.columns(3)
                with col_stats1:
                    st.metric("📊 Total", total)
                with col_stats2:
                    st.metric("✅ Healthy", healthy_count)
                with col_stats3:
                    st.metric("⚠️ Diseased", diseased_count)
    
    # Footer
    st.divider()
    footer_cols = st.columns(4)
    with footer_cols[0]:
        st.write("**Version**: 1.0.0")
    with footer_cols[1]:
        st.write("**Backend**: FastAPI")
    with footer_cols[2]:
        st.write("**Frontend**: Streamlit")
    with footer_cols[3]:
        # Check connection status
        try:
            health = check_backend_health(st.session_state.backend_url)
            if health:
                st.write("**Status**: ✅ Connected")
            else:
                st.write("**Status**: ❌ Disconnected")
        except:
            st.write("**Status**: ❓ Unknown")

if __name__ == "__main__":
    main()