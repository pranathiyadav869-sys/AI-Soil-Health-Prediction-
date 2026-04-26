# """
# =============================================================
#  gradio_app.py
#  Interactive web UI for Soil Health Prediction
#  Run: python gradio_app.py
#  Install: pip install gradio pillow
# =============================================================
# """

# import json
# import gradio as gr
# import numpy as np
# from decision_support import SoilProfile, generate_full_report

# # If you have a trained model, import the predictor:
# # from inference import SoilHealthPredictor
# # predictor = SoilHealthPredictor("best_soil_model.pt", "scalers.pkl")

# # For demo without model, we use rule-based output with placeholder SHI
# def compute_shi_placeholder(N, P, K, pH, organic_carbon):
#     """Simple heuristic SHI when model checkpoint not available."""
#     n_norm  = min(N / 140, 1.0)
#     p_norm  = min(P / 145, 1.0)
#     k_norm  = min(K / 200, 1.0)
#     ph_norm = 1.0 - abs(pH - 6.5) / 3.5
#     oc_norm = min(organic_carbon / 20, 1.0)
#     shi = 0.3 * ph_norm + 0.2 * n_norm + 0.15 * p_norm + 0.15 * k_norm + 0.2 * oc_norm
#     return float(np.clip(shi, 0.0, 1.0))


# def predict_fn(N, P, K, pH, rainfall, temperature, humidity,
#                organic_carbon, sand, image):
#     """Main Gradio prediction function."""
#     shi = compute_shi_placeholder(N, P, K, pH, organic_carbon)
#     soil_class = "Poor" if shi < 0.35 else "Moderate" if shi < 0.50 else "Healthy"

#     profile = SoilProfile(
#         N=N, P=P, K=K, pH=pH,
#         rainfall=rainfall, temperature=temperature,
#         humidity=humidity, organic_carbon=organic_carbon, sand=sand,
#         shi=shi, soil_class=soil_class,
#     )
#     report = generate_full_report(profile)

#     # Format for display
#     sa = report["soil_assessment"]
#     shi_display = f"**SHI:** {sa['soil_health_index']:.4f}  |  **Class:** {sa['soil_class']}"
#     assessment  = sa["interpretation"]

#     crops = report["crop_recommendations"]
#     crop_text = "\n".join([
#         f"{i+1}. **{c['crop']}** — {c['suitability']} ({c['score_pct']}%)"
#         for i, c in enumerate(crops)
#     ]) if crops else "No suitable crops. Remediate soil first."

#     fert = report["fertilizer_advice"]
#     fert_text = "\n".join(f"• {r}" for r in fert["recommendations"])

#     irr = report["irrigation_advice"]
#     irr_text = (f"**Level:** {irr['irrigation_level']}\n"
#                 f"**Frequency:** {irr['frequency']}\n"
#                 f"{irr['advice']}")

#     json_output = json.dumps(report, indent=2)

#     return shi_display, assessment, crop_text, fert_text, irr_text, json_output


# # ── Build Gradio UI ───────────────────────────────────────────────
# with gr.Blocks(title="🌱 Soil Health AI", theme=gr.themes.Soft()) as demo:
#     gr.Markdown("# 🌱 Multimodal Soil Health Prediction System")
#     gr.Markdown("Enter soil and weather data to get crop recommendations and advisory.")

#     with gr.Row():
#         with gr.Column():
#             gr.Markdown("### 🧪 Soil Nutrients")
#             N  = gr.Slider(0, 140, value=50, label="Nitrogen (N) kg/ha")
#             P  = gr.Slider(5, 145, value=50, label="Phosphorus (P) kg/ha")
#             K  = gr.Slider(5, 200, value=50, label="Potassium (K) kg/ha")
#             pH = gr.Slider(3.0, 10.0, value=6.5, step=0.1, label="Soil pH")
#             OC = gr.Slider(0.5, 94, value=10, step=0.5, label="Organic Carbon (%)")
#             SD = gr.Slider(4, 96, value=50, step=1, label="Sand Content (%)")

#         with gr.Column():
#             gr.Markdown("### 🌤️ Weather & Climate")
#             RF  = gr.Slider(0, 300, value=100, label="Rainfall (mm)")
#             TMP = gr.Slider(0, 50, value=25, step=0.5, label="Temperature (°C)")
#             HUM = gr.Slider(10, 100, value=60, label="Humidity (%)")
#             gr.Markdown("### 🖼️ Soil/Crop Image (optional)")
#             IMG = gr.Image(type="pil", label="Upload Image")

#     btn = gr.Button("🔍 Analyse Soil", variant="primary")

#     with gr.Row():
#         shi_out  = gr.Markdown(label="Soil Health")
#         assess   = gr.Textbox(label="Assessment", lines=2)

#     with gr.Row():
#         crops_out = gr.Markdown(label="🌾 Crop Recommendations")
#         fert_out  = gr.Textbox(label="🧪 Fertilizer Advice", lines=6)
#         irr_out   = gr.Markdown(label="💧 Irrigation Advice")

#     json_out = gr.Code(label="Full JSON Output", language="json")

#     btn.click(
#         fn=predict_fn,
#         inputs=[N, P, K, pH, RF, TMP, HUM, OC, SD, IMG],
#         outputs=[shi_out, assess, crops_out, fert_out, irr_out, json_out],
#     )

#     gr.Markdown("""
#     ---
#     **Crop Image Gallery** — To display crop images in the UI:
#     1. Store images in `static/crops/<CropName>.jpg`
#     2. Use `gr.Gallery` component with paths returned from crop recommendations
#     3. Alternatively, fetch from Wikipedia Commons API by crop name
#     """)

# if __name__ == "__main__":
#     demo.launch(share=True)   # share=True gives a public URL
# =============================================================
# 🌱 Enhanced Gradio UI - Soil Health Prediction
# =============================================================

# import json
# import gradio as gr
# import numpy as np
# from decision_support import SoilProfile, generate_full_report

# # ------------------------------
# # SHI Calculation (Placeholder)
# # ------------------------------
# def compute_shi_placeholder(N, P, K, pH, organic_carbon):
#     n_norm  = min(N / 140, 1.0)
#     p_norm  = min(P / 145, 1.0)
#     k_norm  = min(K / 200, 1.0)
#     ph_norm = 1.0 - abs(pH - 6.5) / 3.5
#     oc_norm = min(organic_carbon / 20, 1.0)

#     shi = (
#         0.3 * ph_norm +
#         0.2 * n_norm +
#         0.15 * p_norm +
#         0.15 * k_norm +
#         0.2 * oc_norm
#     )

#     return float(np.clip(shi, 0.0, 1.0))


# # ------------------------------
# # SHI Status Color
# # ------------------------------
# def get_shi_color(shi):
#     if shi < 0.35:
#         return "🔴 Poor"
#     elif shi < 0.5:
#         return "🟡 Moderate"
#     else:
#         return "🟢 Healthy"


# # ------------------------------
# # Main Prediction Function
# # ------------------------------
# def predict_fn(N, P, K, pH, rainfall, temperature, humidity,
#                organic_carbon, sand, image):

#     # Compute SHI
#     shi = compute_shi_placeholder(N, P, K, pH, organic_carbon)
#     soil_class = get_shi_color(shi)

#     # Create profile
#     profile = SoilProfile(
#         N=N, P=P, K=K, pH=pH,
#         rainfall=rainfall, temperature=temperature,
#         humidity=humidity, organic_carbon=organic_carbon, sand=sand,
#         shi=shi, soil_class=soil_class,
#     )

#     # Generate report
#     report = generate_full_report(profile)

#     # ------------------------------
#     # Output Formatting
#     # ------------------------------
#     shi_display = f"""
# ## 🌱 Soil Health Index: **{shi:.3f}**
# ### Status: {soil_class}
# """

#     # Crop recommendations
#     crops = report.get("crop_recommendations", [])
#     if crops:
#         crop_text = "\n".join([
#             f"🌾 **{c['crop']}** → {c['score_pct']}% ({c['suitability']})"
#             for c in crops
#         ])
#     else:
#         crop_text = "No suitable crops. Improve soil health."

#     # Fertilizer advice
#     fert = report.get("fertilizer_advice", {})
#     fert_text = "\n".join([
#         f"• {r}" for r in fert.get("recommendations", [])
#     ])

#     # Irrigation advice
#     irr = report.get("irrigation_advice", {})
#     irr_text = f"""
# 💧 **Level:** {irr.get('irrigation_level', '-')}

# 📅 **Frequency:** {irr.get('frequency', '-')}

# 📝 {irr.get('advice', '-')}
# """

#     return shi_display, crop_text, fert_text, irr_text


# # =============================================================
# # 🎨 UI Layout
# # =============================================================

# with gr.Blocks(theme=gr.themes.Soft(primary_hue="green")) as demo:

#     gr.Markdown("# 🌱 AI Soil Health Advisor")
#     gr.Markdown("### Smart Farming Decision System")

#     with gr.Row():
#         with gr.Column():
#             gr.Markdown("### 🧪 Soil Inputs")

#             N = gr.Slider(0, 140, value=50, label="Nitrogen (N)")
#             P = gr.Slider(5, 145, value=50, label="Phosphorus (P)")
#             K = gr.Slider(5, 200, value=50, label="Potassium (K)")
#             pH = gr.Slider(3, 10, value=6.5, step=0.1, label="Soil pH")
#             OC = gr.Slider(0.5, 20, value=5, step=0.5, label="Organic Carbon")
#             SD = gr.Slider(4, 96, value=50, step=1, label="Sand Content")

#         with gr.Column():
#             gr.Markdown("### 🌤️ Weather")

#             RF = gr.Slider(0, 300, value=100, label="Rainfall (mm)")
#             TMP = gr.Slider(0, 50, value=25, step=0.5, label="Temperature (°C)")
#             HUM = gr.Slider(10, 100, value=60, label="Humidity (%)")

#             gr.Markdown("### 🖼️ Soil/Crop Image (optional)")
#             IMG = gr.Image(type="pil", label="Upload Image")

#     # Button
#     btn = gr.Button("🚀 Analyze Soil", size="lg")

#     gr.Markdown("---")

#     # Outputs
#     shi_out = gr.Markdown()
#     crops_out = gr.Markdown()
#     fert_out = gr.Markdown()
#     irr_out = gr.Markdown()

#     # Button action
#     btn.click(
#         fn=predict_fn,
#         inputs=[N, P, K, pH, RF, TMP, HUM, OC, SD, IMG],
#         outputs=[shi_out, crops_out, fert_out, irr_out]
#     )

# # Launch app
# demo.launch(share=True)

# =============================================================
# 🌱 Advanced Gradio UI - Soil Health Prediction System
# =============================================================
# good
# import gradio as gr
# import numpy as np
# import plotly.graph_objects as go
# import plotly.express as px
# from decision_support import SoilProfile, generate_full_report

# # ------------------------------
# # SHI Calculation (Placeholder)
# # ------------------------------
# def compute_shi_placeholder(N, P, K, pH, organic_carbon):
#     n_norm  = min(N / 140, 1.0)
#     p_norm  = min(P / 145, 1.0)
#     k_norm  = min(K / 200, 1.0)
#     ph_norm = 1.0 - abs(pH - 6.5) / 3.5
#     oc_norm = min(organic_carbon / 20, 1.0)

#     shi = (
#         0.3 * ph_norm +
#         0.2 * n_norm +
#         0.15 * p_norm +
#         0.15 * k_norm +
#         0.2 * oc_norm
#     )

#     return float(np.clip(shi, 0.0, 1.0))


# # ------------------------------
# # SHI Gauge (Plotly)
# # ------------------------------
# def create_shi_gauge(shi):
#     fig = go.Figure(go.Indicator(
#         mode="gauge+number",
#         value=shi,
#         title={'text': "Soil Health Index"},
#         gauge={
#             'axis': {'range': [0, 1]},
#             'steps': [
#                 {'range': [0, 0.35], 'color': "red"},
#                 {'range': [0.35, 0.5], 'color': "yellow"},
#                 {'range': [0.5, 1], 'color': "green"},
#             ]
#         }
#     ))
#     fig.update_layout(height=300)
#     return fig


# # ------------------------------
# # NDVI Plot
# # ------------------------------
# def create_ndvi_plot():
#     ndvi_values = [0.4, 0.5, 0.6, 0.55, 0.65, 0.7, 0.68, 0.72]  # placeholder
#     fig = px.line(
#         x=list(range(1, 9)),
#         y=ndvi_values,
#         labels={'x': 'Time Step', 'y': 'NDVI'},
#         title="NDVI Trend Over Time"
#     )
#     return fig


# # ------------------------------
# # Location-Based Suggestions
# # ------------------------------
# def get_location_advice(lat, lon):
#     if lat > 20:
#         return "🌾 Suitable for Wheat, Mustard (cool regions)"
#     elif lat > 10:
#         return "🌽 Suitable for Maize, Rice (moderate climate)"
#     else:
#         return "🌴 Suitable for Coconut, Sugarcane (tropical region)"


# # ------------------------------
# # Prediction Function
# # ------------------------------
# def predict_fn(N, P, K, pH, rainfall, temperature, humidity,
#                organic_carbon, sand, image, lat, lon):

#     shi = compute_shi_placeholder(N, P, K, pH, organic_carbon)

#     soil_class = "Poor" if shi < 0.35 else "Moderate" if shi < 0.5 else "Healthy"

#     profile = SoilProfile(
#         N=N, P=P, K=K, pH=pH,
#         rainfall=rainfall, temperature=temperature,
#         humidity=humidity, organic_carbon=organic_carbon, sand=sand,
#         shi=shi, soil_class=soil_class,
#     )

#     report = generate_full_report(profile)

#     # ---------------- Outputs ----------------
#     shi_text = f"## 🌱 SHI: {shi:.3f} ({soil_class})"

#     crops = report.get("crop_recommendations", [])
#     crop_text = "\n".join([
#         f"🌾 {c['crop']} → {c['score_pct']}%"
#         for c in crops
#     ])

#     fert = report.get("fertilizer_advice", {})
#     fert_text = "\n".join(f"• {r}" for r in fert.get("recommendations", []))

#     irr = report.get("irrigation_advice", {})
#     irr_text = f"""
# 💧 Level: {irr.get('irrigation_level')}
# 📅 Frequency: {irr.get('frequency')}
# 📝 {irr.get('advice')}
# """

#     # Visuals
#     gauge = create_shi_gauge(shi)
#     ndvi_plot = create_ndvi_plot()
#     loc_text = get_location_advice(lat, lon)

#     return shi_text, gauge, ndvi_plot, loc_text, crop_text, fert_text, irr_text


# # =============================================================
# # 🎨 UI Layout
# # =============================================================

# with gr.Blocks(theme=gr.themes.Soft(primary_hue="green")) as demo:

#     gr.Markdown("# 🌱 Multimodal Soil Health Prediction System")
#     gr.Markdown("### AI-powered smart farming assistant")

#     with gr.Row():
#         with gr.Column():
#             gr.Markdown("### 🧪 Soil Inputs")
#             N = gr.Slider(0, 140, 50, label="Nitrogen")
#             P = gr.Slider(5, 145, 50, label="Phosphorus")
#             K = gr.Slider(5, 200, 50, label="Potassium")
#             pH = gr.Slider(3, 10, 6.5, label="pH")
#             OC = gr.Slider(0.5, 20, 5, label="Organic Carbon")
#             SD = gr.Slider(4, 96, 50, label="Sand")

#         with gr.Column():
#             gr.Markdown("### 🌤️ Weather")
#             RF = gr.Slider(0, 300, 100, label="Rainfall")
#             TMP = gr.Slider(0, 50, 25, label="Temperature")
#             HUM = gr.Slider(10, 100, 60, label="Humidity")

#             gr.Markdown("### 📍 Location")
#             LAT = gr.Slider(-90, 90, 20, label="Latitude")
#             LON = gr.Slider(-180, 180, 78, label="Longitude")

#             IMG = gr.Image(label="Upload Image (optional)")

#     btn = gr.Button("🚀 Analyze Soil")

#     gr.Markdown("---")

#     shi_out = gr.Markdown()
#     gauge_out = gr.Plot(label="📊 SHI Gauge")
#     ndvi_out = gr.Plot(label="🌡️ NDVI Trend")
#     loc_out = gr.Markdown(label="📍 Location Advice")

#     crops_out = gr.Markdown(label="🌾 Crops")
#     fert_out = gr.Markdown(label="🧪 Fertilizer")
#     irr_out = gr.Markdown(label="💧 Irrigation")

#     btn.click(
#         fn=predict_fn,
#         inputs=[N, P, K, pH, RF, TMP, HUM, OC, SD, IMG, LAT, LON],
#         outputs=[shi_out, gauge_out, ndvi_out, loc_out, crops_out, fert_out, irr_out]
#     )

# demo.launch(share=True)
# 3rd
# # =============================================================
# # 🌱 FINAL POLISHED UI - Soil Health AI (Cards + Badges + PDF)
# # =============================================================

# import gradio as gr
# import numpy as np
# import plotly.graph_objects as go
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
# from reportlab.lib.styles import getSampleStyleSheet
# from decision_support import SoilProfile, generate_full_report


# # ------------------------------
# # SHI Calculation
# # ------------------------------
# def compute_shi_placeholder(N, P, K, pH, organic_carbon):
#     n = min(N/140, 1)
#     p = min(P/145, 1)
#     k = min(K/200, 1)
#     ph = 1 - abs(pH - 6.5)/3.5
#     oc = min(organic_carbon/20, 1)

#     shi = 0.3*ph + 0.2*n + 0.15*p + 0.15*k + 0.2*oc
#     return float(np.clip(shi, 0, 1))


# # ------------------------------
# # Gauge Chart
# # ------------------------------
# def create_gauge(shi):
#     fig = go.Figure(go.Indicator(
#         mode="gauge+number",
#         value=shi,
#         title={'text': "Soil Health Index"},
#         gauge={
#             'axis': {'range': [0,1]},
#             'steps': [
#                 {'range':[0,0.35],'color':"#ff4d4d"},
#                 {'range':[0.35,0.5],'color':"#ffd633"},
#                 {'range':[0.5,1],'color':"#66ff66"},
#             ]
#         }
#     ))
#     fig.update_layout(height=300)
#     return fig


# # ------------------------------
# # Colored Card HTML
# # ------------------------------
# def make_card(title, content, color):
#     return f"""
# <div style="
# padding:15px;
# border-radius:12px;
# background-color:{color};
# margin:10px 0;
# box-shadow:0 4px 10px rgba(0,0,0,0.1);
# ">
# <h3>{title}</h3>
# {content}
# </div>
# """


# # ------------------------------
# # PDF Report Generator
# # ------------------------------
# def generate_pdf(report):
#     file = "soil_report.pdf"
#     styles = getSampleStyleSheet()
#     doc = SimpleDocTemplate(file)

#     content = []
#     content.append(Paragraph("Soil Health Report", styles['Title']))
#     content.append(Spacer(1,10))

#     for key, value in report.items():
#         content.append(Paragraph(f"<b>{key}</b>", styles['Heading2']))
#         content.append(Paragraph(str(value), styles['Normal']))
#         content.append(Spacer(1,10))

#     doc.build(content)
#     return file


# # ------------------------------
# # MAIN FUNCTION
# # ------------------------------
# def predict_fn(N,P,K,pH,RF,TMP,HUM,OC,SD,IMG):

#     shi = compute_shi_placeholder(N,P,K,pH,OC)

#     if shi < 0.35:
#         status = "🔴 Poor"
#         color = "#ffe6e6"
#     elif shi < 0.5:
#         status = "🟡 Moderate"
#         color = "#fff5cc"
#     else:
#         status = "🟢 Healthy"
#         color = "#e6ffe6"

#     profile = SoilProfile(
#         N=N,P=P,K=K,pH=pH,
#         rainfall=RF,temperature=TMP,humidity=HUM,
#         organic_carbon=OC,sand=SD,
#         shi=shi,soil_class=status
#     )

#     report = generate_full_report(profile)

#     # ---------------- UI Formatting ----------------

#     shi_card = make_card(
#         "🌱 Soil Health",
#         f"<h2>SHI: {shi:.3f}</h2><b>{status}</b>",
#         color
#     )

#     crops = report.get("crop_recommendations", [])
#     crop_html = ""
#     for c in crops:
#         crop_html += f"""
#         <p>🌾 <b>{c['crop']}</b> — {c['score_pct']}% ({c['suitability']})</p>
#         """

#     crop_card = make_card("🌾 Crop Recommendations", crop_html, "#eef")

#     fert = report.get("fertilizer_advice", {})
#     fert_html = ""
#     for r in fert.get("recommendations", []):
#         fert_html += f"<p>🧪 {r}</p>"

#     fert_card = make_card("🧪 Fertilizer Advice", fert_html, "#f9f9f9")

#     irr = report.get("irrigation_advice", {})
#     irr_card = make_card(
#         "💧 Irrigation Plan",
#         f"""
#         <p><b>Level:</b> {irr.get('irrigation_level')}</p>
#         <p><b>Frequency:</b> {irr.get('frequency')}</p>
#         <p>{irr.get('advice')}</p>
#         """,
#         "#eef9ff"
#     )

#     gauge = create_gauge(shi)
#     pdf_file = generate_pdf(report)

#     return shi_card, gauge, crop_card, fert_card, irr_card, pdf_file


# # =============================================================
# # UI DESIGN
# # =============================================================

# with gr.Blocks(theme=gr.themes.Soft(primary_hue="green")) as demo:

#     gr.Markdown("# 🌱 AI Soil Health Advisor")
#     gr.Markdown("### Smart Farming Decision System")

#     with gr.Row():
#         with gr.Column():
#             N = gr.Slider(0,140,50,label="Nitrogen")
#             P = gr.Slider(5,145,50,label="Phosphorus")
#             K = gr.Slider(5,200,50,label="Potassium")
#             pH = gr.Slider(3,10,6.5,label="pH")
#             OC = gr.Slider(0.5,20,5,label="Organic Carbon")
#             SD = gr.Slider(4,96,50,label="Sand")

#         with gr.Column():
#             RF = gr.Slider(0,300,100,label="Rainfall")
#             TMP = gr.Slider(0,50,25,label="Temperature")
#             HUM = gr.Slider(10,100,60,label="Humidity")
#             IMG = gr.Image(label="Upload Image")

#     btn = gr.Button("🚀 Analyze Soil")

#     gr.Markdown("---")

#     shi_out = gr.HTML()
#     gauge_out = gr.Plot()
#     crop_out = gr.HTML()
#     fert_out = gr.HTML()
#     irr_out = gr.HTML()
#     pdf_out = gr.File(label="📄 Download Report")

#     btn.click(
#         fn=predict_fn,
#         inputs=[N,P,K,pH,RF,TMP,HUM,OC,SD,IMG],
#         outputs=[shi_out,gauge_out,crop_out,fert_out,irr_out,pdf_out]
#     )

# demo.launch(share=True)
#=============================================================
#🌱 FINAL ALL-IN-ONE SOIL HEALTH AI SYSTEM map
#=============================================================

# import gradio as gr
# import numpy as np
# import plotly.graph_objects as go
# import plotly.express as px
# import folium

# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
# from reportlab.lib.styles import getSampleStyleSheet

# from decision_support import SoilProfile, generate_full_report


# # ------------------------------
# # SHI Calculation
# # ------------------------------
# def compute_shi(N, P, K, pH, OC):
#     n = min(N/140, 1)
#     p = min(P/145, 1)
#     k = min(K/200, 1)
#     ph = 1 - abs(pH - 6.5)/3.5
#     oc = min(OC/20, 1)
#     return float(np.clip(0.3*ph + 0.2*n + 0.15*p + 0.15*k + 0.2*oc, 0, 1))


# # ------------------------------
# # Gauge
# # ------------------------------
# def create_gauge(shi):
#     fig = go.Figure(go.Indicator(
#         mode="gauge+number",
#         value=shi,
#         title={'text': "Soil Health Index"},
#         gauge={
#             'axis': {'range': [0,1]},
#             'steps': [
#                 {'range':[0,0.35],'color':"red"},
#                 {'range':[0.35,0.5],'color':"yellow"},
#                 {'range':[0.5,1],'color':"green"},
#             ]
#         }
#     ))
#     return fig


# # ------------------------------
# # NDVI
# # ------------------------------
# def get_ndvi(lat):
#     base = 0.4 + (lat % 10)/50
#     return [base + i*0.04 for i in range(8)]

# def ndvi_plot(ndvi):
#     return px.line(x=list(range(1,9)), y=ndvi, title="NDVI Trend")


# # ------------------------------
# # Map
# # ------------------------------
# def create_map(lat, lon):
#     m = folium.Map(location=[lat, lon], zoom_start=6)
#     folium.Marker([lat, lon], tooltip="Location").add_to(m)
#     return m._repr_html_()


# # ------------------------------
# # Image analysis (safe demo)
# # ------------------------------
# def analyze_image(img):
#     if img is None:
#         return "📸 No image provided"
#     return "📸 Soil texture analyzed (demo)"


