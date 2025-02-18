import streamlit as st
import google.generativeai as genai
from typing import Dict, List
import json

# Configure Gemini API
def configure_gemini(api_key: str):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')

# Initialize session state
def init_session_state():
    if 'current_section' not in st.session_state:
        st.session_state.current_section = 'Topic Selection'
    if 'paper_content' not in st.session_state:
        st.session_state.paper_content = {
            'topic': '',
            'abstract': '',
            'introduction': '',
            'methodology': '',
            'results': '',
            'discussion': '',
            'conclusion': '',
            'references': ''
        }

RESEARCH_GUIDELINES = {
    'abstract': """
    Guidelines for Abstract:
    - Keep it short and simple (200-250 words)
    - Include research problem, methodology, key findings
    - Use past tense for completed actions
    - Avoid citations and abbreviations
    """,
    'introduction': """
    Guidelines for Introduction:
    - Start with broader context
    - Narrow down to research problem
    - State research objectives clearly
    - Review relevant literature
    - Present research questions/hypotheses
    """,
    # Add other sections' guidelines similarly
}

def generate_section_guidance(model, section: str, topic: str) -> str:
    prompt = f"""
    As a research paper writing assistant, provide detailed guidance for writing the {section} section 
    of a research paper on the topic: {topic}
    
    Include:
    1. Specific points to cover
    2. Common mistakes to avoid
    3. Writing style recommendations
    4. Section-specific tips
    5. Examples or templates where appropriate
    
    Base your response on standard academic writing practices and these guidelines:
    {RESEARCH_GUIDELINES.get(section.lower(), '')}
    """
    
    response = model.generate_content(prompt)
    return response.text

def main():
    st.title("Academic Research Assistant/Research Paper Writing Assistant")
    
    # API Key Input
    api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
    if not api_key:
        st.warning("Please enter your Gemini API key to continue")
        return
    
    model = configure_gemini(api_key)
    init_session_state()
    
    # Sidebar Navigation
    sections = [
        "Topic Selection",
        "Abstract",
        "Introduction",
        "Methodology",
        "Results",
        "Discussion",
        "Conclusion",
        "References"
    ]
    
    selected_section = st.sidebar.radio("Navigate Sections", sections)
    st.session_state.current_section = selected_section
    
    # Topic Selection
    if selected_section == "Topic Selection":
        st.header("Research Topic Selection")
        topic = st.text_input("Enter your research topic:", 
                            value=st.session_state.paper_content['topic'])
        
        if st.button("Get Topic Feedback") and topic:
            with st.spinner("Analyzing topic..."):
                prompt = f"""
                Analyze this research topic: {topic}
                
                Provide:
                1. Topic strength evaluation
                2. Suggested refinements
                3. Potential research questions
                4. Key areas to focus on
                5. Possible challenges
                """
                response = model.generate_content(prompt)
                st.markdown(response.text)
            
            st.session_state.paper_content['topic'] = topic
    
    # Other Sections
    else:
        if not st.session_state.paper_content['topic']:
            st.warning("Please select a topic first")
            return
            
        st.header(selected_section)
        
        # Display section guidelines
        with st.expander("View Section Guidelines", expanded=True):
            guidance = generate_section_guidance(
                model, 
                selected_section, 
                st.session_state.paper_content['topic']
            )
            st.markdown(guidance)
        
        # Section content input
        section_content = st.text_area(
            f"Write your {selected_section} here:",
            value=st.session_state.paper_content[selected_section.lower()],
            height=300
        )
        
        if st.button("Get Feedback"):
            with st.spinner("Analyzing content..."):
                prompt = f"""
                Review this {selected_section} section for a research paper on 
                {st.session_state.paper_content['topic']}.
                
                Content to review:
                {section_content}
                
                Provide:
                1. Content evaluation
                2. Style and clarity feedback
                3. Specific improvement suggestions
                4. Missing elements
                5. Strengths of the current version
                """
                response = model.generate_content(prompt)
                st.markdown(response.text)
            
            st.session_state.paper_content[selected_section.lower()] = section_content

    # Export functionality
    if st.sidebar.button("Export Paper Content"):
        paper_content = json.dumps(st.session_state.paper_content, indent=2)
        st.sidebar.download_button(
            label="Download Paper Content",
            data=paper_content,
            file_name="research_paper_content.json",
            mime="application/json"
        )

if __name__ == "__main__":
    main()
