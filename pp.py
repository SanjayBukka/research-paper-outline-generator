import streamlit as st
import google.generativeai as genai

def configure_gemini(api_key: str):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')

def generate_section_outline(model, section: str, topic: str) -> str:
    prompts = {
        'abstract': f"""
        Provide a detailed outline for the Abstract section of a research paper on: {topic}
        Include key points that should be covered:
        1. Research problem/background
        2. Methodology overview
        3. Key findings
        4. Main conclusions
        """,
        
        'introduction': f"""
        Provide a detailed outline for the Introduction section of a research paper on: {topic}
        Include key points that should be covered:
        1. Background context
        2. Problem statement
        3. Research significance
        4. Research objectives
        5. Literature review areas
        6. Research questions/hypotheses
        """,
        
        'methodology': f"""
        Provide a detailed outline for the Methodology section of a research paper on: {topic}
        Include key points that should be covered:
        1. Research design
        2. Data collection methods
        3. Analysis procedures
        4. Tools/instruments used
        5. Sampling strategy
        6. Validity/reliability considerations
        """,
        
        'results': f"""
        Provide a detailed outline for the Results section of a research paper on: {topic}
        Include key points that should be covered:
        1. Key findings
        2. Data presentation structure
        3. Statistical analyses
        4. Visual representations needed
        """,
        
        'discussion': f"""
        Provide a detailed outline for the Discussion section of a research paper on: {topic}
        Include key points that should be covered:
        1. Interpretation of results
        2. Comparison with literature
        3. Implications of findings
        4. Study limitations
        5. Future research directions
        """,
        
        'conclusion': f"""
        Provide a detailed outline for the Conclusion section of a research paper on: {topic}
        Include key points that should be covered:
        1. Summary of key findings
        2. Research contribution
        3. Practical implications
        4. Final thoughts
        """
    }
    
    response = model.generate_content(prompts.get(section.lower(), ''))
    return response.text

def main():
    st.title("Research Paper Outline Generator")
    
    api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
    if not api_key:
        st.warning("Please enter your Gemini API key to continue")
        return
    
    model = configure_gemini(api_key)
    
    topic = st.text_input("Enter your research topic:")
    
    if topic:
        sections = ['abstract', 'introduction', 'methodology', 
                   'results', 'discussion', 'conclusion']
        
        for section in sections:
            with st.expander(f"{section.title()} Outline", expanded=True):
                if st.button(f"Generate {section.title()} Outline"):
                    with st.spinner(f"Generating {section} outline..."):
                        outline = generate_section_outline(model, section, topic)
                        st.markdown(outline)

if __name__ == "__main__":
    main()