# # ------------------------------
# # Cards
# # ------------------------------
# def card(title, content, color):
#     return f"""
# <div style="padding:15px;border-radius:10px;background:{color};margin:10px 0;">
# <h3>{title}</h3>
# {content}
# </div>
# """


# # ------------------------------
# # PDF
# # ------------------------------
# def generate_pdf(report):
#     file = "report.pdf"
#     doc = SimpleDocTemplate(file)
#     styles = getSampleStyleSheet()

#     content = []
#     content.append(Paragraph("Soil Health Report", styles['Title']))
#     content.append(Spacer(1,10))

#     for k,v in report.items():
#         content.append(Paragraph(f"<b>{k}</b>", styles['Heading2']))
#         content.append(Paragraph(str(v), styles['Normal']))
#         content.append(Spacer(1,10))

#     doc.build(content)
#     return file


# # ------------------------------
# # MAIN FUNCTION
# # ------------------------------
# def predict_fn(N,P,K,pH,RF,TMP,HUM,OC,SD,IMG,LAT,LON):

#     shi = compute_shi(N,P,K,pH,OC)

#     if shi < 0.35:
#         status = "🔴 Poor"
#         color = "#ffe6e6"
#     elif shi < 0.5:
#         status = "🟡 Moderate"
#         color = "#fff5cc"
#     else:
#         status = "🟢 Healthy"
#         color = "#e6ffe6"

#     profile = SoilProfile(
#         N=N,P=P,K=K,pH=pH,
#         rainfall=RF,temperature=TMP,humidity=HUM,
#         organic_carbon=OC,sand=SD,
#         shi=shi,soil_class=status
#     )

#     report = generate_full_report(profile)

#     # ---------------- UI ----------------
#     shi_card = card("🌱 Soil Health", f"<h2>{shi:.3f}</h2><b>{status}</b>", color)

#     crops = report.get("crop_recommendations", [])
#     crop_html = "".join([f"<p>🌾 {c['crop']} - {c['score_pct']}%</p>" for c in crops])
#     crop_card = card("🌾 Crops", crop_html, "#eef")

#     fert = report.get("fertilizer_advice", {})
#     fert_html = "".join([f"<p>🧪 {r}</p>" for r in fert.get("recommendations", [])])
#     fert_card = card("🧪 Fertilizer", fert_html, "#f9f9f9")

#     irr = report.get("irrigation_advice", {})
#     irr_card = card("💧 Irrigation",
#                     f"<p>{irr.get('irrigation_level')}</p><p>{irr.get('frequency')}</p><p>{irr.get('advice')}</p>",
#                     "#eef9ff")

#     gauge = create_gauge(shi)
#     ndvi = ndvi_plot(get_ndvi(LAT))
#     map_html = create_map(LAT, LON)
#     img_text = analyze_image(IMG)
#     pdf = generate_pdf(report)

#     return shi_card, gauge, ndvi, map_html, crop_card, fert_card, irr_card, img_text, pdf


# # =============================================================
# # UI
# # =============================================================

# with gr.Blocks() as demo:

#     gr.Markdown("# 🌱 Soil Health AI System")

#     with gr.Row():
#         with gr.Column():
#             N = gr.Slider(0,140,50,label="Nitrogen")
#             P = gr.Slider(5,145,50,label="Phosphorus")
#             K = gr.Slider(5,200,50,label="Potassium")
#             pH = gr.Slider(3,10,6.5,label="pH")
#             OC = gr.Slider(0.5,20,5,label="Organic Carbon")
#             SD = gr.Slider(4,96,50,label="Sand")

#         with gr.Column():
#             RF = gr.Slider(0,300,100,label="Rainfall")
#             TMP = gr.Slider(0,50,25,label="Temp")
#             HUM = gr.Slider(10,100,60,label="Humidity")
#             LAT = gr.Slider(-90,90,20,label="Latitude")
#             LON = gr.Slider(-180,180,78,label="Longitude")
#             IMG = gr.Image(label="Upload Image")

#     btn = gr.Button("🚀 Analyze")

#     shi_out = gr.HTML()
#     gauge_out = gr.Plot()
#     ndvi_out = gr.Plot()
#     map_out = gr.HTML()

#     crop_out = gr.HTML()
#     fert_out = gr.HTML()
#     irr_out = gr.HTML()

#     img_out = gr.Markdown()
#     pdf_out = gr.File()

#     btn.click(
#         fn=predict_fn,
#         inputs=[N,P,K,pH,RF,TMP,HUM,OC,SD,IMG,LAT,LON],
#         outputs=[shi_out,gauge_out,ndvi_out,map_out,crop_out,fert_out,irr_out,img_out,pdf_out]
#     )

# demo.launch(share=True)
"""
=============================================================
 app.py  (UPDATED)
 
 Your existing Gradio app with the new image analysis module
 fully integrated. Changes from old app.py are marked ── NEW ──

 HOW TO RUN IN VS CODE:
   1. Copy soil_image_model.pt + soil_image_labels.json
      into this folder (download from Colab)
   2. pip install gradio torch torchvision plotly folium reportlab
   3. python app.py
=============================================================
"""

# import os
# import gradio as gr
# import numpy as np
# import plotly.graph_objects as go
# import plotly.express as px
# import folium
# from PIL import Image

# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib import colors

# from decision_support import SoilProfile, generate_full_report

# # ── NEW ── Import the image analyzer
# from image_inference import SoilImageAnalyzer

# # ─────────────────────────────────────────────────────
# # ── NEW ── Load image model at startup (once)
# # ─────────────────────────────────────────────────────
# MODEL_PATH = "soil_image_model.pt"
# LABEL_PATH = "soil_image_labels.json"

# _analyzer = None   # lazy-loaded to avoid crash if model not present

# def get_analyzer():
#     global _analyzer
#     if _analyzer is None:
#         if os.path.exists(MODEL_PATH):
#             _analyzer = SoilImageAnalyzer(
#                 model_path=MODEL_PATH,
#                 label_path=LABEL_PATH if os.path.exists(LABEL_PATH) else None,
#                 device="cpu",   # change to "cuda" if GPU available
#             )
#             print("✅ Image model loaded")
#         else:
#             print(f"⚠️  {MODEL_PATH} not found — image analysis will use demo mode")
#     return _analyzer


# # ─────────────────────────────────────────────────────
# # SHI Calculation (unchanged)
# # ─────────────────────────────────────────────────────
# def compute_shi(N, P, K, pH, OC):
#     n  = min(N / 140, 1)
#     p  = min(P / 145, 1)
#     k  = min(K / 200, 1)
#     ph = 1 - abs(pH - 6.5) / 3.5
#     oc = min(OC / 20, 1)
#     return float(np.clip(0.3 * ph + 0.2 * n + 0.15 * p + 0.15 * k + 0.2 * oc, 0, 1))


# # ─────────────────────────────────────────────────────
# # Gauge (unchanged)
# # ─────────────────────────────────────────────────────
# def create_gauge(shi):
#     fig = go.Figure(go.Indicator(
#         mode="gauge+number",
#         value=shi,
#         title={"text": "Soil Health Index"},
#         gauge={
#             "axis": {"range": [0, 1]},
#             "steps": [
#                 {"range": [0, 0.35], "color": "red"},
#                 {"range": [0.35, 0.5], "color": "yellow"},
#                 {"range": [0.5, 1],   "color": "green"},
#             ],
#         }
#     ))
#     return fig


# # ─────────────────────────────────────────────────────
# # NDVI (unchanged)
# # ─────────────────────────────────────────────────────
# def get_ndvi(lat):
#     base = 0.4 + (lat % 10) / 50
#     return [round(base + i * 0.04, 3) for i in range(8)]


# def ndvi_plot(ndvi):
#     return px.line(
#         x=list(range(1, 9)), y=ndvi,
#         title="NDVI Trend (8-step temporal)",
#         labels={"x": "Time Step", "y": "NDVI"},
#     )


# # ─────────────────────────────────────────────────────
# # Map (unchanged)
# # ─────────────────────────────────────────────────────
# def create_map(lat, lon):
#     m = folium.Map(location=[lat, lon], zoom_start=6)
#     folium.Marker([lat, lon], tooltip="Soil Location").add_to(m)
#     return m._repr_html_()


# # ─────────────────────────────────────────────────────
# # Card helper (unchanged)
# # ─────────────────────────────────────────────────────
# def card(title, content, color):
#     return f"""
# <div style="padding:15px;border-radius:10px;background:{color};
#             margin:10px 0;border:1px solid #ddd;">
#   <h3 style="margin-top:0">{title}</h3>
#   {content}
# </div>"""


# # ─────────────────────────────────────────────────────
# # ── NEW ── Image Analysis Function
# # ─────────────────────────────────────────────────────
# def analyze_image(img):
#     """
#     Called by the Gradio app when the user uploads an image.
    
#     Returns:
#       html_output  – styled card for gr.HTML component
#       explanation  – plain text for gr.Markdown component
#     """
#     analyzer = get_analyzer()

#     if img is None:
#         placeholder = """
# <div style="padding:15px;border-radius:10px;background:#f5f5f5;border:1px solid #ddd">
#   <h3>📸 Image Analysis</h3>
#   <p>Upload a soil or crop image to get AI-powered analysis including:</p>
#   <ul>
#     <li>🪨 Soil type classification</li>
#     <li>💧 Moisture condition</li>
#     <li>🌿 Vegetation presence</li>
#     <li>🌾 Crop health condition</li>
#     <li>🦠 Disease detection</li>
#   </ul>
# </div>"""
#         return placeholder, "📸 No image uploaded yet."

#     if analyzer is None:
#         # Demo mode when model file not found
#         demo_html = """
# <div style="padding:15px;border-radius:10px;background:#fff3cd;border:1px solid #ffc107">
#   <h3>⚠️ Demo Mode</h3>
#   <p><b>soil_image_model.pt not found.</b></p>
#   <p>Train the model using <code>image_model_train_colab.py</code> in Google Colab,
#      then download <code>soil_image_model.pt</code> and place it in this folder.</p>
#   <p>Image received: ✅ ({} x {} px)</p>
# </div>""".format(
#             img.shape[1] if hasattr(img, 'shape') else "?",
#             img.shape[0] if hasattr(img, 'shape') else "?",
#         )
#         return demo_html, "⚠️ Model not loaded. See HTML panel for instructions."

#     # Run real inference
#     result = analyzer.analyze(img)
#     return result["html"], result["explanation"]


# # ─────────────────────────────────────────────────────
# # PDF Report (updated to include image results)
# # ─────────────────────────────────────────────────────
# def generate_pdf(report, image_explanation=""):
#     file_path = "soil_health_report.pdf"
#     doc = SimpleDocTemplate(file_path)
#     styles = getSampleStyleSheet()
#     content = []

#     content.append(Paragraph("🌱 Soil Health & Crop Advisory Report", styles["Title"]))
#     content.append(Spacer(1, 12))

#     # Soil assessment section
#     sa = report.get("soil_assessment", {})
#     content.append(Paragraph("Soil Health Assessment", styles["Heading2"]))
#     content.append(Paragraph(f"Soil Health Index (SHI): {sa.get('soil_health_index', 'N/A')}", styles["Normal"]))
#     content.append(Paragraph(f"Classification: {sa.get('soil_class', 'N/A')}", styles["Normal"]))
#     content.append(Paragraph(sa.get("interpretation", ""), styles["Normal"]))
#     content.append(Spacer(1, 12))

#     # Image analysis section (NEW)
#     if image_explanation:
#         content.append(Paragraph("Image-Based Analysis", styles["Heading2"]))
#         content.append(Paragraph(image_explanation, styles["Normal"]))
#         content.append(Spacer(1, 12))

#     # Crop recommendations
#     content.append(Paragraph("Crop Recommendations", styles["Heading2"]))
#     crops = report.get("crop_recommendations", [])
#     for c in crops:
#         content.append(Paragraph(
#             f"• {c['crop']} — {c['suitability']} suitability ({c['score_pct']}%)",
#             styles["Normal"]
#         ))
#     content.append(Spacer(1, 12))

#     # Fertilizer
#     content.append(Paragraph("Fertilizer Advice", styles["Heading2"]))
#     fert = report.get("fertilizer_advice", {})
#     for rec in fert.get("recommendations", []):
#         content.append(Paragraph(f"• {rec}", styles["Normal"]))
#     content.append(Spacer(1, 12))

#     # Irrigation
#     content.append(Paragraph("Irrigation Advice", styles["Heading2"]))
#     irr = report.get("irrigation_advice", {})
#     content.append(Paragraph(f"Level: {irr.get('irrigation_level', 'N/A')}", styles["Normal"]))
#     content.append(Paragraph(f"Frequency: {irr.get('frequency', 'N/A')}", styles["Normal"]))
#     content.append(Paragraph(irr.get("advice", ""), styles["Normal"]))

#     doc.build(content)
#     return file_path


# # ─────────────────────────────────────────────────────
# # MAIN PREDICTION FUNCTION
# # ─────────────────────────────────────────────────────
# def predict_fn(N, P, K, pH, RF, TMP, HUM, OC, SD, IMG, LAT, LON):
#     # ── Tabular SHI ───────────────────────────────────
#     shi = compute_shi(N, P, K, pH, OC)

#     if shi < 0.35:
#         status, bg_color = "🔴 Poor",     "#ffe6e6"
#     elif shi < 0.5:
#         status, bg_color = "🟡 Moderate", "#fff5cc"
#     else:
#         status, bg_color = "🟢 Healthy",  "#e6ffe6"

#     profile = SoilProfile(
#         N=N, P=P, K=K, pH=pH,
#         rainfall=RF, temperature=TMP, humidity=HUM,
#         organic_carbon=OC, sand=SD,
#         shi=shi, soil_class=status,
#     )
#     report = generate_full_report(profile)

#     # ── Image Analysis (NEW) ──────────────────────────
#     img_html, img_explanation = analyze_image(IMG)

#     # ── UI Components ─────────────────────────────────
#     shi_card = card(
#         "🌱 Soil Health",
#         f"<h2>{shi:.3f}</h2><b>{status}</b>",
#         bg_color,
#     )

#     crops = report.get("crop_recommendations", [])
#     crop_html = "".join(
#         [f"<p>🌾 <b>{c['crop']}</b> — {c['suitability']} suitability ({c['score_pct']}%)"
#          f"<br><small>Limiting: {', '.join(c['issues']) if c['issues'] else 'All conditions met'}</small></p>"
#          for c in crops]
#     )
#     crop_card = card("🌾 Crop Recommendations", crop_html, "#eef")

#     fert  = report.get("fertilizer_advice", {})
#     fert_html = "".join([f"<p>🧪 {r}</p>" for r in fert.get("recommendations", [])])
#     fert_card = card("🧪 Fertilizer Advice", fert_html, "#f9f9f9")

#     irr   = report.get("irrigation_advice", {})
#     irr_card = card(
#         "💧 Irrigation Advice",
#         f"<p><b>Level:</b> {irr.get('irrigation_level')}</p>"
#         f"<p><b>Frequency:</b> {irr.get('frequency')}</p>"
#         f"<p>{irr.get('advice')}</p>",
#         "#eef9ff",
#     )

#     gauge = create_gauge(shi)
#     ndvi  = ndvi_plot(get_ndvi(LAT))
#     map_h = create_map(LAT, LON)
#     pdf   = generate_pdf(report, img_explanation)

#     return (
#         shi_card,
#         gauge,
#         ndvi,
#         map_h,
#         crop_card,
#         fert_card,
#         irr_card,
#         img_html,          # ── NEW ── rich image analysis card
#         img_explanation,   # ── NEW ── text explanation
#         pdf,
#     )


# # ─────────────────────────────────────────────────────
# # GRADIO UI
# # ─────────────────────────────────────────────────────
# with gr.Blocks(title="🌱 Soil Health AI", theme=gr.themes.Soft()) as demo:

#     gr.Markdown("""
#     # 🌱 Multimodal Soil Health AI System
#     Enter soil parameters and optionally upload an image for comprehensive analysis.
#     """)

#     with gr.Row():
#         # ── Left: Soil parameters ────────────────────
#         with gr.Column(scale=1):
#             gr.Markdown("### 🧪 Soil Parameters")
#             N   = gr.Slider(0,   140, 50,  label="Nitrogen (kg/ha)")
#             P   = gr.Slider(5,   145, 50,  label="Phosphorus (kg/ha)")
#             K   = gr.Slider(5,   200, 50,  label="Potassium (kg/ha)")
#             pH  = gr.Slider(3,   10,  6.5, label="pH")
#             OC  = gr.Slider(0.5, 20,  5,   label="Organic Carbon (%)")
#             SD  = gr.Slider(4,   96,  50,  label="Sand (%)")

#         # ── Right: Environmental + image ─────────────
#         with gr.Column(scale=1):
#             gr.Markdown("### 🌦️ Environment & Location")
#             RF  = gr.Slider(0,   300, 100, label="Rainfall (mm)")
#             TMP = gr.Slider(0,   50,  25,  label="Temperature (°C)")
#             HUM = gr.Slider(10,  100, 60,  label="Humidity (%)")
#             LAT = gr.Slider(-90, 90,  20,  label="Latitude")
#             LON = gr.Slider(-180,180, 78,  label="Longitude")

#             gr.Markdown("### 📸 Soil / Crop Image")
#             IMG = gr.Image(
#                 label="Upload soil or crop image (optional)",
#                 type="numpy",
#             )

#     btn = gr.Button("🚀 Analyze Soil Health", variant="primary", size="lg")

#     gr.Markdown("---")
#     gr.Markdown("## 📊 Results")

#     with gr.Row():
#         shi_out  = gr.HTML(label="Soil Health")
#         gauge_out = gr.Plot(label="SHI Gauge")

#     with gr.Row():
#         ndvi_out = gr.Plot(label="NDVI Trend")
#         map_out  = gr.HTML(label="Location Map")

#     with gr.Row():
#         crop_out = gr.HTML(label="Crop Recommendations")
#         fert_out = gr.HTML(label="Fertilizer Advice")
#         irr_out  = gr.HTML(label="Irrigation Advice")

#     # ── NEW ── Image analysis outputs
#     gr.Markdown("### 🖼️ Image-Based Analysis")
#     img_html_out  = gr.HTML(label="Image Analysis Results")
#     img_text_out  = gr.Markdown(label="Explanation")

#     pdf_out = gr.File(label="📄 Download Full PDF Report")

#     btn.click(
#         fn=predict_fn,
#         inputs=[N, P, K, pH, RF, TMP, HUM, OC, SD, IMG, LAT, LON],
#         outputs=[
#             shi_out, gauge_out, ndvi_out, map_out,
#             crop_out, fert_out, irr_out,
#             img_html_out, img_text_out,  # ── NEW ──
#             pdf_out,
#         ],
#     )

#     gr.Markdown("""
#     ---
#     **Data Sources**: Soil Types Dataset + PlantVillage (Kaggle) | 
#     **Model**: ResNet18 (ImageNet pretrained, fine-tuned) | 
#     **Multimodal**: Tabular + Image + NDVI Time-series
#     """)


# demo.launch(share=True)
"""
gradio_app.py  ← your main app file (already exists in your project)

FIXES APPLIED:
  1. Model path now correctly points to same folder as this file
  2. image_inference import updated to v2 (3 heads)
  3. Removed app_updated.py confusion — this IS your app
  4. Safe fallback if model not found (demo mode with clear message)
"""

# import os
# import gradio as gr
# import numpy as np
# import plotly.graph_objects as go
# import plotly.express as px
# import folium
# from PIL import Image

# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
# from reportlab.lib.styles import getSampleStyleSheet

# from decision_support import SoilProfile, generate_full_report

# # ── Load image analyzer ───────────────────────────────
# # THIS IS THE FIX: use the folder where THIS file lives
# BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
# MODEL_PATH  = os.path.join(BASE_DIR, "soil_image_model.pt")
# LABEL_PATH  = os.path.join(BASE_DIR, "soil_image_labels.json")

# _analyzer = None

# def get_analyzer():
#     global _analyzer
#     if _analyzer is not None:
#         return _analyzer
#     if os.path.exists(MODEL_PATH):
#         try:
#             # try v2 first, fall back to v1
#             try:
#                 from image_inference_v2 import SoilImageAnalyzer
#             except ImportError:
#                 from image_inference import SoilImageAnalyzer
#             _analyzer = SoilImageAnalyzer(
#                 model_path=MODEL_PATH,
#                 label_path=LABEL_PATH if os.path.exists(LABEL_PATH) else None,
#                 device="cpu",
#             )
#             print("✅ Image model loaded successfully")
#         except Exception as e:
#             print(f"⚠️  Could not load model: {e}")
#     else:
#         print(f"⚠️  Model not found at: {MODEL_PATH}")
#         print("    → Running in demo mode")
#         print("    → Place soil_image_model.pt in:", BASE_DIR)
#     return _analyzer


# # ── SHI ──────────────────────────────────────────────
# def compute_shi(N, P, K, pH, OC):
#     n  = min(N / 140, 1)
#     p  = min(P / 145, 1)
#     k  = min(K / 200, 1)
#     ph = 1 - abs(pH - 6.5) / 3.5
#     oc = min(OC / 20, 1)
#     return float(np.clip(0.3 * ph + 0.2 * n + 0.15 * p + 0.15 * k + 0.2 * oc, 0, 1))


# def create_gauge(shi):
#     fig = go.Figure(go.Indicator(
#         mode="gauge+number",
#         value=shi,
#         title={"text": "Soil Health Index"},
#         gauge={
#             "axis": {"range": [0, 1]},
#             "steps": [
#                 {"range": [0, 0.35], "color": "red"},
#                 {"range": [0.35, 0.5], "color": "yellow"},
#                 {"range": [0.5, 1],   "color": "green"},
#             ],
#         }
#     ))
#     return fig


# def get_ndvi(lat):
#     base = 0.4 + (lat % 10) / 50
#     return [round(base + i * 0.04, 3) for i in range(8)]


# def ndvi_plot(ndvi):
#     return px.line(x=list(range(1, 9)), y=ndvi,
#                    title="NDVI Trend", labels={"x": "Time Step", "y": "NDVI"})


# def create_map(lat, lon):
#     m = folium.Map(location=[lat, lon], zoom_start=6)
#     folium.Marker([lat, lon], tooltip="Soil Location").add_to(m)
#     return m._repr_html_()


# def card(title, content, color):
#     return f"""
# <div style="padding:15px;border-radius:10px;background:{color};
#             margin:10px 0;border:1px solid #ddd;">
#   <h3 style="margin-top:0">{title}</h3>{content}
# </div>"""


# # ── Image analysis ────────────────────────────────────
# def analyze_image(img):
#     analyzer = get_analyzer()

#     if img is None:
#         return (
#             """<div style="padding:15px;border-radius:10px;background:#f5f5f5;border:1px solid #ddd">
#   <h3>📸 Image Analysis</h3>
#   <p>Upload a soil or crop image to get AI-powered analysis.</p>
# </div>""",
#             "No image uploaded."
#         )

#     if analyzer is None:
#         h, w = (img.shape[0], img.shape[1]) if hasattr(img, "shape") else ("?", "?")
#         return (
#             f"""<div style="padding:15px;border-radius:10px;background:#fff3cd;border:1px solid #ffc107">
#   <h3>⚠️ Demo Mode — Model not loaded</h3>
#   <p>Place <b>soil_image_model.pt</b> in your project folder:</p>
#   <code>{BASE_DIR}</code>
#   <p>Image received: {w}×{h}px ✅</p>
# </div>""",
#             f"⚠️ Model not loaded. Put soil_image_model.pt in: {BASE_DIR}"
#         )

#     result = analyzer.analyze(img)
#     return result["html"], result["explanation"]


# # ── PDF ───────────────────────────────────────────────
# def generate_pdf(report, img_explanation=""):
#     path = os.path.join(BASE_DIR, "soil_health_report.pdf")
#     doc  = SimpleDocTemplate(path)
#     styles = getSampleStyleSheet()
#     body = []
#     body.append(Paragraph("Soil Health Report", styles["Title"]))
#     body.append(Spacer(1, 12))

#     sa = report.get("soil_assessment", {})
#     body.append(Paragraph("Soil Health Assessment", styles["Heading2"]))
#     body.append(Paragraph(f"SHI: {sa.get('soil_health_index','N/A')}", styles["Normal"]))
#     body.append(Paragraph(f"Class: {sa.get('soil_class','N/A')}", styles["Normal"]))
#     body.append(Paragraph(sa.get("interpretation", ""), styles["Normal"]))
#     body.append(Spacer(1, 12))

#     if img_explanation:
#         body.append(Paragraph("Image-Based Analysis", styles["Heading2"]))
#         body.append(Paragraph(img_explanation, styles["Normal"]))
#         body.append(Spacer(1, 12))

#     body.append(Paragraph("Crop Recommendations", styles["Heading2"]))
#     for c in report.get("crop_recommendations", []):
#         body.append(Paragraph(
#             f"• {c['crop']} — {c['suitability']} ({c['score_pct']}%)",
#             styles["Normal"]
#         ))
#     body.append(Spacer(1, 12))

#     body.append(Paragraph("Fertilizer Advice", styles["Heading2"]))
#     for r in report.get("fertilizer_advice", {}).get("recommendations", []):
#         body.append(Paragraph(f"• {r}", styles["Normal"]))
#     body.append(Spacer(1, 12))

#     body.append(Paragraph("Irrigation Advice", styles["Heading2"]))
#     irr = report.get("irrigation_advice", {})
#     body.append(Paragraph(f"Level: {irr.get('irrigation_level','')}", styles["Normal"]))
#     body.append(Paragraph(irr.get("advice", ""), styles["Normal"]))

#     doc.build(body)
#     return path


# # ── MAIN PREDICT ──────────────────────────────────────
# def predict_fn(N, P, K, pH, RF, TMP, HUM, OC, SD, IMG, LAT, LON):
#     shi = compute_shi(N, P, K, pH, OC)

#     if shi < 0.35:
#         status, bg = "🔴 Poor",     "#ffe6e6"
#     elif shi < 0.5:
#         status, bg = "🟡 Moderate", "#fff5cc"
#     else:
#         status, bg = "🟢 Healthy",  "#e6ffe6"

#     profile = SoilProfile(N=N, P=P, K=K, pH=pH,
#                           rainfall=RF, temperature=TMP, humidity=HUM,
#                           organic_carbon=OC, sand=SD,
#                           shi=shi, soil_class=status)
#     report = generate_full_report(profile)

#     img_html, img_text = analyze_image(IMG)

#     shi_card = card("🌱 Soil Health", f"<h2>{shi:.3f}</h2><b>{status}</b>", bg)

#     crops = report.get("crop_recommendations", [])
#     crop_html = "".join(
#         f"<p>🌾 <b>{c['crop']}</b> — {c['suitability']} ({c['score_pct']}%)<br>"
#         f"<small>{', '.join(c['issues']) or 'All conditions met'}</small></p>"
#         for c in crops
#     )
#     crop_card = card("🌾 Crop Recommendations", crop_html, "#eef")

#     fert = report.get("fertilizer_advice", {})
#     fert_card = card("🧪 Fertilizer",
#                      "".join(f"<p>{r}</p>" for r in fert.get("recommendations", [])),
#                      "#f9f9f9")

#     irr = report.get("irrigation_advice", {})
#     irr_card = card("💧 Irrigation",
#                     f"<p><b>{irr.get('irrigation_level')}</b> — {irr.get('frequency')}</p>"
#                     f"<p>{irr.get('advice')}</p>", "#eef9ff")

#     pdf = generate_pdf(report, img_text)

#     return (shi_card, create_gauge(shi), ndvi_plot(get_ndvi(LAT)),
#             create_map(LAT, LON), crop_card, fert_card, irr_card,
#             img_html, img_text, pdf)


# # ── UI ────────────────────────────────────────────────
# with gr.Blocks(title="🌱 Soil Health AI") as demo:
#     gr.Markdown("# 🌱 Multimodal Soil Health AI System")

#     with gr.Row():
#         with gr.Column():
#             gr.Markdown("### 🧪 Soil Parameters")
#             N   = gr.Slider(0,   140, 50,  label="Nitrogen (kg/ha)")
#             P   = gr.Slider(5,   145, 50,  label="Phosphorus (kg/ha)")
#             K   = gr.Slider(5,   200, 50,  label="Potassium (kg/ha)")
#             pH  = gr.Slider(3,   10,  6.5, label="pH")
#             OC  = gr.Slider(0.5, 20,  5,   label="Organic Carbon (%)")
#             SD  = gr.Slider(4,   96,  50,  label="Sand (%)")

#         with gr.Column():
#             gr.Markdown("### 🌦️ Environment")
#             RF  = gr.Slider(0,    300, 100, label="Rainfall (mm)")
#             TMP = gr.Slider(0,    50,  25,  label="Temperature (°C)")
#             HUM = gr.Slider(10,   100, 60,  label="Humidity (%)")
#             LAT = gr.Slider(-90,  90,  20,  label="Latitude")
#             LON = gr.Slider(-180, 180, 78,  label="Longitude")
#             gr.Markdown("### 📸 Soil / Crop Image")
#             IMG = gr.Image(label="Upload image (optional)", type="numpy")

#     gr.Button("🚀 Analyze", variant="primary").click(
#         fn=predict_fn,
#         inputs=[N, P, K, pH, RF, TMP, HUM, OC, SD, IMG, LAT, LON],
#         outputs=[
#             gr.HTML(), gr.Plot(), gr.Plot(), gr.HTML(),
#             gr.HTML(), gr.HTML(), gr.HTML(),
#             gr.HTML(), gr.Markdown(), gr.File(),
#         ],
#     )

# demo.launch(share=True)
# import os
# import gradio as gr
# import numpy as np
# import plotly.graph_objects as go
# import plotly.express as px
# import folium
# from PIL import Image

# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
# from reportlab.lib.styles import getSampleStyleSheet

# from decision_support import SoilProfile, generate_full_report

# # ── Load image analyzer ───────────────────────────────
# BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
# MODEL_PATH  = os.path.join(BASE_DIR, "soil_image_model.pt")
# LABEL_PATH  = os.path.join(BASE_DIR, "soil_image_labels.json")

# _analyzer = None

# def get_analyzer():
#     global _analyzer
#     if _analyzer is not None:
#         return _analyzer
#     if os.path.exists(MODEL_PATH):
#         try:
#             try:
#                 from image_inference_v2 import SoilImageAnalyzer
#             except ImportError:
#                 from image_inference import SoilImageAnalyzer
#             _analyzer = SoilImageAnalyzer(
#                 model_path=MODEL_PATH,
#                 label_path=LABEL_PATH if os.path.exists(LABEL_PATH) else None,
#                 device="cpu",
#             )
#             print("✅ Image model loaded successfully")
#         except Exception as e:
#             print(f"⚠️  Could not load model: {e}")
#     else:
#         print(f"⚠️  Model not found at: {MODEL_PATH}")
#         print("    → Running in demo mode")
#         print("    → Place soil_image_model.pt in:", BASE_DIR)
#     return _analyzer


# # ── SHI ──────────────────────────────────────────────
# def compute_shi(N, P, K, pH, OC):
#     n  = min(N / 140, 1)
#     p  = min(P / 145, 1)
#     k  = min(K / 200, 1)
#     ph = 1 - abs(pH - 6.5) / 3.5
#     oc = min(OC / 20, 1)
#     return float(np.clip(0.3 * ph + 0.2 * n + 0.15 * p + 0.15 * k + 0.2 * oc, 0, 1))


# def create_gauge(shi):
#     fig = go.Figure(go.Indicator(
#         mode="gauge+number",
#         value=shi,
#         title={"text": "Soil Health Index", "font": {"size": 18, "color": "#2d5a27", "family": "DM Sans"}},
#         number={"font": {"size": 42, "color": "#1a3a17", "family": "DM Sans"}, "suffix": ""},
#         gauge={
#             "axis": {"range": [0, 1], "tickcolor": "#6b8f71", "tickfont": {"color": "#6b8f71"}},
#             "bar": {"color": "#4caf50"},
#             "bgcolor": "white",
#             "bordercolor": "#e0e8e1",
#             "steps": [
#                 {"range": [0, 0.35], "color": "#ffcdd2"},
#                 {"range": [0.35, 0.5], "color": "#fff9c4"},
#                 {"range": [0.5, 1],   "color": "#c8e6c9"},
#             ],
#             "threshold": {
#                 "line": {"color": "#2d5a27", "width": 3},
#                 "thickness": 0.75,
#                 "value": shi,
#             },
#         }
#     ))
#     fig.update_layout(
#         paper_bgcolor="rgba(0,0,0,0)",
#         plot_bgcolor="rgba(0,0,0,0)",
#         margin=dict(t=40, b=10, l=20, r=20),
#         height=260,
#         font={"family": "DM Sans"},
#     )
#     return fig


# def get_ndvi(lat):
#     base = 0.4 + (lat % 10) / 50
#     return [round(base + i * 0.04, 3) for i in range(8)]


# def ndvi_plot(ndvi):
#     fig = px.line(
#         x=list(range(1, 9)), y=ndvi,
#         title="NDVI Trend Over Time",
#         labels={"x": "Time Step", "y": "NDVI"},
#     )
#     fig.update_traces(
#         line=dict(color="#4caf50", width=3),
#         mode="lines+markers",
#         marker=dict(size=8, color="#2d5a27", symbol="circle"),
#     )
#     fig.update_layout(
#         paper_bgcolor="rgba(0,0,0,0)",
#         plot_bgcolor="rgba(248,252,248,0.8)",
#         font={"family": "DM Sans", "color": "#2d5a27"},
#         title_font={"size": 16, "color": "#1a3a17", "family": "DM Sans"},
#         xaxis=dict(gridcolor="#e0e8e1", linecolor="#c8dbc9"),
#         yaxis=dict(gridcolor="#e0e8e1", linecolor="#c8dbc9"),
#         margin=dict(t=50, b=30, l=40, r=20),
#         height=260,
#     )
#     return fig


# def create_map(lat, lon):
#     m = folium.Map(location=[lat, lon], zoom_start=6,
#                    tiles="CartoDB positron")
#     folium.Marker(
#         [lat, lon],
#         tooltip="📍 Soil Sample Location",
#         icon=folium.Icon(color="green", icon="leaf", prefix="fa"),
#     ).add_to(m)
#     folium.Circle(
#         radius=50000, location=[lat, lon],
#         color="#4caf50", fill=True, fill_opacity=0.1,
#     ).add_to(m)
#     return m._repr_html_()


# def card(title, content, color, icon=""):
#     return f"""
# <div style="
#   padding: 20px 24px;
#   border-radius: 16px;
#   background: {color};
#   margin: 10px 0;
#   border: 1px solid rgba(76,175,80,0.15);
#   box-shadow: 0 4px 20px rgba(45,90,39,0.08);
#   backdrop-filter: blur(8px);
#   font-family: 'DM Sans', sans-serif;
#   transition: transform 0.2s;
# ">
#   <h3 style="margin-top:0; color:#1a3a17; font-size:1.05rem; letter-spacing:0.02em; font-weight:600;">
#     {icon} {title}
#   </h3>
#   {content}
# </div>"""


# # ── Image analysis ────────────────────────────────────
# def analyze_image(img):
#     analyzer = get_analyzer()

#     if img is None:
#         return (
#             """<div style="padding:20px;border-radius:16px;background:rgba(248,252,248,0.9);
#                 border:1px dashed #a5d6a7;font-family:'DM Sans',sans-serif;text-align:center;">
#   <div style="font-size:2.5rem;margin-bottom:8px;">📸</div>
#   <h3 style="color:#2d5a27;margin:0 0 6px">Image Analysis</h3>
#   <p style="color:#6b8f71;margin:0">Upload a soil or crop image to get AI-powered visual analysis.</p>
# </div>""",
#             "No image uploaded."
#         )

#     if analyzer is None:
#         h, w = (img.shape[0], img.shape[1]) if hasattr(img, "shape") else ("?", "?")
#         return (
#             f"""<div style="padding:20px;border-radius:16px;background:#fff8e1;
#                 border:1px solid #ffcc02;font-family:'DM Sans',sans-serif;">
#   <h3 style="color:#e65100;margin-top:0;">⚠️ Demo Mode — Model not loaded</h3>
#   <p style="color:#555;">Place <b>soil_image_model.pt</b> in your project folder:</p>
#   <code style="background:#f5f5f5;padding:4px 8px;border-radius:6px;font-size:0.85rem;">{BASE_DIR}</code>
#   <p style="color:#4caf50;margin-bottom:0;">✅ Image received: {w}×{h}px</p>
# </div>""",
#             f"⚠️ Model not loaded. Put soil_image_model.pt in: {BASE_DIR}"
#         )

#     result = analyzer.analyze(img)
#     return result["html"], result["explanation"]


# # ── PDF ───────────────────────────────────────────────
# def generate_pdf(report, img_explanation=""):
#     path = os.path.join(BASE_DIR, "soil_health_report.pdf")
#     doc  = SimpleDocTemplate(path)
#     styles = getSampleStyleSheet()
#     body = []
#     body.append(Paragraph("Soil Health Report", styles["Title"]))
#     body.append(Spacer(1, 12))

#     sa = report.get("soil_assessment", {})
#     body.append(Paragraph("Soil Health Assessment", styles["Heading2"]))
#     body.append(Paragraph(f"SHI: {sa.get('soil_health_index','N/A')}", styles["Normal"]))
#     body.append(Paragraph(f"Class: {sa.get('soil_class','N/A')}", styles["Normal"]))
#     body.append(Paragraph(sa.get("interpretation", ""), styles["Normal"]))
#     body.append(Spacer(1, 12))

#     if img_explanation:
#         body.append(Paragraph("Image-Based Analysis", styles["Heading2"]))
#         body.append(Paragraph(img_explanation, styles["Normal"]))
#         body.append(Spacer(1, 12))

#     body.append(Paragraph("Crop Recommendations", styles["Heading2"]))
#     for c in report.get("crop_recommendations", []):
#         body.append(Paragraph(
#             f"• {c['crop']} — {c['suitability']} ({c['score_pct']}%)",
#             styles["Normal"]
#         ))
#     body.append(Spacer(1, 12))

#     body.append(Paragraph("Fertilizer Advice", styles["Heading2"]))
#     for r in report.get("fertilizer_advice", {}).get("recommendations", []):
#         body.append(Paragraph(f"• {r}", styles["Normal"]))
#     body.append(Spacer(1, 12))

#     body.append(Paragraph("Irrigation Advice", styles["Heading2"]))
#     irr = report.get("irrigation_advice", {})
#     body.append(Paragraph(f"Level: {irr.get('irrigation_level','')}", styles["Normal"]))
#     body.append(Paragraph(irr.get("advice", ""), styles["Normal"]))

#     doc.build(body)
#     return path


# # ── MAIN PREDICT ──────────────────────────────────────
# def predict_fn(N, P, K, pH, RF, TMP, HUM, OC, SD, IMG, LAT, LON):
#     shi = compute_shi(N, P, K, pH, OC)

#     if shi < 0.35:
#         status, bg, badge_color = "Poor",     "linear-gradient(135deg,#fff5f5,#ffe0e0)", "#e53935"
#         icon = "🔴"
#     elif shi < 0.5:
#         status, bg, badge_color = "Moderate", "linear-gradient(135deg,#fffde7,#fff9c4)", "#f9a825"
#         icon = "🟡"
#     else:
#         status, bg, badge_color = "Healthy",  "linear-gradient(135deg,#f1f8f1,#e0f2e0)", "#2e7d32"
#         icon = "🟢"

#     profile = SoilProfile(N=N, P=P, K=K, pH=pH,
#                           rainfall=RF, temperature=TMP, humidity=HUM,
#                           organic_carbon=OC, sand=SD,
#                           shi=shi, soil_class=status)
#     report = generate_full_report(profile)

#     img_html, img_text = analyze_image(IMG)

#     shi_card = f"""
# <div style="
#   padding: 28px 32px;
#   border-radius: 20px;
#   background: {bg};
#   margin: 10px 0;
#   border: 1.5px solid {badge_color}30;
#   box-shadow: 0 8px 32px {badge_color}20;
#   font-family: 'DM Sans', sans-serif;
#   text-align: center;
# ">
#   <div style="font-size:3rem;margin-bottom:6px;">{icon}</div>
#   <div style="font-size:3.5rem;font-weight:800;color:{badge_color};line-height:1;letter-spacing:-2px;">
#     {shi:.3f}
#   </div>
#   <div style="font-size:1rem;color:#555;margin-top:6px;letter-spacing:0.06em;text-transform:uppercase;font-weight:600;">
#     Soil Health Index
#   </div>
#   <div style="
#     display:inline-block;
#     margin-top:14px;
#     padding:6px 20px;
#     border-radius:50px;
#     background:{badge_color};
#     color:white;
#     font-weight:700;
#     font-size:1rem;
#     letter-spacing:0.04em;
#   ">{status}</div>
# </div>"""

#     crops = report.get("crop_recommendations", [])
#     crop_rows = ""
#     for c in crops:
#         pct = c['score_pct']
#         bar_color = "#4caf50" if pct >= 70 else ("#ffa726" if pct >= 50 else "#ef5350")
#         issues = ', '.join(c['issues']) if c['issues'] else "All conditions met ✓"
#         crop_rows += f"""
# <div style="margin-bottom:14px;">
#   <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">
#     <span style="font-weight:600;color:#1a3a17;font-size:0.95rem;">🌾 {c['crop']}</span>
#     <span style="font-size:0.85rem;color:{bar_color};font-weight:700;">{c['suitability']} ({pct}%)</span>
#   </div>
#   <div style="background:#e8f5e9;border-radius:50px;height:8px;overflow:hidden;">
#     <div style="width:{pct}%;height:100%;background:{bar_color};border-radius:50px;transition:width 0.6s;"></div>
#   </div>
#   <div style="font-size:0.78rem;color:#888;margin-top:3px;">{issues}</div>
# </div>"""
#     crop_card = card("Crop Recommendations", crop_rows, "linear-gradient(135deg,#f3f8f3,#eaf4ea)", "🌾")

#     fert = report.get("fertilizer_advice", {})
#     fert_items = "".join(
#         f'<div style="display:flex;align-items:flex-start;gap:10px;margin-bottom:10px;">'
#         f'<span style="color:#4caf50;font-size:1.1rem;margin-top:1px;">◆</span>'
#         f'<span style="color:#333;font-size:0.9rem;line-height:1.5;">{r}</span>'
#         f'</div>'
#         for r in fert.get("recommendations", [])
#     )
#     fert_card = card("Fertilizer Recommendations", fert_items,
#                      "linear-gradient(135deg,#f9fbe7,#f1f8e9)", "🧪")

#     irr = report.get("irrigation_advice", {})
#     irr_content = f"""
# <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">
#   <div style="
#     background:linear-gradient(135deg,#29b6f6,#0288d1);
#     color:white;padding:8px 18px;border-radius:50px;
#     font-weight:700;font-size:0.9rem;letter-spacing:0.03em;
#   ">{irr.get('irrigation_level','')}</div>
#   <div style="color:#555;font-size:0.9rem;">• {irr.get('frequency','')}</div>
# </div>
# <p style="color:#444;font-size:0.9rem;line-height:1.6;margin:0;">{irr.get('advice','')}</p>"""
#     irr_card = card("Irrigation Advisory", irr_content,
#                     "linear-gradient(135deg,#e1f5fe,#e3f2fd)", "💧")

#     pdf = generate_pdf(report, img_text)

#     return (shi_card, create_gauge(shi), ndvi_plot(get_ndvi(LAT)),
#             create_map(LAT, LON), crop_card, fert_card, irr_card,
#             img_html, img_text, pdf)


# # ── CUSTOM CSS ────────────────────────────────────────
# CUSTOM_CSS = """
# @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;0,9..40,800;1,9..40,400&family=Syne:wght@700;800&display=swap');

# :root {
#   --green-deep:    #1a3a17;
#   --green-mid:     #2d5a27;
#   --green-accent:  #4caf50;
#   --green-light:   #a5d6a7;
#   --green-pale:    #e8f5e9;
#   --bg-primary:    #f0f7f0;
#   --bg-card:       rgba(255,255,255,0.82);
#   --border:        rgba(76,175,80,0.18);
#   --shadow-sm:     0 2px 12px rgba(45,90,39,0.07);
#   --shadow-md:     0 6px 28px rgba(45,90,39,0.12);
#   --shadow-lg:     0 16px 56px rgba(45,90,39,0.16);
#   --radius-sm:     10px;
#   --radius-md:     16px;
#   --radius-lg:     24px;
# }

# /* ── Global reset ── */
# *, *::before, *::after { box-sizing: border-box; }

# body, .gradio-container {
#   font-family: 'DM Sans', sans-serif !important;
#   background: linear-gradient(145deg, #e8f5e9 0%, #f0f7f0 40%, #e3f2fd 100%) !important;
#   min-height: 100vh;
# }

# /* ── Noise texture overlay ── */
# .gradio-container::before {
#   content: "";
#   position: fixed;
#   inset: 0;
#   background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.025'/%3E%3C/svg%3E");
#   pointer-events: none;
#   z-index: 0;
#   opacity: 0.4;
# }

# /* ── App wrapper ── */
# #app-wrapper {
#   max-width: 1200px;
#   margin: 0 auto;
#   padding: 0 16px 40px;
#   position: relative;
#   z-index: 1;
# }

# /* ── Hero header ── */
# #hero-header {
#   text-align: center;
#   padding: 52px 24px 36px;
#   position: relative;
# }

# #hero-header::after {
#   content: "";
#   display: block;
#   width: 80px;
#   height: 4px;
#   background: linear-gradient(90deg, #4caf50, #81c784);
#   border-radius: 2px;
#   margin: 18px auto 0;
# }

# .hero-title {
#   font-family: 'Syne', sans-serif !important;
#   font-size: clamp(2rem, 5vw, 3rem) !important;
#   font-weight: 800 !important;
#   color: var(--green-deep) !important;
#   letter-spacing: -1px !important;
#   margin: 0 0 8px !important;
#   line-height: 1.1 !important;
# }

# .hero-subtitle {
#   font-size: 1.05rem !important;
#   color: #6b8f71 !important;
#   font-weight: 400 !important;
#   margin: 0 !important;
# }

# /* ── Section labels ── */
# .section-label {
#   font-family: 'Syne', sans-serif !important;
#   font-size: 0.72rem !important;
#   font-weight: 700 !important;
#   letter-spacing: 0.12em !important;
#   text-transform: uppercase !important;
#   color: var(--green-accent) !important;
#   margin: 0 0 14px !important;
#   display: flex;
#   align-items: center;
#   gap: 8px;
# }

# .section-label::before {
#   content: "";
#   display: inline-block;
#   width: 18px;
#   height: 2px;
#   background: var(--green-accent);
#   border-radius: 1px;
# }

# /* ── Input panels ── */
# .input-panel {
#   background: var(--bg-card) !important;
#   border: 1px solid var(--border) !important;
#   border-radius: var(--radius-lg) !important;
#   padding: 24px !important;
#   box-shadow: var(--shadow-md) !important;
#   backdrop-filter: blur(12px) !important;
#   transition: box-shadow 0.3s ease !important;
# }

# .input-panel:hover {
#   box-shadow: var(--shadow-lg) !important;
# }

# /* ── Sliders ── */
# .gradio-slider input[type=range] {
#   accent-color: var(--green-accent) !important;
#   height: 5px !important;
# }

# .gradio-slider .wrap {
#   background: transparent !important;
# }

# label span {
#   font-size: 0.85rem !important;
#   font-weight: 600 !important;
#   color: #2d5a27 !important;
#   letter-spacing: 0.01em !important;
# }

# /* ── Analyze button ── */
# #analyze-btn {
#   background: linear-gradient(135deg, #2e7d32, #4caf50) !important;
#   color: white !important;
#   font-family: 'Syne', sans-serif !important;
#   font-size: 1rem !important;
#   font-weight: 700 !important;
#   letter-spacing: 0.06em !important;
#   text-transform: uppercase !important;
#   padding: 16px 48px !important;
#   border-radius: 50px !important;
#   border: none !important;
#   cursor: pointer !important;
#   box-shadow: 0 6px 24px rgba(46,125,50,0.35) !important;
#   transition: transform 0.22s cubic-bezier(0.34,1.56,0.64,1),
#               box-shadow 0.22s ease,
#               filter 0.22s ease !important;
#   min-width: 220px !important;
#   margin: 8px auto !important;
#   display: block !important;
# }

# #analyze-btn:hover {
#   transform: translateY(-3px) scale(1.04) !important;
#   box-shadow: 0 12px 36px rgba(46,125,50,0.45) !important;
#   filter: brightness(1.06) !important;
# }

# #analyze-btn:active {
#   transform: translateY(0) scale(0.98) !important;
# }

# /* ── Button row centering ── */
# .btn-row {
#   display: flex !important;
#   justify-content: center !important;
#   padding: 8px 0 24px !important;
# }

# /* ── Output cards ── */
# .output-card {
#   background: var(--bg-card) !important;
#   border: 1px solid var(--border) !important;
#   border-radius: var(--radius-md) !important;
#   padding: 22px !important;
#   box-shadow: var(--shadow-sm) !important;
#   backdrop-filter: blur(8px) !important;
#   transition: box-shadow 0.25s ease !important;
# }

# .output-card:hover {
#   box-shadow: var(--shadow-md) !important;
# }

# /* ── Plot backgrounds ── */
# .gradio-plot {
#   background: transparent !important;
#   border-radius: var(--radius-md) !important;
# }

# /* ── HTML output wrappers ── */
# .gradio-html {
#   background: transparent !important;
# }

# /* ── Image upload zone ── */
# .gradio-image {
#   border-radius: var(--radius-md) !important;
#   border: 2px dashed var(--green-light) !important;
#   background: rgba(232,245,233,0.5) !important;
#   transition: border-color 0.2s !important;
# }

# .gradio-image:hover {
#   border-color: var(--green-accent) !important;
# }

# /* ── File download ── */
# .gradio-file {
#   background: var(--bg-card) !important;
#   border: 1px solid var(--border) !important;
#   border-radius: var(--radius-sm) !important;
# }

# /* ── Markdown output ── */
# .gradio-markdown {
#   font-family: 'DM Sans', sans-serif !important;
#   font-size: 0.9rem !important;
#   color: #3d5c42 !important;
#   background: rgba(248,252,248,0.7) !important;
#   border-radius: var(--radius-sm) !important;
#   padding: 14px !important;
#   border: 1px solid var(--border) !important;
# }

# /* ── Section divider ── */
# .divider {
#   border: none;
#   border-top: 1.5px solid rgba(76,175,80,0.15);
#   margin: 8px 0 18px;
# }

# /* ── Results section header ── */
# .results-header {
#   font-family: 'Syne', sans-serif !important;
#   font-size: 1.35rem !important;
#   font-weight: 800 !important;
#   color: var(--green-deep) !important;
#   text-align: center !important;
#   margin: 28px 0 18px !important;
#   letter-spacing: -0.02em !important;
# }

# /* ── Scrollbar ── */
# ::-webkit-scrollbar { width: 6px; }
# ::-webkit-scrollbar-track { background: #f1f8f1; }
# ::-webkit-scrollbar-thumb { background: #a5d6a7; border-radius: 3px; }
# ::-webkit-scrollbar-thumb:hover { background: #4caf50; }

# /* ── Fade-in animation ── */
# @keyframes fadeUp {
#   from { opacity: 0; transform: translateY(16px); }
#   to   { opacity: 1; transform: translateY(0); }
# }

# .gradio-container > * {
#   animation: fadeUp 0.5s ease both;
# }
# """

# # ── UI ────────────────────────────────────────────────
# with gr.Blocks(title="🌱 Soil Health AI", css=CUSTOM_CSS) as demo:

#     # ── Hero ──
#     gr.HTML("""
#     <div id="hero-header">
#       <div class="hero-title">🌱 Soil Health AI</div>
#       <p class="hero-subtitle">
#         Multimodal intelligence for precision agriculture — analyze soil, predict crops, and optimize yield.
#       </p>
#     </div>
#     """)

#     # ── Inputs ──
#     with gr.Row(equal_height=True):
#         with gr.Column(scale=1):
#             gr.HTML('<div class="section-label">Soil Chemistry</div>')
#             with gr.Group(elem_classes="input-panel"):
#                 N   = gr.Slider(0,   140, 50,  label="Nitrogen (kg/ha)")
#                 P   = gr.Slider(5,   145, 50,  label="Phosphorus (kg/ha)")
#                 K   = gr.Slider(5,   200, 50,  label="Potassium (kg/ha)")
#                 pH  = gr.Slider(3,   10,  6.5, label="pH Level")
#                 OC  = gr.Slider(0.5, 20,  5,   label="Organic Carbon (%)")
#                 SD  = gr.Slider(4,   96,  50,  label="Sand Content (%)")

#         with gr.Column(scale=1):
#             gr.HTML('<div class="section-label">Environment & Location</div>')
#             with gr.Group(elem_classes="input-panel"):
#                 RF  = gr.Slider(0,    300, 100, label="Rainfall (mm)")
#                 TMP = gr.Slider(0,    50,  25,  label="Temperature (°C)")
#                 HUM = gr.Slider(10,   100, 60,  label="Humidity (%)")
#                 LAT = gr.Slider(-90,  90,  20,  label="Latitude")
#                 LON = gr.Slider(-180, 180, 78,  label="Longitude")
#             gr.HTML('<div class="section-label" style="margin-top:18px;">Soil / Crop Image</div>')
#             with gr.Group(elem_classes="input-panel"):
#                 IMG = gr.Image(label="Upload image (optional)", type="numpy",
#                                show_label=False, height=160)

#     # ── CTA ──
#     with gr.Row(elem_classes="btn-row"):
#         btn = gr.Button("🚀  Run Analysis", variant="primary", elem_id="analyze-btn")

#     # ── Results header ──
#     gr.HTML('<div class="results-header">Analysis Results</div>')
#     gr.HTML('<hr class="divider">')

#     # ── Output row 1: SHI card + gauge + NDVI ──
#     with gr.Row(equal_height=False):
#         with gr.Column(scale=1):
#             shi_html = gr.HTML(elem_classes="output-card")
#         with gr.Column(scale=1):
#             gauge_plot = gr.Plot(elem_classes="output-card")
#         with gr.Column(scale=1):
#             ndvi_plot_out = gr.Plot(elem_classes="output-card")

#     # ── Output row 2: Map ──
#     gr.HTML('<div class="section-label" style="margin-top:24px;">Geospatial View</div>')
#     map_html = gr.HTML(elem_classes="output-card")

#     # ── Output row 3: Crop / Fert / Irrigation ──
#     gr.HTML('<div class="section-label" style="margin-top:24px;">Agronomic Intelligence</div>')
#     with gr.Row(equal_height=False):
#         with gr.Column(scale=1):
#             crop_html  = gr.HTML(elem_classes="output-card")
#         with gr.Column(scale=1):
#             fert_html  = gr.HTML(elem_classes="output-card")
#         with gr.Column(scale=1):
#             irr_html   = gr.HTML(elem_classes="output-card")

#     # ── Output row 4: Image AI + PDF ──
#     gr.HTML('<div class="section-label" style="margin-top:24px;">Image Intelligence & Report</div>')
#     with gr.Row():
#         with gr.Column(scale=2):
#             img_out_html = gr.HTML(elem_classes="output-card")
#         with gr.Column(scale=1):
#             img_out_md = gr.Markdown(label="Image Explanation", elem_classes="output-card")
#             pdf_file   = gr.File(label="📥 Download Full PDF Report")

#     btn.click(
#         fn=predict_fn,
#         inputs=[N, P, K, pH, RF, TMP, HUM, OC, SD, IMG, LAT, LON],
#         outputs=[
#             shi_html, gauge_plot, ndvi_plot_out, map_html,
#             crop_html, fert_html, irr_html,
#             img_out_html, img_out_md, pdf_file,
#         ],
#     )

# demo.launch(share=True)

# import os
# import gradio as gr
# import numpy as np
# import plotly.graph_objects as go
# import plotly.express as px
# import folium
# from PIL import Image

# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
# from reportlab.lib.styles import getSampleStyleSheet

# from decision_support import SoilProfile, generate_full_report

# # ── Load image analyzer ───────────────────────────────
# BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
# MODEL_PATH  = os.path.join(BASE_DIR, "soil_image_model.pt")
# LABEL_PATH  = os.path.join(BASE_DIR, "soil_image_labels.json")

# _analyzer = None

# def get_analyzer():
#     global _analyzer
#     if _analyzer is not None:
#         return _analyzer
#     if os.path.exists(MODEL_PATH):
#         try:
#             try:
#                 from image_inference_v2 import SoilImageAnalyzer
#             except ImportError:
#                 from image_inference import SoilImageAnalyzer
#             _analyzer = SoilImageAnalyzer(
#                 model_path=MODEL_PATH,
#                 label_path=LABEL_PATH if os.path.exists(LABEL_PATH) else None,
#                 device="cpu",
#             )
#             print("✅ Image model loaded successfully")
#         except Exception as e:
#             print(f"⚠️  Could not load model: {e}")
#     else:
#         print(f"⚠️  Model not found at: {MODEL_PATH}")
#         print("    → Running in demo mode")
#         print("    → Place soil_image_model.pt in:", BASE_DIR)
#     return _analyzer


# # ── SHI ──────────────────────────────────────────────
# def compute_shi(N, P, K, pH, OC):
#     n  = min(N / 140, 1)
#     p  = min(P / 145, 1)
#     k  = min(K / 200, 1)
#     ph = 1 - abs(pH - 6.5) / 3.5
#     oc = min(OC / 20, 1)
#     return float(np.clip(0.3 * ph + 0.2 * n + 0.15 * p + 0.15 * k + 0.2 * oc, 0, 1))


# def create_gauge(shi):
#     fig = go.Figure(go.Indicator(
#         mode="gauge+number",
#         value=shi,
#         title={"text": "Soil Health Index", "font": {"size": 16, "color": "#c9b8f0", "family": "Outfit"}},
#         number={"font": {"size": 44, "color": "#f5d97e", "family": "Outfit"}, "suffix": ""},
#         gauge={
#             "axis": {"range": [0, 1], "tickcolor": "#7c5cbf", "tickfont": {"color": "#a08ad4"}},
#             "bar": {"color": "#f5d97e"},
#             "bgcolor": "rgba(0,0,0,0)",
#             "borderwidth": 0,
#             "steps": [
#                 {"range": [0, 0.35], "color": "rgba(239,83,80,0.25)"},
#                 {"range": [0.35, 0.5], "color": "rgba(255,183,77,0.25)"},
#                 {"range": [0.5, 1],   "color": "rgba(171,130,255,0.25)"},
#             ],
#             "threshold": {
#                 "line": {"color": "#f5d97e", "width": 3},
#                 "thickness": 0.78,
#                 "value": shi,
#             },
#         }
#     ))
#     fig.update_layout(
#         paper_bgcolor="rgba(0,0,0,0)",
#         plot_bgcolor="rgba(0,0,0,0)",
#         margin=dict(t=40, b=10, l=20, r=20),
#         height=260,
#         font={"family": "Outfit"},
#     )
#     return fig


# def get_ndvi(lat):
#     base = 0.4 + (lat % 10) / 50
#     return [round(base + i * 0.04, 3) for i in range(8)]


# def ndvi_plot(ndvi):
#     fig = px.line(
#         x=list(range(1, 9)), y=ndvi,
#         title="NDVI Trend Over Time",
#         labels={"x": "Time Step", "y": "NDVI"},
#     )
#     fig.update_traces(
#         line=dict(color="#f5d97e", width=3),
#         mode="lines+markers",
#         marker=dict(size=8, color="#ab82ff", symbol="circle"),
#     )
#     fig.update_layout(
#         paper_bgcolor="rgba(0,0,0,0)",
#         plot_bgcolor="rgba(30,18,60,0.5)",
#         font={"family": "Outfit", "color": "#c9b8f0"},
#         title_font={"size": 15, "color": "#f5d97e", "family": "Outfit"},
#         xaxis=dict(gridcolor="rgba(124,92,191,0.2)", linecolor="rgba(124,92,191,0.3)", color="#a08ad4"),
#         yaxis=dict(gridcolor="rgba(124,92,191,0.2)", linecolor="rgba(124,92,191,0.3)", color="#a08ad4"),
#         margin=dict(t=48, b=30, l=40, r=20),
#         height=260,
#     )
#     return fig


# def create_map(lat, lon):
#     m = folium.Map(location=[lat, lon], zoom_start=6, tiles="CartoDB dark_matter")
#     folium.Marker(
#         [lat, lon],
#         tooltip="📍 Soil Sample Location",
#         icon=folium.Icon(color="purple", icon="star", prefix="fa"),
#     ).add_to(m)
#     folium.Circle(
#         radius=50000, location=[lat, lon],
#         color="#ab82ff", fill=True, fill_color="#7c5cbf", fill_opacity=0.15,
#     ).add_to(m)
#     return m._repr_html_()


# def card(title, content, icon=""):
#     return f"""
# <div style="
#   padding: 20px 24px;
#   border-radius: 16px;
#   background: rgba(30,18,60,0.82);
#   margin: 8px 0;
#   border: 1px solid rgba(171,130,255,0.22);
#   box-shadow: 0 4px 24px rgba(0,0,0,0.4), inset 0 1px 0 rgba(245,217,126,0.08);
#   font-family: 'Outfit', sans-serif;
#   backdrop-filter: blur(14px);
# ">
#   <h3 style="margin-top:0; color:#f5d97e; font-size:0.85rem; letter-spacing:0.1em;
#              text-transform:uppercase; font-weight:700; margin-bottom:14px;
#              display:flex; align-items:center; gap:8px;">
#     <span>{icon}</span> {title}
#   </h3>
#   <div style="color:#d4c4f0;">{content}</div>
# </div>"""


# # ── Image analysis ────────────────────────────────────
# def analyze_image(img):
#     analyzer = get_analyzer()

#     if img is None:
#         return (
#             """<div style="padding:24px;border-radius:16px;
#                 background:rgba(30,18,60,0.82);border:1px dashed rgba(171,130,255,0.35);
#                 font-family:'Outfit',sans-serif;text-align:center;">
#   <div style="font-size:2.8rem;margin-bottom:10px;">📸</div>
#   <h3 style="color:#f5d97e;margin:0 0 6px;font-size:1rem;">Image Analysis</h3>
#   <p style="color:#7c5cbf;margin:0;font-size:0.88rem;">Upload a soil or crop image to get AI-powered visual analysis.</p>
# </div>""",
#             "No image uploaded."
#         )

#     if analyzer is None:
#         h, w = (img.shape[0], img.shape[1]) if hasattr(img, "shape") else ("?", "?")
#         return (
#             f"""<div style="padding:20px;border-radius:16px;background:rgba(42,24,10,0.85);
#                 border:1px solid rgba(255,183,77,0.35);font-family:'Outfit',sans-serif;">
#   <h3 style="color:#ffb74d;margin-top:0;font-size:1rem;">⚠️ Demo Mode — Model not loaded</h3>
#   <p style="color:#c9b8f0;font-size:0.88rem;">Place <b>soil_image_model.pt</b> in:</p>
#   <code style="background:rgba(0,0,0,0.35);padding:4px 10px;border-radius:6px;
#                font-size:0.8rem;color:#f5d97e;">{BASE_DIR}</code>
#   <p style="color:#ab82ff;margin-bottom:0;margin-top:10px;font-size:0.88rem;">✅ Image received: {w}×{h}px</p>
# </div>""",
#             f"⚠️ Model not loaded. Put soil_image_model.pt in: {BASE_DIR}"
#         )

#     result = analyzer.analyze(img)
#     return result["html"], result["explanation"]


# # ── PDF ───────────────────────────────────────────────
# def generate_pdf(report, img_explanation=""):
#     path = os.path.join(BASE_DIR, "soil_health_report.pdf")
#     doc  = SimpleDocTemplate(path)
#     styles = getSampleStyleSheet()
#     body = []
#     body.append(Paragraph("Soil Health Report", styles["Title"]))
#     body.append(Spacer(1, 12))

#     sa = report.get("soil_assessment", {})
#     body.append(Paragraph("Soil Health Assessment", styles["Heading2"]))
#     body.append(Paragraph(f"SHI: {sa.get('soil_health_index','N/A')}", styles["Normal"]))
#     body.append(Paragraph(f"Class: {sa.get('soil_class','N/A')}", styles["Normal"]))
#     body.append(Paragraph(sa.get("interpretation", ""), styles["Normal"]))
#     body.append(Spacer(1, 12))

#     if img_explanation:
#         body.append(Paragraph("Image-Based Analysis", styles["Heading2"]))
#         body.append(Paragraph(img_explanation, styles["Normal"]))
#         body.append(Spacer(1, 12))

#     body.append(Paragraph("Crop Recommendations", styles["Heading2"]))
#     for c in report.get("crop_recommendations", []):
#         body.append(Paragraph(
#             f"• {c['crop']} — {c['suitability']} ({c['score_pct']}%)",
#             styles["Normal"]
#         ))
#     body.append(Spacer(1, 12))

#     body.append(Paragraph("Fertilizer Advice", styles["Heading2"]))
#     for r in report.get("fertilizer_advice", {}).get("recommendations", []):
#         body.append(Paragraph(f"• {r}", styles["Normal"]))
#     body.append(Spacer(1, 12))

#     body.append(Paragraph("Irrigation Advice", styles["Heading2"]))
#     irr = report.get("irrigation_advice", {})
#     body.append(Paragraph(f"Level: {irr.get('irrigation_level','')}", styles["Normal"]))
#     body.append(Paragraph(irr.get("advice", ""), styles["Normal"]))

#     doc.build(body)
#     return path


# # ── MAIN PREDICT ──────────────────────────────────────
# def predict_fn(N, P, K, pH, RF, TMP, HUM, OC, SD, IMG, LAT, LON):
#     shi = compute_shi(N, P, K, pH, OC)

#     if shi < 0.35:
#         status, badge_color, badge_bg = "Poor",     "#ef5350", "rgba(239,83,80,0.18)"
#         icon = "🔴"
#     elif shi < 0.5:
#         status, badge_color, badge_bg = "Moderate", "#ffb74d", "rgba(255,183,77,0.18)"
#         icon = "🟡"
#     else:
#         status, badge_color, badge_bg = "Healthy",  "#ab82ff", "rgba(171,130,255,0.22)"
#         icon = "✨"

#     profile = SoilProfile(N=N, P=P, K=K, pH=pH,
#                           rainfall=RF, temperature=TMP, humidity=HUM,
#                           organic_carbon=OC, sand=SD,
#                           shi=shi, soil_class=status)
#     report = generate_full_report(profile)
#     img_html, img_text = analyze_image(IMG)

#     # ── SHI Hero Card ──
#     shi_card = f"""
# <div style="
#   padding: 32px 28px;
#   border-radius: 20px;
#   background: linear-gradient(145deg, rgba(42,24,80,0.96), rgba(18,10,46,0.99));
#   border: 1px solid rgba(245,217,126,0.22);
#   box-shadow: 0 8px 40px rgba(0,0,0,0.55),
#               0 0 0 1px rgba(171,130,255,0.1),
#               inset 0 1px 0 rgba(245,217,126,0.1);
#   font-family: 'Outfit', sans-serif;
#   text-align: center;
#   position: relative;
#   overflow: hidden;
# ">
#   <div style="
#     position:absolute;top:-50px;left:50%;transform:translateX(-50%);
#     width:200px;height:200px;
#     background:radial-gradient(circle, rgba(171,130,255,0.15) 0%, transparent 70%);
#     pointer-events:none;
#   "></div>
#   <div style="font-size:2.8rem;margin-bottom:10px;position:relative;">{icon}</div>
#   <div style="font-size:4.2rem;font-weight:800;color:#f5d97e;
#               line-height:1;letter-spacing:-3px;position:relative;">
#     {shi:.3f}
#   </div>
#   <div style="font-size:0.72rem;color:#7c5cbf;margin-top:10px;letter-spacing:0.16em;
#               text-transform:uppercase;font-weight:600;">
#     Soil Health Index
#   </div>
#   <div style="
#     display:inline-block;margin-top:16px;
#     padding:7px 26px;border-radius:50px;
#     background:{badge_bg};
#     border:1.5px solid {badge_color}88;
#     color:{badge_color};font-weight:700;font-size:0.9rem;letter-spacing:0.05em;
#   ">{status}</div>
# </div>"""

#     # ── Crop Card ──
#     crops = report.get("crop_recommendations", [])
#     crop_rows = ""
#     for c in crops:
#         pct = c['score_pct']
#         bar_color = "#ab82ff" if pct >= 70 else ("#ffb74d" if pct >= 50 else "#ef5350")
#         issues = ', '.join(c['issues']) if c['issues'] else "All conditions met ✓"
#         crop_rows += f"""
# <div style="margin-bottom:16px;">
#   <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:5px;">
#     <span style="font-weight:600;color:#e8dcff;font-size:0.9rem;">🌾 {c['crop']}</span>
#     <span style="font-size:0.78rem;color:{bar_color};font-weight:700;
#                  background:rgba(0,0,0,0.3);padding:2px 10px;border-radius:50px;
#                  border:1px solid {bar_color}44;">
#       {c['suitability']} · {pct}%
#     </span>
#   </div>
#   <div style="background:rgba(124,92,191,0.2);border-radius:50px;height:6px;overflow:hidden;">
#     <div style="width:{pct}%;height:100%;
#                 background:linear-gradient(90deg,{bar_color}88,{bar_color});
#                 border-radius:50px;"></div>
#   </div>
#   <div style="font-size:0.73rem;color:#6b4fa8;margin-top:4px;">{issues}</div>
# </div>"""
#     crop_card = card("Crop Recommendations", crop_rows, "🌾")

#     # ── Fertilizer Card ──
#     fert = report.get("fertilizer_advice", {})
#     fert_items = "".join(
#         f'<div style="display:flex;align-items:flex-start;gap:10px;margin-bottom:12px;">'
#         f'<span style="color:#f5d97e;font-size:0.9rem;margin-top:3px;flex-shrink:0;">◆</span>'
#         f'<span style="color:#d4c4f0;font-size:0.87rem;line-height:1.55;">{r}</span>'
#         f'</div>'
#         for r in fert.get("recommendations", [])
#     )
#     fert_card = card("Fertilizer Recommendations", fert_items, "🧪")

#     # ── Irrigation Card ──
#     irr = report.get("irrigation_advice", {})
#     irr_content = f"""
# <div style="display:flex;align-items:center;gap:12px;margin-bottom:14px;flex-wrap:wrap;">
#   <div style="
#     background:linear-gradient(135deg,#5c3d9e,#9b5de5);
#     color:white;padding:7px 20px;border-radius:50px;
#     font-weight:700;font-size:0.85rem;letter-spacing:0.04em;white-space:nowrap;
#     box-shadow:0 4px 14px rgba(124,92,191,0.4);
#   ">{irr.get('irrigation_level','')}</div>
#   <div style="color:#a08ad4;font-size:0.87rem;">{irr.get('frequency','')}</div>
# </div>
# <p style="color:#d4c4f0;font-size:0.87rem;line-height:1.6;margin:0;">{irr.get('advice','')}</p>"""
#     irr_card = card("Irrigation Advisory", irr_content, "💧")

#     pdf = generate_pdf(report, img_text)

#     return (shi_card, create_gauge(shi), ndvi_plot(get_ndvi(LAT)),
#             create_map(LAT, LON), crop_card, fert_card, irr_card,
#             img_html, img_text, pdf)


# # ── CUSTOM CSS ────────────────────────────────────────
# CUSTOM_CSS = """
# @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Syne:wght@700;800&display=swap');

# :root {
#   --purple-deep:    #0d0820;
#   --purple-dark:    #1a0f3c;
#   --purple-mid:     #2a1850;
#   --purple-card:    rgba(30,18,60,0.82);
#   --purple-border:  rgba(171,130,255,0.2);
#   --purple-accent:  #ab82ff;
#   --purple-soft:    #7c5cbf;
#   --gold:           #f5d97e;
#   --gold-dim:       #c9a84c;
#   --text-primary:   #f0e8ff;
#   --text-secondary: #e6dcff;   
#   --text-muted:     #cbb6ff;       
#   --shadow-glow:    0 0 50px rgba(124,92,191,0.2);
# }

# *, *::before, *::after { box-sizing: border-box; }

# body, .gradio-container {
#   font-family: 'Outfit', sans-serif !important;
#   background: radial-gradient(ellipse at 20% 10%, #2a1060 0%, #0d0820 45%, #060414 100%) !important;
#   min-height: 100vh;
#   color: var(--text-primary) !important;
# }

# /* ── Ambient glow orbs ── */
# .gradio-container::before {
#   content: "";
#   position: fixed;
#   inset: 0;
#   background:
#     radial-gradient(ellipse 600px 400px at 10% 20%, rgba(124,92,191,0.12) 0%, transparent 70%),
#     radial-gradient(ellipse 400px 300px at 90% 80%, rgba(245,217,126,0.07) 0%, transparent 70%),
#     radial-gradient(ellipse 300px 400px at 80% 15%, rgba(155,93,229,0.08) 0%, transparent 70%);
#   pointer-events: none;
#   z-index: 0;
# }

# /* ── Hero ── */
# #hero-header {
#   text-align: center;
#   padding: 56px 24px 38px;
#   position: relative;
#   z-index: 1;
# }

# .hero-eyebrow {
#   font-size: 0.7rem;
#   font-weight: 600;
#   letter-spacing: 0.2em;
#   text-transform: uppercase;
#   color: var(--gold);
#   margin-bottom: 14px;
#   display: flex;
#   align-items: center;
#   justify-content: center;
#   gap: 12px;
#   opacity: 0.85;
# }

# .hero-eyebrow::before,
# .hero-eyebrow::after {
#   content: "";
#   display: inline-block;
#   width: 36px;
#   height: 1px;
#   background: linear-gradient(90deg, transparent, var(--gold-dim));
# }
# .hero-eyebrow::after {
#   background: linear-gradient(90deg, var(--gold-dim), transparent);
# }

# .hero-title {
#   font-family: 'Syne', sans-serif !important;
#   font-size: clamp(2.2rem, 5.5vw, 3.4rem) !important;
#   font-weight: 800 !important;
#   color: var(--text-primary) !important;
#   letter-spacing: -1.5px !important;
#   margin: 0 0 12px !important;
#   line-height: 1.05 !important;
#   text-shadow: 0 0 80px rgba(171,130,255,0.35) !important;
# }

# .hero-title span {
#   background: linear-gradient(135deg, #f5d97e 30%, #e0b8ff);
#   -webkit-background-clip: text;
#   -webkit-text-fill-color: transparent;
#   background-clip: text;
# }

# .hero-subtitle {
#   font-size: 0.97rem !important;
#   color: var(--text-muted) !important;
#   font-weight: 400 !important;
#   max-width: 500px;
#   margin: 0 auto !important;
#   line-height: 1.65 !important;
# }

# /* ── Section labels ── */
# .section-label {
#   font-size: 0.67rem !important;
#   font-weight: 700 !important;
#   letter-spacing: 0.18em !important;
#   text-transform: uppercase !important;
#   color: var(--gold) !important;
#   margin: 0 0 12px !important;
#   display: flex;
#   align-items: center;
#   gap: 10px;
#   opacity: 0.85;
# }

# .section-label::before {
#   content: "";
#   display: inline-block;
#   width: 18px;
#   height: 1.5px;
#   background: var(--gold-dim);
#   border-radius: 1px;
# }

# /* ── Input panels ── */
# .input-panel {
#   background: rgba(26,15,60,0.75) !important;
#   border: 1px solid var(--purple-border) !important;
#   border-radius: 20px !important;
#   padding: 24px !important;
#   box-shadow: 0 8px 36px rgba(0,0,0,0.45),
#               inset 0 1px 0 rgba(245,217,126,0.06),
#               var(--shadow-glow) !important;
#   backdrop-filter: blur(18px) !important;
# }

# /* ── Sliders ── */
# .gradio-slider input[type=range] {
#   accent-color: var(--purple-accent) !important;
# }

# label span {
#   color: #f0e8ff !important;
#   font-weight: 600 !important;
# }


# input[type="number"] {
#   background: rgba(124,92,191,0.12) !important;
#   border: 1px solid var(--purple-border) !important;
#   border-radius: 8px !important;
#   color: var(--gold) !important;
#   font-family: 'Outfit', sans-serif !important;
#   font-size: 0.85rem !important;
# }

# /* ── Analyze button ── */
# #analyze-btn {
#   background: linear-gradient(135deg, #6b3fa0 0%, #9b5de5 50%, #f5c842 100%) !important;
#   color: #0d0820 !important;
#   font-family: 'Syne', sans-serif !important;
#   font-size: 0.9rem !important;
#   font-weight: 800 !important;
#   letter-spacing: 0.12em !important;
#   text-transform: uppercase !important;
#   padding: 16px 56px !important;
#   border-radius: 50px !important;
#   border: none !important;
#   cursor: pointer !important;
#   box-shadow: 0 6px 30px rgba(155,93,229,0.5),
#               0 0 0 1px rgba(245,217,126,0.15),
#               inset 0 1px 0 rgba(255,255,255,0.15) !important;
#   transition: transform 0.25s cubic-bezier(0.34,1.56,0.64,1),
#               box-shadow 0.25s ease !important;
#   min-width: 240px !important;
# }

# #analyze-btn:hover {
#   transform: translateY(-4px) scale(1.05) !important;
#   box-shadow: 0 16px 44px rgba(155,93,229,0.6),
#               0 0 70px rgba(245,217,126,0.12) !important;
# }

# #analyze-btn:active {
#   transform: translateY(0) scale(0.97) !important;
# }

# .btn-row {
#   display: flex !important;
#   justify-content: center !important;
#   padding: 12px 0 30px !important;
# }

# /* ── Output cards ── */
# .output-card {
#   background: rgba(26,15,60,0.75) !important;
#   border: 1px solid var(--purple-border) !important;
#   border-radius: 16px !important;
#   padding: 20px !important;
#   box-shadow: 0 4px 26px rgba(0,0,0,0.4),
#               inset 0 1px 0 rgba(245,217,126,0.05) !important;
#   backdrop-filter: blur(14px) !important;
# }

# .gradio-plot, .gradio-html {
#   background: transparent !important;
#   border-radius: 16px !important;
# }

# .gradio-image {
#   border-radius: 14px !important;
#   border: 2px dashed rgba(171,130,255,0.3) !important;
#   background: rgba(26,15,60,0.5) !important;
# }
# .gradio-image:hover {
#   border-color: rgba(245,217,126,0.45) !important;
# }

# .gradio-markdown {
#   font-family: 'Outfit', sans-serif !important;
#   font-size: 0.87rem !important;
#   color: var(--text-secondary) !important;
#   background: rgba(26,15,60,0.65) !important;
#   border-radius: 10px !important;
#   padding: 14px !important;
#   border: 1px solid var(--purple-border) !important;
#   line-height: 1.6 !important;
# }

# .gradio-file {
#   background: rgba(26,15,60,0.7) !important;
#   border: 1px solid rgba(245,217,126,0.18) !important;
#   border-radius: 10px !important;
# }

# .divider {
#   border: none;
#   border-top: 1px solid rgba(124,92,191,0.18);
#   margin: 6px 0 22px;
# }

# .results-header {
#   font-family: 'Syne', sans-serif !important;
#   font-size: 1.25rem !important;
#   font-weight: 800 !important;
#   color: var(--text-primary) !important;
#   text-align: center !important;
#   margin: 28px 0 12px !important;
#   letter-spacing: -0.02em !important;
# }

# ::-webkit-scrollbar { width: 5px; }
# ::-webkit-scrollbar-track { background: #0d0820; }
# ::-webkit-scrollbar-thumb { background: #3d2770; border-radius: 3px; }
# ::-webkit-scrollbar-thumb:hover { background: #ab82ff; }

# @keyframes fadeUp {
#   from { opacity: 0; transform: translateY(18px); }
#   to   { opacity: 1; transform: translateY(0); }
# }
# .gradio-container > * { animation: fadeUp 0.5s ease both; }
# """

# # ── UI ────────────────────────────────────────────────
# with gr.Blocks(title="🌱 Soil Health AI", css=CUSTOM_CSS) as demo:

#     gr.HTML("""
#     <div id="hero-header">
#       <div class="hero-eyebrow">Precision Agriculture Intelligence</div>
#       <div class="hero-title">Soil Health <span>AI</span></div>
#       <p class="hero-subtitle">
#         Multimodal analysis for smarter farming — soil chemistry, crop recommendations,
#         irrigation advisory &amp; AI-powered image insights.
#       </p>
#     </div>
#     """)

#     with gr.Row(equal_height=True):
#         with gr.Column(scale=1):
#             gr.HTML('<div class="section-label">Soil Chemistry</div>')
#             with gr.Group(elem_classes="input-panel"):
#                 N   = gr.Slider(0,   140, 50,  label="Nitrogen (kg/ha)")
#                 P   = gr.Slider(5,   145, 50,  label="Phosphorus (kg/ha)")
#                 K   = gr.Slider(5,   200, 50,  label="Potassium (kg/ha)")
#                 pH  = gr.Slider(3,   10,  6.5, label="pH Level")
#                 OC  = gr.Slider(0.5, 20,  5,   label="Organic Carbon (%)")
#                 SD  = gr.Slider(4,   96,  50,  label="Sand Content (%)")

#         with gr.Column(scale=1):
#             gr.HTML('<div class="section-label">Environment & Location</div>')
#             with gr.Group(elem_classes="input-panel"):
#                 RF  = gr.Slider(0,    300, 100, label="Rainfall (mm)")
#                 TMP = gr.Slider(0,    50,  25,  label="Temperature (°C)")
#                 HUM = gr.Slider(10,   100, 60,  label="Humidity (%)")
#                 LAT = gr.Slider(-90,  90,  20,  label="Latitude")
#                 LON = gr.Slider(-180, 180, 78,  label="Longitude")
#             gr.HTML('<div class="section-label" style="margin-top:18px;">Soil / Crop Image</div>')
#             with gr.Group(elem_classes="input-panel"):
#                 IMG = gr.Image(label="Upload image (optional)", type="numpy",
#                                show_label=False, height=152)

#     with gr.Row(elem_classes="btn-row"):
#         btn = gr.Button("✦  Run Analysis", variant="primary", elem_id="analyze-btn")

#     gr.HTML('<div class="results-header">Analysis Results</div>')
#     gr.HTML('<hr class="divider">')

#     with gr.Row(equal_height=False):
#         with gr.Column(scale=1):
#             shi_html = gr.HTML(elem_classes="output-card")
#         with gr.Column(scale=1):
#             gauge_plot = gr.Plot(elem_classes="output-card")
#         with gr.Column(scale=1):
#             ndvi_plot_out = gr.Plot(elem_classes="output-card")

#     gr.HTML('<div class="section-label" style="margin-top:24px;">Geospatial View</div>')
#     map_html = gr.HTML(elem_classes="output-card")

#     gr.HTML('<div class="section-label" style="margin-top:24px;">Agronomic Intelligence</div>')
#     with gr.Row(equal_height=False):
#         with gr.Column(scale=1):
#             crop_html = gr.HTML(elem_classes="output-card")
#         with gr.Column(scale=1):
#             fert_html = gr.HTML(elem_classes="output-card")
#         with gr.Column(scale=1):
#             irr_html  = gr.HTML(elem_classes="output-card")

#     gr.HTML('<div class="section-label" style="margin-top:24px;">Image Intelligence & Report</div>')
#     with gr.Row():
#         with gr.Column(scale=2):
#             img_out_html = gr.HTML(elem_classes="output-card")
#         with gr.Column(scale=1):
#             img_out_md = gr.Markdown(label="Image Explanation")
#             pdf_file   = gr.File(label="📥 Download Full PDF Report")

#     btn.click(
#         fn=predict_fn,
#         inputs=[N, P, K, pH, RF, TMP, HUM, OC, SD, IMG, LAT, LON],
#         outputs=[
#             shi_html, gauge_plot, ndvi_plot_out, map_html,
#             crop_html, fert_html, irr_html,
#             img_out_html, img_out_md, pdf_file,
#         ],
#     )

# demo.launch(share=True)

# 


# import os
# import gradio as gr
# import numpy as np
# import plotly.graph_objects as go
# import plotly.express as px
# import folium
# from PIL import Image

# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
# from reportlab.lib.styles import getSampleStyleSheet

# from decision_support import SoilProfile, generate_full_report

# # ── Load image analyzer ───────────────────────────────
# BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
# MODEL_PATH  = os.path.join(BASE_DIR, "soil_image_model.pt")
# LABEL_PATH  = os.path.join(BASE_DIR, "soil_image_labels.json")

# _analyzer = None

# def get_analyzer():
#     global _analyzer
#     if _analyzer is not None:
#         return _analyzer
#     if os.path.exists(MODEL_PATH):
#         try:
#             try:
#                 from image_inference_v2 import SoilImageAnalyzer
#             except ImportError:
#                 from image_inference import SoilImageAnalyzer
#             _analyzer = SoilImageAnalyzer(
#                 model_path=MODEL_PATH,
#                 label_path=LABEL_PATH if os.path.exists(LABEL_PATH) else None,
#                 device="cpu",
#             )
#             print("✅ Image model loaded successfully")
#         except Exception as e:
#             print(f"⚠️  Could not load model: {e}")
#     else:
#         print(f"⚠️  Model not found at: {MODEL_PATH}")
#         print("    → Running in demo mode")
#         print("    → Place soil_image_model.pt in:", BASE_DIR)
#     return _analyzer


# # ── SHI ──────────────────────────────────────────────
# def compute_shi(N, P, K, pH, OC):
#     n  = min(N / 140, 1)
#     p  = min(P / 145, 1)
#     k  = min(K / 200, 1)
#     ph = 1 - abs(pH - 6.5) / 3.5
#     oc = min(OC / 20, 1)
#     return float(np.clip(0.3 * ph + 0.2 * n + 0.15 * p + 0.15 * k + 0.2 * oc, 0, 1))


# def create_gauge(shi):
#     fig = go.Figure(go.Indicator(
#         mode="gauge+number",
#         value=shi,
#         title={"text": "Soil Health Index", "font": {"size": 16, "color": "#c9b8f0", "family": "Outfit"}},
#         number={"font": {"size": 44, "color": "#f5d97e", "family": "Outfit"}, "suffix": ""},
#         gauge={
#             "axis": {"range": [0, 1], "tickcolor": "#7c5cbf", "tickfont": {"color": "#a08ad4"}},
#             "bar": {"color": "#f5d97e"},
#             "bgcolor": "rgba(0,0,0,0)",
#             "borderwidth": 0,
#             "steps": [
#                 {"range": [0, 0.35], "color": "rgba(239,83,80,0.25)"},
#                 {"range": [0.35, 0.5], "color": "rgba(255,183,77,0.25)"},
#                 {"range": [0.5, 1],   "color": "rgba(171,130,255,0.25)"},
#             ],
#             "threshold": {
#                 "line": {"color": "#f5d97e", "width": 3},
#                 "thickness": 0.78,
#                 "value": shi,
#             },
#         }
#     ))
#     fig.update_layout(
#         paper_bgcolor="rgba(0,0,0,0)",
#         plot_bgcolor="rgba(0,0,0,0)",
#         margin=dict(t=40, b=10, l=20, r=20),
#         height=260,
#         font={"family": "Outfit"},
#     )
#     return fig


# def get_ndvi(lat):
#     base = 0.4 + (lat % 10) / 50
#     return [round(base + i * 0.04, 3) for i in range(8)]


# def ndvi_plot(ndvi):
#     fig = px.line(
#         x=list(range(1, 9)), y=ndvi,
#         title="NDVI Trend Over Time",
#         labels={"x": "Time Step", "y": "NDVI"},
#     )
#     fig.update_traces(
#         line=dict(color="#f5d97e", width=3),
#         mode="lines+markers",
#         marker=dict(size=8, color="#ab82ff", symbol="circle"),
#     )
#     fig.update_layout(
#         paper_bgcolor="rgba(0,0,0,0)",
#         plot_bgcolor="rgba(30,18,60,0.5)",
#         font={"family": "Outfit", "color": "#c9b8f0"},
#         title_font={"size": 15, "color": "#f5d97e", "family": "Outfit"},
#         xaxis=dict(gridcolor="rgba(124,92,191,0.2)", linecolor="rgba(124,92,191,0.3)", color="#a08ad4"),
#         yaxis=dict(gridcolor="rgba(124,92,191,0.2)", linecolor="rgba(124,92,191,0.3)", color="#a08ad4"),
#         margin=dict(t=48, b=30, l=40, r=20),
#         height=260,
#     )
#     return fig


# def create_map(lat, lon):
#     m = folium.Map(location=[lat, lon], zoom_start=6, tiles="CartoDB dark_matter")
#     folium.Marker(
#         [lat, lon],
#         tooltip="📍 Soil Sample Location",
#         icon=folium.Icon(color="purple", icon="star", prefix="fa"),
#     ).add_to(m)
#     folium.Circle(
#         radius=50000, location=[lat, lon],
#         color="#ab82ff", fill=True, fill_color="#7c5cbf", fill_opacity=0.15,
#     ).add_to(m)
#     return m._repr_html_()


# def card(title, content, icon=""):
#     return f"""
# <div style="
#   padding: 20px 24px;
#   border-radius: 16px;
#   background: rgba(30,18,60,0.82);
#   margin: 8px 0;
#   border: 1px solid rgba(171,130,255,0.22);
#   box-shadow: 0 4px 24px rgba(0,0,0,0.4), inset 0 1px 0 rgba(245,217,126,0.08);
#   font-family: 'Outfit', sans-serif;
#   backdrop-filter: blur(14px);
# ">
#   <h3 style="margin-top:0; color:#f5d97e; font-size:0.85rem; letter-spacing:0.1em;
#              text-transform:uppercase; font-weight:700; margin-bottom:14px;
#              display:flex; align-items:center; gap:8px;">
#     <span>{icon}</span> {title}
#   </h3>
#   <div style="color:#d4c4f0;">{content}</div>
# </div>"""


# # ── Image analysis ────────────────────────────────────
# def analyze_image(img):
#     analyzer = get_analyzer()

#     if img is None:
#         return (
#             """<div style="padding:24px;border-radius:16px;
#                 background:rgba(30,18,60,0.82);border:1px dashed rgba(171,130,255,0.35);
#                 font-family:'Outfit',sans-serif;text-align:center;">
#   <div style="font-size:2.8rem;margin-bottom:10px;">📸</div>
#   <h3 style="color:#f5d97e;margin:0 0 6px;font-size:1rem;">Image Analysis</h3>
#   <p style="color:#7c5cbf;margin:0;font-size:0.88rem;">Upload a soil or crop image to get AI-powered visual analysis.</p>
# </div>""",
#             "No image uploaded."
#         )

#     if analyzer is None:
#         h, w = (img.shape[0], img.shape[1]) if hasattr(img, "shape") else ("?", "?")
#         return (
#             f"""<div style="padding:20px;border-radius:16px;background:rgba(42,24,10,0.85);
#                 border:1px solid rgba(255,183,77,0.35);font-family:'Outfit',sans-serif;">
#   <h3 style="color:#ffb74d;margin-top:0;font-size:1rem;">⚠️ Demo Mode — Model not loaded</h3>
#   <p style="color:#c9b8f0;font-size:0.88rem;">Place <b>soil_image_model.pt</b> in:</p>
#   <code style="background:rgba(0,0,0,0.35);padding:4px 10px;border-radius:6px;
#                font-size:0.8rem;color:#f5d97e;">{BASE_DIR}</code>
#   <p style="color:#ab82ff;margin-bottom:0;margin-top:10px;font-size:0.88rem;">✅ Image received: {w}×{h}px</p>
# </div>""",
#             f"⚠️ Model not loaded. Put soil_image_model.pt in: {BASE_DIR}"
#         )

#     result = analyzer.analyze(img)
#     return result["html"], result["explanation"]


# # ── PDF ───────────────────────────────────────────────
# def generate_pdf(report, img_explanation=""):
#     path = os.path.join(BASE_DIR, "soil_health_report.pdf")
#     doc  = SimpleDocTemplate(path)
#     styles = getSampleStyleSheet()
#     body = []
#     body.append(Paragraph("Soil Health Report", styles["Title"]))
#     body.append(Spacer(1, 12))

#     sa = report.get("soil_assessment", {})
#     body.append(Paragraph("Soil Health Assessment", styles["Heading2"]))
#     body.append(Paragraph(f"SHI: {sa.get('soil_health_index','N/A')}", styles["Normal"]))
#     body.append(Paragraph(f"Class: {sa.get('soil_class','N/A')}", styles["Normal"]))
#     body.append(Paragraph(sa.get("interpretation", ""), styles["Normal"]))
#     body.append(Spacer(1, 12))

#     if img_explanation:
#         body.append(Paragraph("Image-Based Analysis", styles["Heading2"]))
#         body.append(Paragraph(img_explanation, styles["Normal"]))
#         body.append(Spacer(1, 12))

#     body.append(Paragraph("Crop Recommendations", styles["Heading2"]))
#     for c in report.get("crop_recommendations", []):
#         body.append(Paragraph(
#             f"• {c['crop']} — {c['suitability']} ({c['score_pct']}%)",
#             styles["Normal"]
#         ))
#     body.append(Spacer(1, 12))

#     body.append(Paragraph("Fertilizer Advice", styles["Heading2"]))
#     for r in report.get("fertilizer_advice", {}).get("recommendations", []):
#         body.append(Paragraph(f"• {r}", styles["Normal"]))
#     body.append(Spacer(1, 12))

#     body.append(Paragraph("Irrigation Advice", styles["Heading2"]))
#     irr = report.get("irrigation_advice", {})
#     body.append(Paragraph(f"Level: {irr.get('irrigation_level','')}", styles["Normal"]))
#     body.append(Paragraph(irr.get("advice", ""), styles["Normal"]))

#     doc.build(body)
#     return path


# # ── MAIN PREDICT ──────────────────────────────────────
# def predict_fn(N, P, K, pH, RF, TMP, HUM, OC, SD, IMG, LAT, LON):
#     shi = compute_shi(N, P, K, pH, OC)

#     if shi < 0.35:
#         status, badge_color, badge_bg = "Poor",     "#ef5350", "rgba(239,83,80,0.18)"
#         icon = "🔴"
#     elif shi < 0.5:
#         status, badge_color, badge_bg = "Moderate", "#ffb74d", "rgba(255,183,77,0.18)"
#         icon = "🟡"
#     else:
#         status, badge_color, badge_bg = "Healthy",  "#ab82ff", "rgba(171,130,255,0.22)"
#         icon = "✨"

#     profile = SoilProfile(N=N, P=P, K=K, pH=pH,
#                           rainfall=RF, temperature=TMP, humidity=HUM,
#                           organic_carbon=OC, sand=SD,
#                           shi=shi, soil_class=status)
#     report = generate_full_report(profile)
#     img_html, img_text = analyze_image(IMG)

#     # ── SHI Hero Card ──
#     shi_card = f"""
# <div style="
#   padding: 32px 28px;
#   border-radius: 20px;
#   background: linear-gradient(145deg, rgba(42,24,80,0.96), rgba(18,10,46,0.99));
#   border: 1px solid rgba(245,217,126,0.22);
#   box-shadow: 0 8px 40px rgba(0,0,0,0.55),
#               0 0 0 1px rgba(171,130,255,0.1),
#               inset 0 1px 0 rgba(245,217,126,0.1);
#   font-family: 'Outfit', sans-serif;
#   text-align: center;
#   position: relative;
#   overflow: hidden;
# ">
#   <div style="
#     position:absolute;top:-50px;left:50%;transform:translateX(-50%);
#     width:200px;height:200px;
#     background:radial-gradient(circle, rgba(171,130,255,0.15) 0%, transparent 70%);
#     pointer-events:none;
#   "></div>
#   <div style="font-size:2.8rem;margin-bottom:10px;position:relative;">{icon}</div>
#   <div style="font-size:4.2rem;font-weight:800;color:#f5d97e;
#               line-height:1;letter-spacing:-3px;position:relative;">
#     {shi:.3f}
#   </div>
#   <div style="font-size:0.72rem;color:#7c5cbf;margin-top:10px;letter-spacing:0.16em;
#               text-transform:uppercase;font-weight:600;">
#     Soil Health Index
#   </div>
#   <div style="
#     display:inline-block;margin-top:16px;
#     padding:7px 26px;border-radius:50px;
#     background:{badge_bg};
#     border:1.5px solid {badge_color}88;
#     color:{badge_color};font-weight:700;font-size:0.9rem;letter-spacing:0.05em;
#   ">{status}</div>
# </div>"""

#     # ── Crop Card ──
#     crops = report.get("crop_recommendations", [])
#     crop_rows = ""
#     for c in crops:
#         pct = c['score_pct']
#         bar_color = "#ab82ff" if pct >= 70 else ("#ffb74d" if pct >= 50 else "#ef5350")
#         issues = ', '.join(c['issues']) if c['issues'] else "All conditions met ✓"
#         crop_rows += f"""
# <div style="margin-bottom:16px;">
#   <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:5px;">
#     <span style="font-weight:600;color:#e8dcff;font-size:0.9rem;">🌾 {c['crop']}</span>
#     <span style="font-size:0.78rem;color:{bar_color};font-weight:700;
#                  background:rgba(0,0,0,0.3);padding:2px 10px;border-radius:50px;
#                  border:1px solid {bar_color}44;">
#       {c['suitability']} · {pct}%
#     </span>
#   </div>
#   <div style="background:rgba(124,92,191,0.2);border-radius:50px;height:6px;overflow:hidden;">
#     <div style="width:{pct}%;height:100%;
#                 background:linear-gradient(90deg,{bar_color}88,{bar_color});
#                 border-radius:50px;"></div>
#   </div>
#   <div style="font-size:0.73rem;color:#6b4fa8;margin-top:4px;">{issues}</div>
# </div>"""
#     crop_card = card("Crop Recommendations", crop_rows, "🌾")

#     # ── Fertilizer Card ──
#     fert = report.get("fertilizer_advice", {})
#     fert_items = "".join(
#         f'<div style="display:flex;align-items:flex-start;gap:10px;margin-bottom:12px;">'
#         f'<span style="color:#f5d97e;font-size:0.9rem;margin-top:3px;flex-shrink:0;">◆</span>'
#         f'<span style="color:#d4c4f0;font-size:0.87rem;line-height:1.55;">{r}</span>'
#         f'</div>'
#         for r in fert.get("recommendations", [])
#     )
#     fert_card = card("Fertilizer Recommendations", fert_items, "🧪")

#     # ── Irrigation Card ──
#     irr = report.get("irrigation_advice", {})
#     irr_content = f"""
# <div style="display:flex;align-items:center;gap:12px;margin-bottom:14px;flex-wrap:wrap;">
#   <div style="
#     background:linear-gradient(135deg,#5c3d9e,#9b5de5);
#     color:white;padding:7px 20px;border-radius:50px;
#     font-weight:700;font-size:0.85rem;letter-spacing:0.04em;white-space:nowrap;
#     box-shadow:0 4px 14px rgba(124,92,191,0.4);
#   ">{irr.get('irrigation_level','')}</div>
#   <div style="color:#a08ad4;font-size:0.87rem;">{irr.get('frequency','')}</div>
# </div>
# <p style="color:#d4c4f0;font-size:0.87rem;line-height:1.6;margin:0;">{irr.get('advice','')}</p>"""
#     irr_card = card("Irrigation Advisory", irr_content, "💧")

#     pdf = generate_pdf(report, img_text)

#     return (shi_card, create_gauge(shi), ndvi_plot(get_ndvi(LAT)),
#             create_map(LAT, LON), crop_card, fert_card, irr_card,
#             img_html, img_text, pdf)


# # ── CUSTOM CSS ────────────────────────────────────────
# CUSTOM_CSS = """
# @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Syne:wght@700;800&display=swap');

# :root {
#   --purple-deep:    #0d0820;
#   --purple-dark:    #1a0f3c;
#   --purple-mid:     #2a1850;
#   --purple-card:    rgba(30,18,60,0.82);
#   --purple-border:  rgba(171,130,255,0.2);
#   --purple-accent:  #ab82ff;
#   --purple-soft:    #7c5cbf;
#   --gold:           #f5d97e;
#   --gold-dim:       #c9a84c;
#   --text-primary:   #f0e8ff;
#   --text-secondary: #c9b8f0;
#   --text-muted:     #7c5cbf;
#   --shadow-glow:    0 0 50px rgba(124,92,191,0.2);
# }

# *, *::before, *::after { box-sizing: border-box; }

# body, .gradio-container {
#   font-family: 'Outfit', sans-serif !important;
#   background: radial-gradient(ellipse at 20% 10%, #2a1060 0%, #0d0820 45%, #060414 100%) !important;
#   min-height: 100vh;
#   color: var(--text-primary) !important;
# }

# /* ── Ambient glow orbs ── */
# .gradio-container::before {
#   content: "";
#   position: fixed;
#   inset: 0;
#   background:
#     radial-gradient(ellipse 600px 400px at 10% 20%, rgba(124,92,191,0.12) 0%, transparent 70%),
#     radial-gradient(ellipse 400px 300px at 90% 80%, rgba(245,217,126,0.07) 0%, transparent 70%),
#     radial-gradient(ellipse 300px 400px at 80% 15%, rgba(155,93,229,0.08) 0%, transparent 70%);
#   pointer-events: none;
#   z-index: 0;
# }

# /* ── Hero ── */
# #hero-header {
#   text-align: center;
#   padding: 56px 24px 38px;
#   position: relative;
#   z-index: 1;
# }

# .hero-eyebrow {
#   font-size: 0.7rem;
#   font-weight: 600;
#   letter-spacing: 0.2em;
#   text-transform: uppercase;
#   color: var(--gold);
#   margin-bottom: 14px;
#   display: flex;
#   align-items: center;
#   justify-content: center;
#   gap: 12px;
#   opacity: 0.85;
# }

# .hero-eyebrow::before,
# .hero-eyebrow::after {
#   content: "";
#   display: inline-block;
#   width: 36px;
#   height: 1px;
#   background: linear-gradient(90deg, transparent, var(--gold-dim));
# }
# .hero-eyebrow::after {
#   background: linear-gradient(90deg, var(--gold-dim), transparent);
# }

# .hero-title {
#   font-family: 'Syne', sans-serif !important;
#   font-size: clamp(2.2rem, 5.5vw, 3.4rem) !important;
#   font-weight: 800 !important;
#   color: var(--text-primary) !important;
#   letter-spacing: -1.5px !important;
#   margin: 0 0 12px !important;
#   line-height: 1.05 !important;
#   text-shadow: 0 0 80px rgba(171,130,255,0.35) !important;
# }

# .hero-title span {
#   background: linear-gradient(135deg, #f5d97e 30%, #e0b8ff);
#   -webkit-background-clip: text;
#   -webkit-text-fill-color: transparent;
#   background-clip: text;
# }

# .hero-subtitle {
#   font-size: 0.97rem !important;
#   color: var(--text-muted) !important;
#   font-weight: 400 !important;
#   max-width: 500px;
#   margin: 0 auto !important;
#   line-height: 1.65 !important;
# }

# /* ── Section labels ── */
# .section-label {
#   font-size: 0.67rem !important;
#   font-weight: 700 !important;
#   letter-spacing: 0.18em !important;
#   text-transform: uppercase !important;
#   color: var(--gold) !important;
#   margin: 0 0 12px !important;
#   display: flex;
#   align-items: center;
#   gap: 10px;
#   opacity: 0.85;
# }

# .section-label::before {
#   content: "";
#   display: inline-block;
#   width: 18px;
#   height: 1.5px;
#   background: var(--gold-dim);
#   border-radius: 1px;
# }

# /* ── Input panels ── */
# .input-panel {
#   background: rgba(26,15,60,0.75) !important;
#   border: 1px solid var(--purple-border) !important;
#   border-radius: 20px !important;
#   padding: 24px !important;
#   box-shadow: 0 8px 36px rgba(0,0,0,0.45),
#               inset 0 1px 0 rgba(245,217,126,0.06),
#               var(--shadow-glow) !important;
#   backdrop-filter: blur(18px) !important;
# }

# /* ── Sliders ── */
# .gradio-slider input[type=range] {
#   accent-color: var(--purple-accent) !important;
# }

# label span {
#   font-size: 0.83rem !important;
#   font-weight: 500 !important;
#   color: var(--text-secondary) !important;
# }

# input[type="number"] {
#   background: rgba(124,92,191,0.12) !important;
#   border: 1px solid var(--purple-border) !important;
#   border-radius: 8px !important;
#   color: var(--gold) !important;
#   font-family: 'Outfit', sans-serif !important;
#   font-size: 0.85rem !important;
# }

# /* ── Analyze button ── */
# #analyze-btn {
#   background: linear-gradient(135deg, #6b3fa0 0%, #9b5de5 50%, #f5c842 100%) !important;
#   color: #0d0820 !important;
#   font-family: 'Syne', sans-serif !important;
#   font-size: 0.9rem !important;
#   font-weight: 800 !important;
#   letter-spacing: 0.12em !important;
#   text-transform: uppercase !important;
#   padding: 16px 56px !important;
#   border-radius: 50px !important;
#   border: none !important;
#   cursor: pointer !important;
#   box-shadow: 0 6px 30px rgba(155,93,229,0.5),
#               0 0 0 1px rgba(245,217,126,0.15),
#               inset 0 1px 0 rgba(255,255,255,0.15) !important;
#   transition: transform 0.25s cubic-bezier(0.34,1.56,0.64,1),
#               box-shadow 0.25s ease !important;
#   min-width: 240px !important;
# }

# #analyze-btn:hover {
#   transform: translateY(-4px) scale(1.05) !important;
#   box-shadow: 0 16px 44px rgba(155,93,229,0.6),
#               0 0 70px rgba(245,217,126,0.12) !important;
# }

# #analyze-btn:active {
#   transform: translateY(0) scale(0.97) !important;
# }

# .btn-row {
#   display: flex !important;
#   justify-content: center !important;
#   padding: 12px 0 30px !important;
# }

# /* ── Output cards ── */
# .output-card {
#   background: rgba(26,15,60,0.75) !important;
#   border: 1px solid var(--purple-border) !important;
#   border-radius: 16px !important;
#   padding: 20px !important;
#   box-shadow: 0 4px 26px rgba(0,0,0,0.4),
#               inset 0 1px 0 rgba(245,217,126,0.05) !important;
#   backdrop-filter: blur(14px) !important;
# }

# .gradio-plot, .gradio-html {
#   background: transparent !important;
#   border-radius: 16px !important;
# }

# .gradio-image {
#   border-radius: 14px !important;
#   border: 2px dashed rgba(171,130,255,0.3) !important;
#   background: rgba(26,15,60,0.5) !important;
# }
# .gradio-image:hover {
#   border-color: rgba(245,217,126,0.45) !important;
# }

# .gradio-markdown {
#   font-family: 'Outfit', sans-serif !important;
#   font-size: 0.87rem !important;
#   color: var(--text-secondary) !important;
#   background: rgba(26,15,60,0.65) !important;
#   border-radius: 10px !important;
#   padding: 14px !important;
#   border: 1px solid var(--purple-border) !important;
#   line-height: 1.6 !important;
# }

# .gradio-file {
#   background: rgba(26,15,60,0.7) !important;
#   border: 1px solid rgba(245,217,126,0.18) !important;
#   border-radius: 10px !important;
# }

# .divider {
#   border: none;
#   border-top: 1px solid rgba(124,92,191,0.18);
#   margin: 6px 0 22px;
# }

# .results-header {
#   font-family: 'Syne', sans-serif !important;
#   font-size: 1.25rem !important;
#   font-weight: 800 !important;
#   color: var(--text-primary) !important;
#   text-align: center !important;
#   margin: 28px 0 12px !important;
#   letter-spacing: -0.02em !important;
# }

# ::-webkit-scrollbar { width: 5px; }
# ::-webkit-scrollbar-track { background: #0d0820; }
# ::-webkit-scrollbar-thumb { background: #3d2770; border-radius: 3px; }
# ::-webkit-scrollbar-thumb:hover { background: #ab82ff; }

# @keyframes fadeUp {
#   from { opacity: 0; transform: translateY(18px); }
#   to   { opacity: 1; transform: translateY(0); }
# }
# .gradio-container > * { animation: fadeUp 0.5s ease both; }
# """

# # ── UI ────────────────────────────────────────────────
# with gr.Blocks(title="🌱 Soil Health AI", css=CUSTOM_CSS) as demo:

#     gr.HTML("""
#     <div id="hero-header">
#       <div class="hero-eyebrow">Precision Agriculture Intelligence</div>
#       <div class="hero-title">Soil Health <span>AI</span></div>
#       <p class="hero-subtitle">
#         Multimodal analysis for smarter farming — soil chemistry, crop recommendations,
#         irrigation advisory &amp; AI-powered image insights.
#       </p>
#     </div>
#     """)

#     with gr.Row(equal_height=True):
#         with gr.Column(scale=1):
#             gr.HTML('<div class="section-label">Soil Chemistry</div>')
#             with gr.Group(elem_classes="input-panel"):
#                 N   = gr.Slider(0,   140, 50,  label="Nitrogen (kg/ha)")
#                 P   = gr.Slider(5,   145, 50,  label="Phosphorus (kg/ha)")
#                 K   = gr.Slider(5,   200, 50,  label="Potassium (kg/ha)")
#                 pH  = gr.Slider(3,   10,  6.5, label="pH Level")
#                 OC  = gr.Slider(0.5, 20,  5,   label="Organic Carbon (%)")
#                 SD  = gr.Slider(4,   96,  50,  label="Sand Content (%)")

#         with gr.Column(scale=1):
#             gr.HTML('<div class="section-label">Environment & Location</div>')
#             with gr.Group(elem_classes="input-panel"):
#                 RF  = gr.Slider(0,    300, 100, label="Rainfall (mm)")
#                 TMP = gr.Slider(0,    50,  25,  label="Temperature (°C)")
#                 HUM = gr.Slider(10,   100, 60,  label="Humidity (%)")
#                 LAT = gr.Slider(-90,  90,  20,  label="Latitude")
#                 LON = gr.Slider(-180, 180, 78,  label="Longitude")
#             gr.HTML('<div class="section-label" style="margin-top:18px;">Soil / Crop Image</div>')
#             with gr.Group(elem_classes="input-panel"):
#                 IMG = gr.Image(label="Upload image (optional)", type="numpy",
#                                show_label=False, height=152)

#     with gr.Row(elem_classes="btn-row"):
#         btn = gr.Button("✦  Run Analysis", variant="primary", elem_id="analyze-btn")

#     gr.HTML('<div class="results-header">Analysis Results</div>')
#     gr.HTML('<hr class="divider">')

#     with gr.Row(equal_height=False):
#         with gr.Column(scale=1):
#             shi_html = gr.HTML(elem_classes="output-card")
#         with gr.Column(scale=1):
#             gauge_plot = gr.Plot(elem_classes="output-card")
#         with gr.Column(scale=1):
#             ndvi_plot_out = gr.Plot(elem_classes="output-card")

#     gr.HTML('<div class="section-label" style="margin-top:24px;">Geospatial View</div>')
#     map_html = gr.HTML(elem_classes="output-card")

#     gr.HTML('<div class="section-label" style="margin-top:24px;">Agronomic Intelligence</div>')
#     with gr.Row(equal_height=False):
#         with gr.Column(scale=1):
#             crop_html = gr.HTML(elem_classes="output-card")
#         with gr.Column(scale=1):
#             fert_html = gr.HTML(elem_classes="output-card")
#         with gr.Column(scale=1):
#             irr_html  = gr.HTML(elem_classes="output-card")

#     gr.HTML('<div class="section-label" style="margin-top:24px;">Image Intelligence & Report</div>')
#     with gr.Row():
#         with gr.Column(scale=2):
#             img_out_html = gr.HTML(elem_classes="output-card")
#         with gr.Column(scale=1):
#             img_out_md = gr.Markdown(label="Image Explanation")
#             pdf_file   = gr.File(label="📥 Download Full PDF Report")

#     btn.click(
#         fn=predict_fn,
#         inputs=[N, P, K, pH, RF, TMP, HUM, OC, SD, IMG, LAT, LON],
#         outputs=[
#             shi_html, gauge_plot, ndvi_plot_out, map_html,
#             crop_html, fert_html, irr_html,
#             img_out_html, img_out_md, pdf_file,
#         ],
#     )

# demo.launch(share=True)



# import os
# import gradio as gr
# import numpy as np
# import plotly.graph_objects as go
# import plotly.express as px
# import folium
# from PIL import Image

# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
# from reportlab.lib.styles import getSampleStyleSheet

# from decision_support import SoilProfile, generate_full_report

# # ── Load image analyzer ───────────────────────────────
# BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
# MODEL_PATH  = os.path.join(BASE_DIR, "soil_image_model.pt")
# LABEL_PATH  = os.path.join(BASE_DIR, "soil_image_labels.json")

# _analyzer = None

# def get_analyzer():
#     global _analyzer
#     if _analyzer is not None:
#         return _analyzer
#     if os.path.exists(MODEL_PATH):
#         try:
#             try:
#                 from image_inference_v2 import SoilImageAnalyzer
#             except ImportError:
#                 from image_inference import SoilImageAnalyzer
#             _analyzer = SoilImageAnalyzer(
#                 model_path=MODEL_PATH,
#                 label_path=LABEL_PATH if os.path.exists(LABEL_PATH) else None,
#                 device="cpu",
#             )
#             print("✅ Image model loaded successfully")
#         except Exception as e:
#             print(f"⚠️  Could not load model: {e}")
#     else:
#         print(f"⚠️  Model not found at: {MODEL_PATH}")
#         print("    → Running in demo mode")
#         print("    → Place soil_image_model.pt in:", BASE_DIR)
#     return _analyzer


# # ── SHI ──────────────────────────────────────────────
# def compute_shi(N, P, K, pH, OC):
#     n  = min(N / 140, 1)
#     p  = min(P / 145, 1)
#     k  = min(K / 200, 1)
#     ph = 1 - abs(pH - 6.5) / 3.5
#     oc = min(OC / 20, 1)
#     return float(np.clip(0.3 * ph + 0.2 * n + 0.15 * p + 0.15 * k + 0.2 * oc, 0, 1))


# def create_gauge(shi):
#     fig = go.Figure(go.Indicator(
#         mode="gauge+number",
#         value=shi,
#         title={"text": "Soil Health Index", "font": {"size": 16, "color": "#c9b8f0", "family": "Outfit"}},
#         number={"font": {"size": 44, "color": "#f5d97e", "family": "Outfit"}, "suffix": ""},
#         gauge={
#             "axis": {"range": [0, 1], "tickcolor": "#7c5cbf", "tickfont": {"color": "#a08ad4"}},
#             "bar": {"color": "#f5d97e"},
#             "bgcolor": "rgba(0,0,0,0)",
#             "borderwidth": 0,
#             "steps": [
#                 {"range": [0, 0.35], "color": "rgba(239,83,80,0.25)"},
#                 {"range": [0.35, 0.5], "color": "rgba(255,183,77,0.25)"},
#                 {"range": [0.5, 1],   "color": "rgba(171,130,255,0.25)"},
#             ],
#             "threshold": {
#                 "line": {"color": "#f5d97e", "width": 3},
#                 "thickness": 0.78,
#                 "value": shi,
#             },
#         }
#     ))
#     fig.update_layout(
#         paper_bgcolor="rgba(0,0,0,0)",
#         plot_bgcolor="rgba(0,0,0,0)",
#         margin=dict(t=40, b=10, l=20, r=20),
#         height=260,
#         font={"family": "Outfit"},
#     )
#     return fig


# def get_ndvi(lat):
#     base = 0.4 + (lat % 10) / 50
#     return [round(base + i * 0.04, 3) for i in range(8)]


# def ndvi_plot(ndvi):
#     fig = px.line(
#         x=list(range(1, 9)), y=ndvi,
#         title="NDVI Trend Over Time",
#         labels={"x": "Time Step", "y": "NDVI"},
#     )
#     fig.update_traces(
#         line=dict(color="#f5d97e", width=3),
#         mode="lines+markers",
#         marker=dict(size=8, color="#ab82ff", symbol="circle"),
#     )
#     fig.update_layout(
#         paper_bgcolor="rgba(0,0,0,0)",
#         plot_bgcolor="rgba(30,18,60,0.5)",
#         font={"family": "Outfit", "color": "#c9b8f0"},
#         title_font={"size": 15, "color": "#f5d97e", "family": "Outfit"},
#         xaxis=dict(gridcolor="rgba(124,92,191,0.2)", linecolor="rgba(124,92,191,0.3)", color="#a08ad4"),
#         yaxis=dict(gridcolor="rgba(124,92,191,0.2)", linecolor="rgba(124,92,191,0.3)", color="#a08ad4"),
#         margin=dict(t=48, b=30, l=40, r=20),
#         height=260,
#     )
#     return fig


# def create_map(lat, lon):
#     m = folium.Map(location=[lat, lon], zoom_start=6, tiles="CartoDB dark_matter")
#     folium.Marker(
#         [lat, lon],
#         tooltip="📍 Soil Sample Location",
#         icon=folium.Icon(color="purple", icon="star", prefix="fa"),
#     ).add_to(m)
#     folium.Circle(
#         radius=50000, location=[lat, lon],
#         color="#ab82ff", fill=True, fill_color="#7c5cbf", fill_opacity=0.15,
#     ).add_to(m)
#     return m._repr_html_()


# def card(title, content, icon=""):
#     return f"""
# <div style="
#   padding: 20px 24px;
#   border-radius: 16px;
#   background: rgba(30,18,60,0.82);
#   margin: 8px 0;
#   border: 1px solid rgba(171,130,255,0.22);
#   box-shadow: 0 4px 24px rgba(0,0,0,0.4), inset 0 1px 0 rgba(245,217,126,0.08);
#   font-family: 'Outfit', sans-serif;
#   backdrop-filter: blur(14px);
# ">
#   <h3 style="margin-top:0; color:#f5d97e; font-size:0.85rem; letter-spacing:0.1em;
#              text-transform:uppercase; font-weight:700; margin-bottom:14px;
#              display:flex; align-items:center; gap:8px;">
#     <span>{icon}</span> {title}
#   </h3>
#   <div style="color:#e8deff;">{content}</div>
# </div>"""


# # ── Image analysis ────────────────────────────────────
# def analyze_image(img):
#     analyzer = get_analyzer()

#     if img is None:
#         return (
#             """<div style="padding:24px;border-radius:16px;
#                 background:rgba(30,18,60,0.82);border:1px dashed rgba(171,130,255,0.35);
#                 font-family:'Outfit',sans-serif;text-align:center;">
#   <div style="font-size:2.8rem;margin-bottom:10px;">📸</div>
#   <h3 style="color:#f5d97e;margin:0 0 6px;font-size:1rem;">Image Analysis</h3>
#   <p style="color:#b8a8e0;margin:0;font-size:0.88rem;">Upload a soil or crop image to get AI-powered visual analysis.</p>
# </div>""",
#             "No image uploaded."
#         )

#     if analyzer is None:
#         h, w = (img.shape[0], img.shape[1]) if hasattr(img, "shape") else ("?", "?")
#         return (
#             f"""<div style="padding:20px;border-radius:16px;background:rgba(42,24,10,0.85);
#                 border:1px solid rgba(255,183,77,0.35);font-family:'Outfit',sans-serif;">
#   <h3 style="color:#ffb74d;margin-top:0;font-size:1rem;">⚠️ Demo Mode — Model not loaded</h3>
#   <p style="color:#e0d4ff;font-size:0.88rem;">Place <b>soil_image_model.pt</b> in:</p>
#   <code style="background:rgba(0,0,0,0.35);padding:4px 10px;border-radius:6px;
#                font-size:0.8rem;color:#f5d97e;">{BASE_DIR}</code>
#   <p style="color:#c4a8ff;margin-bottom:0;margin-top:10px;font-size:0.88rem;">✅ Image received: {w}×{h}px</p>
# </div>""",
#             f"⚠️ Model not loaded. Put soil_image_model.pt in: {BASE_DIR}"
#         )

#     result = analyzer.analyze(img)
#     return result["html"], result["explanation"]


# # ── PDF ───────────────────────────────────────────────
# def generate_pdf(report, img_explanation=""):
#     path = os.path.join(BASE_DIR, "soil_health_report.pdf")
#     doc  = SimpleDocTemplate(path)
#     styles = getSampleStyleSheet()
#     body = []
#     body.append(Paragraph("Soil Health Report", styles["Title"]))
#     body.append(Spacer(1, 12))

#     sa = report.get("soil_assessment", {})
#     body.append(Paragraph("Soil Health Assessment", styles["Heading2"]))
#     body.append(Paragraph(f"SHI: {sa.get('soil_health_index','N/A')}", styles["Normal"]))
#     body.append(Paragraph(f"Class: {sa.get('soil_class','N/A')}", styles["Normal"]))
#     body.append(Paragraph(sa.get("interpretation", ""), styles["Normal"]))
#     body.append(Spacer(1, 12))

#     if img_explanation:
#         body.append(Paragraph("Image-Based Analysis", styles["Heading2"]))
#         body.append(Paragraph(img_explanation, styles["Normal"]))
#         body.append(Spacer(1, 12))

#     body.append(Paragraph("Crop Recommendations", styles["Heading2"]))
#     for c in report.get("crop_recommendations", []):
#         body.append(Paragraph(
#             f"• {c['crop']} — {c['suitability']} ({c['score_pct']}%)",
#             styles["Normal"]
#         ))
#     body.append(Spacer(1, 12))

#     body.append(Paragraph("Fertilizer Advice", styles["Heading2"]))
#     for r in report.get("fertilizer_advice", {}).get("recommendations", []):
#         body.append(Paragraph(f"• {r}", styles["Normal"]))
#     body.append(Spacer(1, 12))

#     body.append(Paragraph("Irrigation Advice", styles["Heading2"]))
#     irr = report.get("irrigation_advice", {})
#     body.append(Paragraph(f"Level: {irr.get('irrigation_level','')}", styles["Normal"]))
#     body.append(Paragraph(irr.get("advice", ""), styles["Normal"]))

#     doc.build(body)
#     return path


# # ── MAIN PREDICT ──────────────────────────────────────
# def predict_fn(N, P, K, pH, RF, TMP, HUM, OC, SD, IMG, LAT, LON):
#     shi = compute_shi(N, P, K, pH, OC)

#     if shi < 0.35:
#         status, badge_color, badge_bg = "Poor",     "#ef5350", "rgba(239,83,80,0.18)"
#         icon = "🔴"
#     elif shi < 0.5:
#         status, badge_color, badge_bg = "Moderate", "#ffb74d", "rgba(255,183,77,0.18)"
#         icon = "🟡"
#     else:
#         status, badge_color, badge_bg = "Healthy",  "#ab82ff", "rgba(171,130,255,0.22)"
#         icon = "✨"

#     profile = SoilProfile(N=N, P=P, K=K, pH=pH,
#                           rainfall=RF, temperature=TMP, humidity=HUM,
#                           organic_carbon=OC, sand=SD,
#                           shi=shi, soil_class=status)
#     report = generate_full_report(profile)
#     img_html, img_text = analyze_image(IMG)

#     # ── SHI Hero Card ──
#     shi_card = f"""
# <div style="
#   padding: 32px 28px;
#   border-radius: 20px;
#   background: linear-gradient(145deg, rgba(42,24,80,0.96), rgba(18,10,46,0.99));
#   border: 1px solid rgba(245,217,126,0.22);
#   box-shadow: 0 8px 40px rgba(0,0,0,0.55),
#               0 0 0 1px rgba(171,130,255,0.1),
#               inset 0 1px 0 rgba(245,217,126,0.1);
#   font-family: 'Outfit', sans-serif;
#   text-align: center;
#   position: relative;
#   overflow: hidden;
# ">
#   <div style="
#     position:absolute;top:-50px;left:50%;transform:translateX(-50%);
#     width:200px;height:200px;
#     background:radial-gradient(circle, rgba(171,130,255,0.15) 0%, transparent 70%);
#     pointer-events:none;
#   "></div>
#   <div style="font-size:2.8rem;margin-bottom:10px;position:relative;">{icon}</div>
#   <div style="font-size:4.2rem;font-weight:800;color:#f5d97e;
#               line-height:1;letter-spacing:-3px;position:relative;">
#     {shi:.3f}
#   </div>
#   <div style="font-size:0.72rem;color:#b8a8e0;margin-top:10px;letter-spacing:0.16em;
#               text-transform:uppercase;font-weight:600;">
#     Soil Health Index
#   </div>
#   <div style="
#     display:inline-block;margin-top:16px;
#     padding:7px 26px;border-radius:50px;
#     background:{badge_bg};
#     border:1.5px solid {badge_color}88;
#     color:{badge_color};font-weight:700;font-size:0.9rem;letter-spacing:0.05em;
#   ">{status}</div>
# </div>"""

#     # ── Crop Card ──
#     crops = report.get("crop_recommendations", [])
#     crop_rows = ""
#     for c in crops:
#         pct = c['score_pct']
#         bar_color = "#ab82ff" if pct >= 70 else ("#ffb74d" if pct >= 50 else "#ef5350")
#         issues = ', '.join(c['issues']) if c['issues'] else "All conditions met ✓"
#         crop_rows += f"""
# <div style="margin-bottom:16px;">
#   <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:5px;">
#     <span style="font-weight:600;color:#f0e8ff;font-size:0.9rem;">🌾 {c['crop']}</span>
#     <span style="font-size:0.78rem;color:{bar_color};font-weight:700;
#                  background:rgba(0,0,0,0.3);padding:2px 10px;border-radius:50px;
#                  border:1px solid {bar_color}44;">
#       {c['suitability']} · {pct}%
#     </span>
#   </div>
#   <div style="background:rgba(124,92,191,0.2);border-radius:50px;height:6px;overflow:hidden;">
#     <div style="width:{pct}%;height:100%;
#                 background:linear-gradient(90deg,{bar_color}88,{bar_color});
#                 border-radius:50px;"></div>
#   </div>
#   <div style="font-size:0.73rem;color:#a090cc;margin-top:4px;">{issues}</div>
# </div>"""
#     crop_card = card("Crop Recommendations", crop_rows, "🌾")

#     # ── Fertilizer Card ──
#     fert = report.get("fertilizer_advice", {})
#     fert_items = "".join(
#         f'<div style="display:flex;align-items:flex-start;gap:10px;margin-bottom:12px;">'
#         f'<span style="color:#f5d97e;font-size:0.9rem;margin-top:3px;flex-shrink:0;">◆</span>'
#         f'<span style="color:#e8deff;font-size:0.87rem;line-height:1.55;">{r}</span>'
#         f'</div>'
#         for r in fert.get("recommendations", [])
#     )
#     fert_card = card("Fertilizer Recommendations", fert_items, "🧪")

#     # ── Irrigation Card ──
#     irr = report.get("irrigation_advice", {})
#     irr_content = f"""
# <div style="display:flex;align-items:center;gap:12px;margin-bottom:14px;flex-wrap:wrap;">
#   <div style="
#     background:linear-gradient(135deg,#5c3d9e,#9b5de5);
#     color:white;padding:7px 20px;border-radius:50px;
#     font-weight:700;font-size:0.85rem;letter-spacing:0.04em;white-space:nowrap;
#     box-shadow:0 4px 14px rgba(124,92,191,0.4);
#   ">{irr.get('irrigation_level','')}</div>
#   <div style="color:#c4b4f0;font-size:0.87rem;">{irr.get('frequency','')}</div>
# </div>
# <p style="color:#e8deff;font-size:0.87rem;line-height:1.6;margin:0;">{irr.get('advice','')}</p>"""
#     irr_card = card("Irrigation Advisory", irr_content, "💧")

#     pdf = generate_pdf(report, img_text)

#     return (shi_card, create_gauge(shi), ndvi_plot(get_ndvi(LAT)),
#             create_map(LAT, LON), crop_card, fert_card, irr_card,
#             img_html, img_text, pdf)


# # ── CUSTOM CSS ────────────────────────────────────────
# CUSTOM_CSS = """
# @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Syne:wght@700;800&display=swap');

# :root {
#   --purple-deep:    #0d0820;
#   --purple-dark:    #1a0f3c;
#   --purple-mid:     #2a1850;
#   --purple-card:    rgba(30,18,60,0.82);
#   --purple-border:  rgba(171,130,255,0.25);
#   --purple-accent:  #c4a8ff;
#   --purple-soft:    #9b7fd4;
#   --gold:           #f5d97e;
#   --gold-dim:       #c9a84c;
#   --text-primary:   #f5f0ff;
#   --text-secondary: #e8deff;
#   --text-muted:     #c4b4f0;
#   --shadow-glow:    0 0 50px rgba(124,92,191,0.2);
# }

# *, *::before, *::after { box-sizing: border-box; }

# body, .gradio-container {
#   font-family: 'Outfit', sans-serif !important;
#   background: radial-gradient(ellipse at 20% 10%, #2a1060 0%, #0d0820 45%, #060414 100%) !important;
#   min-height: 100vh;
#   color: var(--text-primary) !important;
# }

# /* ── Ambient glow orbs ── */
# .gradio-container::before {
#   content: "";
#   position: fixed;
#   inset: 0;
#   background:
#     radial-gradient(ellipse 600px 400px at 10% 20%, rgba(124,92,191,0.12) 0%, transparent 70%),
#     radial-gradient(ellipse 400px 300px at 90% 80%, rgba(245,217,126,0.07) 0%, transparent 70%),
#     radial-gradient(ellipse 300px 400px at 80% 15%, rgba(155,93,229,0.08) 0%, transparent 70%);
#   pointer-events: none;
#   z-index: 0;
# }

# /* ── Hero ── */
# #hero-header {
#   text-align: center;
#   padding: 56px 24px 38px;
#   position: relative;
#   z-index: 1;
# }

# .hero-eyebrow {
#   font-size: 0.72rem;
#   font-weight: 600;
#   letter-spacing: 0.2em;
#   text-transform: uppercase;
#   color: var(--gold);
#   margin-bottom: 14px;
#   display: flex;
#   align-items: center;
#   justify-content: center;
#   gap: 12px;
#   opacity: 0.9;
# }

# .hero-eyebrow::before,
# .hero-eyebrow::after {
#   content: "";
#   display: inline-block;
#   width: 36px;
#   height: 1px;
#   background: linear-gradient(90deg, transparent, var(--gold-dim));
# }
# .hero-eyebrow::after {
#   background: linear-gradient(90deg, var(--gold-dim), transparent);
# }

# .hero-title {
#   font-family: 'Syne', sans-serif !important;
#   font-size: clamp(2.2rem, 5.5vw, 3.4rem) !important;
#   font-weight: 800 !important;
#   color: var(--text-primary) !important;
#   letter-spacing: -1.5px !important;
#   margin: 0 0 12px !important;
#   line-height: 1.05 !important;
#   text-shadow: 0 0 80px rgba(171,130,255,0.35) !important;
# }

# .hero-title span {
#   background: linear-gradient(135deg, #f5d97e 30%, #e0b8ff);
#   -webkit-background-clip: text;
#   -webkit-text-fill-color: transparent;
#   background-clip: text;
# }

# .hero-subtitle {
#   font-size: 1rem !important;
#   color: var(--text-muted) !important;
#   font-weight: 400 !important;
#   max-width: 500px;
#   margin: 0 auto !important;
#   line-height: 1.65 !important;
# }

# /* ── Section labels ── */
# .section-label {
#   font-size: 0.72rem !important;
#   font-weight: 700 !important;
#   letter-spacing: 0.18em !important;
#   text-transform: uppercase !important;
#   color: var(--gold) !important;
#   margin: 0 0 12px !important;
#   display: flex;
#   align-items: center;
#   gap: 10px;
#   opacity: 0.9;
# }

# .section-label::before {
#   content: "";
#   display: inline-block;
#   width: 18px;
#   height: 1.5px;
#   background: var(--gold-dim);
#   border-radius: 1px;
# }

# /* ── Input panels ── */
# .input-panel {
#   background: rgba(30,18,60,0.80) !important;
#   border: 1px solid rgba(171,130,255,0.28) !important;
#   border-radius: 20px !important;
#   padding: 24px !important;
#   box-shadow: 0 8px 36px rgba(0,0,0,0.45),
#               inset 0 1px 0 rgba(245,217,126,0.06),
#               var(--shadow-glow) !important;
#   backdrop-filter: blur(18px) !important;
# }

# /* ── Slider label text — dark color for readability on light Gradio backgrounds ── */
# label span,
# .gradio-slider label span,
# .gradio-slider > label > span,
# span.svelte-1gfkn6j,
# .gradio-slider span,
# .gradio-container .gradio-slider label > span:first-child {
#   color: #1a0f3c !important;
#   font-weight: 700 !important;
#   font-size: 0.9rem !important;
# }

# /* ── Slider value input box — keep number color as gold, darken only the label ── */
# .gradio-slider input[type="number"] {
#   /* Appearance only — no layout overrides that fight Gradio */
#   background: rgba(100,70,180,0.18) !important;
#   border: 1px solid rgba(196,168,255,0.4) !important;
#   border-radius: 6px !important;
#   color: #0d0820 !important;
#   font-family: 'Outfit', sans-serif !important;
#   font-size: 0.9rem !important;
#   font-weight: 600 !important;
#   text-align: center !important;
# }



# /* ── Slider bar color — soft glowing lavender, override native orange ── */
# .gradio-slider input[type=range] {
#   accent-color: #9b6dff !important;
#   -webkit-appearance: none !important;
#   appearance: none !important;
# }

# /* Webkit (Chrome/Safari) — thumb and filled track */
# .gradio-slider input[type=range]::-webkit-slider-thumb {
#   -webkit-appearance: none !important;
#   appearance: none !important;
#   background: #c4a8ff !important;
#   border: 2px solid #9b6dff !important;
#   width: 18px !important;
#   height: 18px !important;
#   border-radius: 50% !important;
#   box-shadow: 0 0 8px rgba(155,109,255,0.55) !important;
#   cursor: pointer !important;
# }

# .gradio-slider input[type=range]::-webkit-slider-runnable-track {
#   background: linear-gradient(90deg, #9b6dff, #c4a8ff) !important;
#   height: 4px !important;
#   border-radius: 2px !important;
# }

# /* Firefox */
# .gradio-slider input[type=range]::-moz-range-thumb {
#   background: #c4a8ff !important;
#   border: 2px solid #9b6dff !important;
#   width: 16px !important;
#   height: 16px !important;
#   border-radius: 50% !important;
#   box-shadow: 0 0 8px rgba(155,109,255,0.55) !important;
#   cursor: pointer !important;
# }

# .gradio-slider input[type=range]::-moz-range-track {
#   background: linear-gradient(90deg, #9b6dff, #c4a8ff) !important;
#   height: 4px !important;
#   border-radius: 2px !important;
# }

# /* Global input[type="number"] intentionally removed — was causing layout shift in Gradio sliders */



# /* ── General text inside components ── */
# .gradio-container p,
# .gradio-container span,
# .gradio-container div {
#   font-family: 'Outfit', sans-serif;
# }

# /* ── Analyze button ── */
# #analyze-btn {
#   background: linear-gradient(135deg, #6b3fa0 0%, #9b5de5 50%, #f5c842 100%) !important;
#   color: #0d0820 !important;
#   font-family: 'Syne', sans-serif !important;
#   font-size: 0.9rem !important;
#   font-weight: 800 !important;
#   letter-spacing: 0.12em !important;
#   text-transform: uppercase !important;
#   padding: 16px 56px !important;
#   border-radius: 50px !important;
#   border: none !important;
#   cursor: pointer !important;
#   box-shadow: 0 6px 30px rgba(155,93,229,0.5),
#               0 0 0 1px rgba(245,217,126,0.15),
#               inset 0 1px 0 rgba(255,255,255,0.15) !important;
#   transition: transform 0.25s cubic-bezier(0.34,1.56,0.64,1),
#               box-shadow 0.25s ease !important;
#   min-width: 240px !important;
# }

# #analyze-btn:hover {
#   transform: translateY(-4px) scale(1.05) !important;
#   box-shadow: 0 16px 44px rgba(155,93,229,0.6),
#               0 0 70px rgba(245,217,126,0.12) !important;
# }

# #analyze-btn:active {
#   transform: translateY(0) scale(0.97) !important;
# }

# .btn-row {
#   display: flex !important;
#   justify-content: center !important;
#   padding: 12px 0 30px !important;
# }

# /* ── Output cards ── */
# .output-card {
#   background: rgba(30,18,60,0.80) !important;
#   border: 1px solid rgba(171,130,255,0.28) !important;
#   border-radius: 16px !important;
#   padding: 20px !important;
#   box-shadow: 0 4px 26px rgba(0,0,0,0.4),
#               inset 0 1px 0 rgba(245,217,126,0.05) !important;
#   backdrop-filter: blur(14px) !important;
# }

# .gradio-plot, .gradio-html {
#   background: transparent !important;
#   border-radius: 16px !important;
# }

# .gradio-image {
#   border-radius: 14px !important;
#   border: 2px dashed rgba(196,168,255,0.38) !important;
#   background: rgba(26,15,60,0.5) !important;
# }
# .gradio-image:hover {
#   border-color: rgba(245,217,126,0.5) !important;
# }

# /* ── Markdown / image explanation panel — FIXED READABILITY ── */
# .gradio-markdown,
# .gradio-markdown p,
# .gradio-markdown span,
# .gradio-markdown div,
# div[data-testid="markdown"],
# div[data-testid="markdown"] p,
# div[data-testid="markdown"] span {
#   font-family: 'Outfit', sans-serif !important;
#   font-size: 0.92rem !important;
#   color: #e8deff !important;
#   line-height: 1.65 !important;
# }

# .gradio-markdown {
#   background: rgba(35,20,72,0.85) !important;
#   border-radius: 12px !important;
#   padding: 16px 18px !important;
#   border: 1px solid rgba(196,168,255,0.28) !important;
# }

# /* ── File download area ── */
# .gradio-file {
#   background: rgba(35,20,72,0.85) !important;
#   border: 1px solid rgba(245,217,126,0.25) !important;
#   border-radius: 12px !important;
#   color: #f0e8ff !important;
# }

# /* File component inner text */
# .gradio-file span,
# .gradio-file p,
# .gradio-file div,
# .gradio-file label,
# [data-testid="file"] span,
# [data-testid="file"] p,
# [data-testid="file"] div {
#   color: #e8deff !important;
#   font-size: 0.9rem !important;
# }

# /* ── Label text for image upload, file, markdown ── */
# .gradio-image label span,
# .gradio-file label span,
# .gradio-markdown label span {
#   color: #c4a8ff !important;
#   font-size: 0.95rem !important;
#   font-weight: 600 !important;
#   letter-spacing: 0.06em !important;
# }

# /* ── Results header & section labels brightness boost ── */
# .results-header {
#   font-family: 'Syne', sans-serif !important;
#   font-size: 1.3rem !important;
#   font-weight: 800 !important;
#   color: #f5f0ff !important;
#   text-align: center !important;
#   margin: 28px 0 12px !important;
#   letter-spacing: -0.02em !important;
# }

# .divider {
#   border: none;
#   border-top: 1px solid rgba(124,92,191,0.22);
#   margin: 6px 0 22px;
# }

# /* ── Scrollbar ── */
# ::-webkit-scrollbar { width: 5px; }
# ::-webkit-scrollbar-track { background: #0d0820; }
# ::-webkit-scrollbar-thumb { background: #3d2770; border-radius: 3px; }
# ::-webkit-scrollbar-thumb:hover { background: #ab82ff; }

# @keyframes fadeUp {
#   from { opacity: 0; transform: translateY(18px); }
#   to   { opacity: 1; transform: translateY(0); }
# }
# .gradio-container > * { animation: fadeUp 0.5s ease both; }
# """

# # ── UI ────────────────────────────────────────────────



# # ── Slider fix: appended last to override everything ──
# CUSTOM_CSS += """
# /* ===== FINAL FIX — NO CLIPPING ===== */
# .gradio-slider,
# .gradio-slider * {
#   overflow: visible !important;
# }
# .gradio-slider input[type="number"] {
#   width: 85px !important;
#   min-width: 85px !important;
#   padding: 4px 6px !important;
#   text-align: center !important;
#   box-sizing: border-box !important;
#   color: #0d0820 !important;
#   font-size: 0.9rem !important;
#   font-weight: 600 !important;
# }
# .gradio-slider div {
#   flex-shrink: 0 !important;
# }
# """

# with gr.Blocks(title="🌱 Soil Health AI", css=CUSTOM_CSS) as demo:

#     gr.HTML("""
#     <div id="hero-header">
#       <div class="hero-eyebrow">Precision Agriculture Intelligence</div>
#       <div class="hero-title">Soil Health <span>AI</span></div>
#       <p class="hero-subtitle">
#         Multimodal analysis for smarter farming — soil chemistry, crop recommendations,
#         irrigation advisory &amp; AI-powered image insights.
#       </p>
#     </div>
#     """)

#     with gr.Row(equal_height=True):
#         with gr.Column(scale=1):
#             gr.HTML('<div class="section-label">Soil Chemistry</div>')
#             with gr.Group(elem_classes="input-panel"):
#                 N   = gr.Slider(0,   140, 50,  label="Nitrogen (kg/ha)")
#                 P   = gr.Slider(5,   145, 50,  label="Phosphorus (kg/ha)")
#                 K   = gr.Slider(5,   200, 50,  label="Potassium (kg/ha)")
#                 pH  = gr.Slider(3,   10,  6.5, label="pH Level")
#                 OC  = gr.Slider(0.5, 20,  5,   label="Organic Carbon (%)")
#                 SD  = gr.Slider(4,   96,  50,  label="Sand Content (%)")

#         with gr.Column(scale=1):
#             gr.HTML('<div class="section-label">Environment & Location</div>')
#             with gr.Group(elem_classes="input-panel"):
#                 RF  = gr.Slider(0,    300, 100, label="Rainfall (mm)")
#                 TMP = gr.Slider(0,    50,  25,  label="Temperature (°C)")
#                 HUM = gr.Slider(10,   100, 60,  label="Humidity (%)")
#                 LAT = gr.Slider(-90,  90,  20,  label="Latitude")
#                 LON = gr.Slider(-180, 180, 78,  label="Longitude")
#             gr.HTML('<div class="section-label" style="margin-top:18px;">Soil / Crop Image</div>')
#             with gr.Group(elem_classes="input-panel"):
#                 IMG = gr.Image(label="Upload image (optional)", type="numpy",
#                                show_label=False, height=152)

#     with gr.Row(elem_classes="btn-row"):
#         btn = gr.Button("✦  Run Analysis", variant="primary", elem_id="analyze-btn")

#     gr.HTML('<div class="results-header">Analysis Results</div>')
#     gr.HTML('<hr class="divider">')

#     with gr.Row(equal_height=False):
#         with gr.Column(scale=1):
#             shi_html = gr.HTML(elem_classes="output-card")
#         with gr.Column(scale=1):
#             gauge_plot = gr.Plot(elem_classes="output-card")
#         with gr.Column(scale=1):
#             ndvi_plot_out = gr.Plot(elem_classes="output-card")

#     gr.HTML('<div class="section-label" style="margin-top:24px;">Geospatial View</div>')
#     map_html = gr.HTML(elem_classes="output-card")

#     gr.HTML('<div class="section-label" style="margin-top:24px;">Agronomic Intelligence</div>')
#     with gr.Row(equal_height=False):
#         with gr.Column(scale=1):
#             crop_html = gr.HTML(elem_classes="output-card")
#         with gr.Column(scale=1):
#             fert_html = gr.HTML(elem_classes="output-card")
#         with gr.Column(scale=1):
#             irr_html  = gr.HTML(elem_classes="output-card")

#     gr.HTML('<div class="section-label" style="margin-top:24px;">Image Intelligence & Report</div>')
#     with gr.Row():
#         with gr.Column(scale=2):
#             img_out_html = gr.HTML(elem_classes="output-card")
#         with gr.Column(scale=1):
#             img_out_md = gr.Markdown(label="Image Explanation")
#             pdf_file   = gr.File(label="📥 Download Full PDF Report")

#     btn.click(
#         fn=predict_fn,
#         inputs=[N, P, K, pH, RF, TMP, HUM, OC, SD, IMG, LAT, LON],
#         outputs=[
#             shi_html, gauge_plot, ndvi_plot_out, map_html,
#             crop_html, fert_html, irr_html,
#             img_out_html, img_out_md, pdf_file,
#         ],
#     )

# demo.launch(share=True)



import os
import gradio as gr
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import folium
from PIL import Image

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from decision_support import SoilProfile, generate_full_report

# ── Load image analyzer ───────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH  = os.path.join(BASE_DIR, "soil_image_model.pt")
LABEL_PATH  = os.path.join(BASE_DIR, "soil_image_labels.json")

_analyzer = None

def get_analyzer():
    global _analyzer
    if _analyzer is not None:
        return _analyzer
    if os.path.exists(MODEL_PATH):
        try:
            try:
                from image_inference_v2 import SoilImageAnalyzer
            except ImportError:
                from image_inference import SoilImageAnalyzer
            _analyzer = SoilImageAnalyzer(
                model_path=MODEL_PATH,
                label_path=LABEL_PATH if os.path.exists(LABEL_PATH) else None,
                device="cpu",
            )
            print("✅ Image model loaded successfully")
        except Exception as e:
            print(f"⚠️  Could not load model: {e}")
    else:
        print(f"⚠️  Model not found at: {MODEL_PATH}")
        print("    → Running in demo mode")
        print("    → Place soil_image_model.pt in:", BASE_DIR)
    return _analyzer


# ── SHI ──────────────────────────────────────────────
def compute_shi(N, P, K, pH, OC):
    n  = min(N / 140, 1)
    p  = min(P / 145, 1)
    k  = min(K / 200, 1)
    ph = 1 - abs(pH - 6.5) / 3.5
    oc = min(OC / 20, 1)
    return float(np.clip(0.3 * ph + 0.2 * n + 0.15 * p + 0.15 * k + 0.2 * oc, 0, 1))


def create_gauge(shi):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=shi,
        title={"text": "Soil Health Index", "font": {"size": 16, "color": "#c9b8f0", "family": "Outfit"}},
        number={"font": {"size": 44, "color": "#f5d97e", "family": "Outfit"}, "suffix": ""},
        gauge={
            "axis": {"range": [0, 1], "tickcolor": "#7c5cbf", "tickfont": {"color": "#a08ad4"}},
            "bar": {"color": "#f5d97e"},
            "bgcolor": "rgba(0,0,0,0)",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 0.35], "color": "rgba(239,83,80,0.25)"},
                {"range": [0.35, 0.5], "color": "rgba(255,183,77,0.25)"},
                {"range": [0.5, 1],   "color": "rgba(171,130,255,0.25)"},
            ],
            "threshold": {
                "line": {"color": "#f5d97e", "width": 3},
                "thickness": 0.78,
                "value": shi,
            },
        }
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=40, b=10, l=20, r=20),
        height=260,
        font={"family": "Outfit"},
    )
    return fig


def get_ndvi(lat):
    base = 0.4 + (lat % 10) / 50
    return [round(base + i * 0.04, 3) for i in range(8)]


def ndvi_plot(ndvi):
    fig = px.line(
        x=list(range(1, 9)), y=ndvi,
        title="NDVI Trend Over Time",
        labels={"x": "Time Step", "y": "NDVI"},
    )
    fig.update_traces(
        line=dict(color="#f5d97e", width=3),
        mode="lines+markers",
        marker=dict(size=8, color="#ab82ff", symbol="circle"),
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(30,18,60,0.5)",
        font={"family": "Outfit", "color": "#c9b8f0"},
        title_font={"size": 15, "color": "#f5d97e", "family": "Outfit"},
        xaxis=dict(gridcolor="rgba(124,92,191,0.2)", linecolor="rgba(124,92,191,0.3)", color="#a08ad4"),
        yaxis=dict(gridcolor="rgba(124,92,191,0.2)", linecolor="rgba(124,92,191,0.3)", color="#a08ad4"),
        margin=dict(t=48, b=30, l=40, r=20),
        height=260,
    )
    return fig


def create_map(lat, lon):
    m = folium.Map(location=[lat, lon], zoom_start=6, tiles="CartoDB dark_matter")
    folium.Marker(
        [lat, lon],
        tooltip="📍 Soil Sample Location",
        icon=folium.Icon(color="purple", icon="star", prefix="fa"),
    ).add_to(m)
    folium.Circle(
        radius=50000, location=[lat, lon],
        color="#ab82ff", fill=True, fill_color="#7c5cbf", fill_opacity=0.15,
    ).add_to(m)
    return m._repr_html_()


def card(title, content, icon=""):
    return f"""
<div style="
  padding: 20px 24px;
  border-radius: 16px;
  background: rgba(30,18,60,0.82);
  margin: 8px 0;
  border: 1px solid rgba(171,130,255,0.22);
  box-shadow: 0 4px 24px rgba(0,0,0,0.4), inset 0 1px 0 rgba(245,217,126,0.08);
  font-family: 'Outfit', sans-serif;
  backdrop-filter: blur(14px);
">
  <h3 style="margin-top:0; color:#f5d97e; font-size:0.85rem; letter-spacing:0.1em;
             text-transform:uppercase; font-weight:700; margin-bottom:14px;
             display:flex; align-items:center; gap:8px;">
    <span>{icon}</span> {title}
  </h3>
  <div style="color:#e8deff;">{content}</div>
</div>"""


# ── Image analysis ────────────────────────────────────
def analyze_image(img):
    analyzer = get_analyzer()

    if img is None:
        return (
            """<div style="padding:24px;border-radius:16px;
                background:rgba(30,18,60,0.82);border:1px dashed rgba(171,130,255,0.35);
                font-family:'Outfit',sans-serif;text-align:center;">
  <div style="font-size:2.8rem;margin-bottom:10px;">📸</div>
  <h3 style="color:#f5d97e;margin:0 0 6px;font-size:1rem;">Image Analysis</h3>
  <p style="color:#b8a8e0;margin:0;font-size:0.88rem;">Upload a soil or crop image to get AI-powered visual analysis.</p>
</div>""",
            "No image uploaded."
        )

    if analyzer is None:
        h, w = (img.shape[0], img.shape[1]) if hasattr(img, "shape") else ("?", "?")
        return (
            f"""<div style="padding:20px;border-radius:16px;background:rgba(42,24,10,0.85);
                border:1px solid rgba(255,183,77,0.35);font-family:'Outfit',sans-serif;">
  <h3 style="color:#ffb74d;margin-top:0;font-size:1rem;">⚠️ Demo Mode — Model not loaded</h3>
  <p style="color:#e0d4ff;font-size:0.88rem;">Place <b>soil_image_model.pt</b> in:</p>
  <code style="background:rgba(0,0,0,0.35);padding:4px 10px;border-radius:6px;
               font-size:0.8rem;color:#f5d97e;">{BASE_DIR}</code>
  <p style="color:#c4a8ff;margin-bottom:0;margin-top:10px;font-size:0.88rem;">✅ Image received: {w}×{h}px</p>
</div>""",
            f"⚠️ Model not loaded. Put soil_image_model.pt in: {BASE_DIR}"
        )

    result = analyzer.analyze(img)
    return result["html"], result["explanation"]


# ── PDF ───────────────────────────────────────────────
def generate_pdf(report, img_explanation=""):
    path = os.path.join(BASE_DIR, "soil_health_report.pdf")
    doc  = SimpleDocTemplate(path)
    styles = getSampleStyleSheet()
    body = []
    body.append(Paragraph("Soil Health Report", styles["Title"]))
    body.append(Spacer(1, 12))

    sa = report.get("soil_assessment", {})
    body.append(Paragraph("Soil Health Assessment", styles["Heading2"]))
    body.append(Paragraph(f"SHI: {sa.get('soil_health_index','N/A')}", styles["Normal"]))
    body.append(Paragraph(f"Class: {sa.get('soil_class','N/A')}", styles["Normal"]))
    body.append(Paragraph(sa.get("interpretation", ""), styles["Normal"]))
    body.append(Spacer(1, 12))

    if img_explanation:
        body.append(Paragraph("Image-Based Analysis", styles["Heading2"]))
        body.append(Paragraph(img_explanation, styles["Normal"]))
        body.append(Spacer(1, 12))

    body.append(Paragraph("Crop Recommendations", styles["Heading2"]))
    for c in report.get("crop_recommendations", []):
        body.append(Paragraph(
            f"• {c['crop']} — {c['suitability']} ({c['score_pct']}%)",
            styles["Normal"]
        ))
    body.append(Spacer(1, 12))

    body.append(Paragraph("Fertilizer Advice", styles["Heading2"]))
    for r in report.get("fertilizer_advice", {}).get("recommendations", []):
        body.append(Paragraph(f"• {r}", styles["Normal"]))
    body.append(Spacer(1, 12))

    body.append(Paragraph("Irrigation Advice", styles["Heading2"]))
    irr = report.get("irrigation_advice", {})
    body.append(Paragraph(f"Level: {irr.get('irrigation_level','')}", styles["Normal"]))
    body.append(Paragraph(irr.get("advice", ""), styles["Normal"]))

    doc.build(body)
    return path


# ── MAIN PREDICT ──────────────────────────────────────
def predict_fn(N, P, K, pH, RF, TMP, HUM, OC, SD, IMG, LAT, LON):
    shi = compute_shi(N, P, K, pH, OC)

    if shi < 0.35:
        status, badge_color, badge_bg = "Poor",     "#ef5350", "rgba(239,83,80,0.18)"
        icon = "🔴"
    elif shi < 0.5:
        status, badge_color, badge_bg = "Moderate", "#ffb74d", "rgba(255,183,77,0.18)"
        icon = "🟡"
    else:
        status, badge_color, badge_bg = "Healthy",  "#ab82ff", "rgba(171,130,255,0.22)"
        icon = "✨"

    profile = SoilProfile(N=N, P=P, K=K, pH=pH,
                          rainfall=RF, temperature=TMP, humidity=HUM,
                          organic_carbon=OC, sand=SD,
                          shi=shi, soil_class=status)
    report = generate_full_report(profile)
    img_html, img_text = analyze_image(IMG)

    # ── SHI Hero Card ──
    shi_card = f"""
<div style="
  padding: 32px 28px;
  border-radius: 20px;
  background: linear-gradient(145deg, rgba(42,24,80,0.96), rgba(18,10,46,0.99));
  border: 1px solid rgba(245,217,126,0.22);
  box-shadow: 0 8px 40px rgba(0,0,0,0.55),
              0 0 0 1px rgba(171,130,255,0.1),
              inset 0 1px 0 rgba(245,217,126,0.1);
  font-family: 'Outfit', sans-serif;
  text-align: center;
  position: relative;
  overflow: hidden;
">
  <div style="
    position:absolute;top:-50px;left:50%;transform:translateX(-50%);
    width:200px;height:200px;
    background:radial-gradient(circle, rgba(171,130,255,0.15) 0%, transparent 70%);
    pointer-events:none;
  "></div>
  <div style="font-size:2.8rem;margin-bottom:10px;position:relative;">{icon}</div>
  <div style="font-size:4.2rem;font-weight:800;color:#f5d97e;
              line-height:1;letter-spacing:-3px;position:relative;">
    {shi:.3f}
  </div>
  <div style="font-size:0.72rem;color:#b8a8e0;margin-top:10px;letter-spacing:0.16em;
              text-transform:uppercase;font-weight:600;">
    Soil Health Index
  </div>
  <div style="
    display:inline-block;margin-top:16px;
    padding:7px 26px;border-radius:50px;
    background:{badge_bg};
    border:1.5px solid {badge_color}88;
    color:{badge_color};font-weight:700;font-size:0.9rem;letter-spacing:0.05em;
  ">{status}</div>
</div>"""

    # ── Crop Card ──
    crops = report.get("crop_recommendations", [])
    crop_rows = ""
    for c in crops:
        pct = c['score_pct']
        bar_color = "#ab82ff" if pct >= 70 else ("#ffb74d" if pct >= 50 else "#ef5350")
        issues = ', '.join(c['issues']) if c['issues'] else "All conditions met ✓"
        crop_rows += f"""
<div style="margin-bottom:16px;">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:5px;">
    <span style="font-weight:600;color:#f0e8ff;font-size:0.9rem;">🌾 {c['crop']}</span>
    <span style="font-size:0.78rem;color:{bar_color};font-weight:700;
                 background:rgba(0,0,0,0.3);padding:2px 10px;border-radius:50px;
                 border:1px solid {bar_color}44;">
      {c['suitability']} · {pct}%
    </span>
  </div>
  <div style="background:rgba(124,92,191,0.2);border-radius:50px;height:6px;overflow:hidden;">
    <div style="width:{pct}%;height:100%;
                background:linear-gradient(90deg,{bar_color}88,{bar_color});
                border-radius:50px;"></div>
  </div>
  <div style="font-size:0.73rem;color:#a090cc;margin-top:4px;">{issues}</div>
</div>"""
    crop_card = card("Crop Recommendations", crop_rows, "🌾")

    # ── Fertilizer Card ──
    fert = report.get("fertilizer_advice", {})
    fert_items = "".join(
        f'<div style="display:flex;align-items:flex-start;gap:10px;margin-bottom:12px;">'
        f'<span style="color:#f5d97e;font-size:0.9rem;margin-top:3px;flex-shrink:0;">◆</span>'
        f'<span style="color:#e8deff;font-size:0.87rem;line-height:1.55;">{r}</span>'
        f'</div>'
        for r in fert.get("recommendations", [])
    )
    fert_card = card("Fertilizer Recommendations", fert_items, "🧪")

    # ── Irrigation Card ──
    irr = report.get("irrigation_advice", {})
    irr_content = f"""
<div style="display:flex;align-items:center;gap:12px;margin-bottom:14px;flex-wrap:wrap;">
  <div style="
    background:linear-gradient(135deg,#5c3d9e,#9b5de5);
    color:white;padding:7px 20px;border-radius:50px;
    font-weight:700;font-size:0.85rem;letter-spacing:0.04em;white-space:nowrap;
    box-shadow:0 4px 14px rgba(124,92,191,0.4);
  ">{irr.get('irrigation_level','')}</div>
  <div style="color:#c4b4f0;font-size:0.87rem;">{irr.get('frequency','')}</div>
</div>
<p style="color:#e8deff;font-size:0.87rem;line-height:1.6;margin:0;">{irr.get('advice','')}</p>"""
    irr_card = card("Irrigation Advisory", irr_content, "💧")

    pdf = generate_pdf(report, img_text)

    return (shi_card, create_gauge(shi), ndvi_plot(get_ndvi(LAT)),
            create_map(LAT, LON), crop_card, fert_card, irr_card,
            img_html, img_text, pdf)


# ── CUSTOM CSS ────────────────────────────────────────
CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Syne:wght@700;800&display=swap');

:root {
  --purple-deep:    #0d0820;
  --purple-dark:    #1a0f3c;
  --purple-mid:     #2a1850;
  --purple-card:    rgba(30,18,60,0.82);
  --purple-border:  rgba(171,130,255,0.25);
  --purple-accent:  #c4a8ff;
  --purple-soft:    #9b7fd4;
  --gold:           #f5d97e;
  --gold-dim:       #c9a84c;
  --text-primary:   #f5f0ff;
  --text-secondary: #e8deff;
  --text-muted:     #c4b4f0;
  --shadow-glow:    0 0 50px rgba(124,92,191,0.2);
}

*, *::before, *::after { box-sizing: border-box; }

body, .gradio-container {
  font-family: 'Outfit', sans-serif !important;
  background: radial-gradient(ellipse at 20% 10%, #2a1060 0%, #0d0820 45%, #060414 100%) !important;
  min-height: 100vh;
  color: var(--text-primary) !important;
}

/* ── Ambient glow orbs ── */
.gradio-container::before {
  content: "";
  position: fixed;
  inset: 0;
  background:
    radial-gradient(ellipse 600px 400px at 10% 20%, rgba(124,92,191,0.12) 0%, transparent 70%),
    radial-gradient(ellipse 400px 300px at 90% 80%, rgba(245,217,126,0.07) 0%, transparent 70%),
    radial-gradient(ellipse 300px 400px at 80% 15%, rgba(155,93,229,0.08) 0%, transparent 70%);
  pointer-events: none;
  z-index: 0;
}

/* ── Hero ── */
#hero-header {
  text-align: center;
  padding: 56px 24px 38px;
  position: relative;
  z-index: 1;
}

.hero-eyebrow {
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--gold);
  margin-bottom: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  opacity: 0.9;
}

.hero-eyebrow::before,
.hero-eyebrow::after {
  content: "";
  display: inline-block;
  width: 36px;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--gold-dim));
}
.hero-eyebrow::after {
  background: linear-gradient(90deg, var(--gold-dim), transparent);
}

.hero-title {
  font-family: 'Syne', sans-serif !important;
  font-size: clamp(2.2rem, 5.5vw, 3.4rem) !important;
  font-weight: 800 !important;
  color: var(--text-primary) !important;
  letter-spacing: -1.5px !important;
  margin: 0 0 12px !important;
  line-height: 1.05 !important;
  text-shadow: 0 0 80px rgba(171,130,255,0.35) !important;
}

.hero-title span {
  background: linear-gradient(135deg, #f5d97e 30%, #e0b8ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 1rem !important;
  color: var(--text-muted) !important;
  font-weight: 400 !important;
  max-width: 500px;
  margin: 0 auto !important;
  line-height: 1.65 !important;
}

/* ── Section labels ── */
.section-label {
  font-size: 0.72rem !important;
  font-weight: 700 !important;
  letter-spacing: 0.18em !important;
  text-transform: uppercase !important;
  color: var(--gold) !important;
  margin: 0 0 12px !important;
  display: flex;
  align-items: center;
  gap: 10px;
  opacity: 0.9;
}

.section-label::before {
  content: "";
  display: inline-block;
  width: 18px;
  height: 1.5px;
  background: var(--gold-dim);
  border-radius: 1px;
}

/* ── Input panels ── */
.input-panel {
  background: rgba(30,18,60,0.80) !important;
  border: 1px solid rgba(171,130,255,0.28) !important;
  border-radius: 20px !important;
  padding: 24px !important;
  box-shadow: 0 8px 36px rgba(0,0,0,0.45),
              inset 0 1px 0 rgba(245,217,126,0.06),
              var(--shadow-glow) !important;
  backdrop-filter: blur(18px) !important;
}

/* ── Slider label text — dark color for readability on light Gradio backgrounds ── */
label span,
.gradio-slider label span,
.gradio-slider > label > span,
span.svelte-1gfkn6j,
.gradio-slider span,
.gradio-container .gradio-slider label > span:first-child {
  color: #1a0f3c !important;
  font-weight: 700 !important;
  font-size: 0.9rem !important;
}

/* ── Slider value input box — keep number color as gold, darken only the label ── */
/* slider input styled via inline <style> tag in gr.HTML */



/* ── Slider bar color — soft glowing lavender, override native orange ── */
.gradio-slider input[type=range] {
  accent-color: #9b6dff !important;
  -webkit-appearance: none !important;
  appearance: none !important;
}

/* Webkit (Chrome/Safari) — thumb and filled track */
.gradio-slider input[type=range]::-webkit-slider-thumb {
  -webkit-appearance: none !important;
  appearance: none !important;
  background: #c4a8ff !important;
  border: 2px solid #9b6dff !important;
  width: 18px !important;
  height: 18px !important;
  border-radius: 50% !important;
  box-shadow: 0 0 8px rgba(155,109,255,0.55) !important;
  cursor: pointer !important;
}

.gradio-slider input[type=range]::-webkit-slider-runnable-track {
  background: linear-gradient(90deg, #9b6dff, #c4a8ff) !important;
  height: 4px !important;
  border-radius: 2px !important;
}

/* Firefox */
.gradio-slider input[type=range]::-moz-range-thumb {
  background: #c4a8ff !important;
  border: 2px solid #9b6dff !important;
  width: 16px !important;
  height: 16px !important;
  border-radius: 50% !important;
  box-shadow: 0 0 8px rgba(155,109,255,0.55) !important;
  cursor: pointer !important;
}

.gradio-slider input[type=range]::-moz-range-track {
  background: linear-gradient(90deg, #9b6dff, #c4a8ff) !important;
  height: 4px !important;
  border-radius: 2px !important;
}

/* Global input[type="number"] intentionally removed — was causing layout shift in Gradio sliders */



/* ── General text inside components ── */
.gradio-container p,
.gradio-container span,
.gradio-container div {
  font-family: 'Outfit', sans-serif;
}

/* ── Analyze button ── */
#analyze-btn {
  background: linear-gradient(135deg, #6b3fa0 0%, #9b5de5 50%, #f5c842 100%) !important;
  color: #0d0820 !important;
  font-family: 'Syne', sans-serif !important;
  font-size: 0.9rem !important;
  font-weight: 800 !important;
  letter-spacing: 0.12em !important;
  text-transform: uppercase !important;
  padding: 16px 56px !important;
  border-radius: 50px !important;
  border: none !important;
  cursor: pointer !important;
  box-shadow: 0 6px 30px rgba(155,93,229,0.5),
              0 0 0 1px rgba(245,217,126,0.15),
              inset 0 1px 0 rgba(255,255,255,0.15) !important;
  transition: transform 0.25s cubic-bezier(0.34,1.56,0.64,1),
              box-shadow 0.25s ease !important;
  min-width: 240px !important;
}

#analyze-btn:hover {
  transform: translateY(-4px) scale(1.05) !important;
  box-shadow: 0 16px 44px rgba(155,93,229,0.6),
              0 0 70px rgba(245,217,126,0.12) !important;
}

#analyze-btn:active {
  transform: translateY(0) scale(0.97) !important;
}

.btn-row {
  display: flex !important;
  justify-content: center !important;
  padding: 12px 0 30px !important;
}

/* ── Output cards ── */
.output-card {
  background: rgba(30,18,60,0.80) !important;
  border: 1px solid rgba(171,130,255,0.28) !important;
  border-radius: 16px !important;
  padding: 20px !important;
  box-shadow: 0 4px 26px rgba(0,0,0,0.4),
              inset 0 1px 0 rgba(245,217,126,0.05) !important;
  backdrop-filter: blur(14px) !important;
}

.gradio-plot, .gradio-html {
  background: transparent !important;
  border-radius: 16px !important;
}

.gradio-image {
  border-radius: 14px !important;
  border: 2px dashed rgba(196,168,255,0.38) !important;
  background: rgba(26,15,60,0.5) !important;
}
.gradio-image:hover {
  border-color: rgba(245,217,126,0.5) !important;
}

/* ── Markdown / image explanation panel — FIXED READABILITY ── */
.gradio-markdown,
.gradio-markdown p,
.gradio-markdown span,
.gradio-markdown div,
div[data-testid="markdown"],
div[data-testid="markdown"] p,
div[data-testid="markdown"] span {
  font-family: 'Outfit', sans-serif !important;
  font-size: 0.92rem !important;
  color: #e8deff !important;
  line-height: 1.65 !important;
}

.gradio-markdown {
  background: rgba(35,20,72,0.85) !important;
  border-radius: 12px !important;
  padding: 16px 18px !important;
  border: 1px solid rgba(196,168,255,0.28) !important;
}

/* ── File download area ── */
.gradio-file {
  background: rgba(35,20,72,0.85) !important;
  border: 1px solid rgba(245,217,126,0.25) !important;
  border-radius: 12px !important;
  color: #f0e8ff !important;
}

/* File component inner text */
.gradio-file span,
.gradio-file p,
.gradio-file div,
.gradio-file label,
[data-testid="file"] span,
[data-testid="file"] p,
[data-testid="file"] div {
  color: #e8deff !important;
  font-size: 0.9rem !important;
}

/* ── Label text for image upload, file, markdown ── */
.gradio-image label span,
.gradio-file label span,
.gradio-markdown label span {
  color: #c4a8ff !important;
  font-size: 0.95rem !important;
  font-weight: 600 !important;
  letter-spacing: 0.06em !important;
}

/* ── Results header & section labels brightness boost ── */
.results-header {
  font-family: 'Syne', sans-serif !important;
  font-size: 1.3rem !important;
  font-weight: 800 !important;
  color: #f5f0ff !important;
  text-align: center !important;
  margin: 28px 0 12px !important;
  letter-spacing: -0.02em !important;
}

.divider {
  border: none;
  border-top: 1px solid rgba(124,92,191,0.22);
  margin: 6px 0 22px;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #0d0820; }
::-webkit-scrollbar-thumb { background: #3d2770; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #ab82ff; }

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(18px); }
  to   { opacity: 1; transform: translateY(0); }
}
.gradio-container > * { animation: fadeUp 0.5s ease both; }
"""

# ── UI ────────────────────────────────────────────────




with gr.Blocks(title="🌱 Soil Health AI", css=CUSTOM_CSS) as demo:

    gr.HTML("""
    <style>
    /* ====================================================
       SLIDER NUMBER INPUT — INJECTED AFTER SVELTE STYLES
       This fires last and cannot be overridden by Gradio.
    ==================================================== */
    input[type=number] {
        width: 80px !important;
        min-width: 80px !important;
        max-width: 80px !important;
        height: 32px !important;
        padding: 0 6px !important;
        box-sizing: border-box !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        color: #1a0f3c !important;
        text-align: center !important;
        background: rgba(196,168,255,0.15) !important;
        border: 1px solid rgba(196,168,255,0.5) !important;
        border-radius: 6px !important;
        overflow: visible !important;
        flex-shrink: 0 !important;
        display: block !important;
    }
    /* Ensure no parent clips the input */
    .gradio-slider,
    .gradio-slider > *,
    .gradio-slider label,
    .gradio-slider label > * {
        overflow: visible !important;
    }
    </style>
    <div id="hero-header">
      <div class="hero-eyebrow">Precision Agriculture Intelligence</div>
      <div class="hero-title">Soil Health <span>AI</span></div>
      <p class="hero-subtitle">
        Multimodal analysis for smarter farming — soil chemistry, crop recommendations,
        irrigation advisory &amp; AI-powered image insights.
      </p>
    </div>
    """)

    with gr.Row(equal_height=True):
        with gr.Column(scale=1):
            gr.HTML('<div class="section-label">Soil Chemistry</div>')
            with gr.Group(elem_classes="input-panel"):
                N   = gr.Slider(0,   140, 50,  label="Nitrogen (kg/ha)")
                P   = gr.Slider(5,   145, 50,  label="Phosphorus (kg/ha)")
                K   = gr.Slider(5,   200, 50,  label="Potassium (kg/ha)")
                pH  = gr.Slider(3,   10,  6.5, label="pH Level")
                OC  = gr.Slider(0.5, 20,  5,   label="Organic Carbon (%)")
                SD  = gr.Slider(4,   96,  50,  label="Sand Content (%)")

        with gr.Column(scale=1):
            gr.HTML('<div class="section-label">Environment & Location</div>')
            with gr.Group(elem_classes="input-panel"):
                RF  = gr.Slider(0,    300, 100, label="Rainfall (mm)")
                TMP = gr.Slider(0,    50,  25,  label="Temperature (°C)")
                HUM = gr.Slider(10,   100, 60,  label="Humidity (%)")
                LAT = gr.Slider(-90,  90,  20,  label="Latitude")
                LON = gr.Slider(-180, 180, 78,  label="Longitude")
            gr.HTML('<div class="section-label" style="margin-top:18px;">Soil / Crop Image</div>')
            with gr.Group(elem_classes="input-panel"):
                IMG = gr.Image(label="Upload image (optional)", type="numpy",
                               show_label=False, height=152)

    with gr.Row(elem_classes="btn-row"):
        btn = gr.Button("✦  Run Analysis", variant="primary", elem_id="analyze-btn")

    gr.HTML('<div class="results-header">Analysis Results</div>')
    gr.HTML('<hr class="divider">')

    with gr.Row(equal_height=False):
        with gr.Column(scale=1):
            shi_html = gr.HTML(elem_classes="output-card")
        with gr.Column(scale=1):
            gauge_plot = gr.Plot(elem_classes="output-card")
        with gr.Column(scale=1):
            ndvi_plot_out = gr.Plot(elem_classes="output-card")

    gr.HTML('<div class="section-label" style="margin-top:24px;">Geospatial View</div>')
    map_html = gr.HTML(elem_classes="output-card")

    gr.HTML('<div class="section-label" style="margin-top:24px;">Agronomic Intelligence</div>')
    with gr.Row(equal_height=False):
        with gr.Column(scale=1):
            crop_html = gr.HTML(elem_classes="output-card")
        with gr.Column(scale=1):
            fert_html = gr.HTML(elem_classes="output-card")
        with gr.Column(scale=1):
            irr_html  = gr.HTML(elem_classes="output-card")

    gr.HTML('<div class="section-label" style="margin-top:24px;">Image Intelligence & Report</div>')
    with gr.Row():
        with gr.Column(scale=2):
            img_out_html = gr.HTML(elem_classes="output-card")
        with gr.Column(scale=1):
            img_out_md = gr.Markdown(label="Image Explanation")
            pdf_file   = gr.File(label="📥 Download Full PDF Report")

    btn.click(
        fn=predict_fn,
        inputs=[N, P, K, pH, RF, TMP, HUM, OC, SD, IMG, LAT, LON],
        outputs=[
            shi_html, gauge_plot, ndvi_plot_out, map_html,
            crop_html, fert_html, irr_html,
            img_out_html, img_out_md, pdf_file,
        ],
    )

demo.launch(share=True)